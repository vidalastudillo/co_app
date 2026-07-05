# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import getdate, today

test_ignore = ["Company"]

TEST_USER_EMAIL = "consultanormativa.test@vidalastudillo.com"


class TestConsultaNormativa(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		if not frappe.db.exists("User", TEST_USER_EMAIL):
			frappe.get_doc(
				{
					"doctype": "User",
					"email": TEST_USER_EMAIL,
					"first_name": "Consultado",
					"last_name": "De Prueba",
					"send_welcome_email": 0,
				}
			).insert(ignore_permissions=True)

	def make_consulta(self, **kwargs):
		data = {
			"doctype": "Consulta Normativa",
			"titulo": "Consulta de prueba sobre política contable",
			"pregunta": "<p>¿Cómo se clasifica este gasto según NIC 8?</p>",
		}
		data.update(kwargs)
		doc = frappe.get_doc(data)
		doc.insert(ignore_permissions=True)
		return doc

	def test_after_insert_crea_todo_para_consultado_a(self):
		"""Pieza 1: after_insert asigna vía frappe.desk.form.assign_to.add."""
		doc = self.make_consulta(consultado_a=TEST_USER_EMAIL)

		todo_existe = frappe.db.exists(
			"ToDo",
			{
				"reference_type": "Consulta Normativa",
				"reference_name": doc.name,
				"allocated_to": TEST_USER_EMAIL,
			},
		)
		self.assertTrue(todo_existe, "Se esperaba un ToDo asignado a consultado_a tras el after_insert")

	def test_sin_consultado_a_no_crea_todo(self):
		doc = self.make_consulta()

		todo_existe = frappe.db.exists(
			"ToDo", {"reference_type": "Consulta Normativa", "reference_name": doc.name}
		)
		self.assertFalse(todo_existe, "Sin consultado_a no debe crearse ninguna asignación")

	def test_fecha_respuesta_se_llena_al_transicionar_a_respondida(self):
		"""Pieza 2: la transición (no la mera presencia) llena fecha_respuesta con hoy."""
		doc = self.make_consulta()
		self.assertFalse(doc.fecha_respuesta)

		doc.estado = "Respondida"
		doc.save(ignore_permissions=True)
		doc.reload()

		self.assertEqual(getdate(doc.fecha_respuesta), getdate(today()))

	def test_fecha_respuesta_manual_no_se_sobrescribe_en_la_transicion(self):
		doc = self.make_consulta()
		fecha_manual = "2020-01-01"

		doc.estado = "Respondida"
		doc.fecha_respuesta = fecha_manual
		doc.save(ignore_permissions=True)
		doc.reload()

		self.assertEqual(getdate(doc.fecha_respuesta), getdate(fecha_manual))

	def test_volver_a_abierta_no_limpia_fecha_respuesta(self):
		doc = self.make_consulta()

		doc.estado = "Respondida"
		doc.save(ignore_permissions=True)
		doc.reload()
		fecha_respondida = doc.fecha_respuesta
		self.assertTrue(fecha_respondida)

		doc.estado = "Abierta"
		doc.save(ignore_permissions=True)
		doc.reload()

		self.assertEqual(getdate(doc.fecha_respuesta), getdate(fecha_respondida))

	def test_documento_nuevo_nace_respondida_llena_fecha(self):
		doc = self.make_consulta(estado="Respondida")

		self.assertEqual(getdate(doc.fecha_respuesta), getdate(today()))

	def test_notificaciones_generan_communication(self):
		"""Pieza 3 / pieza 7(e): verificación real, no simulada.

		`Document.run_notifications` (frappe/model/document.py) solo se omite
		bajo `frappe.flags.in_import/in_patch/in_install`; NO bajo `in_test`, así
		que las 2 Notification SÍ se evalúan aquí.

		Se verifica contra *Communication* y no contra *Email Queue*: se
		comprobó en la práctica (falla real de CI en un site sin ningún Email
		Account configurado) que `frappe.sendmail` solo llega a insertar en
		Email Queue si antes logra resolver una cuenta de correo saliente
		(`EmailAccount.find_outgoing(_raise_error=True)`,
		frappe/email/doctype/email_account/email_account.py:384-410) y arma el
		mensaje sin error; si eso falla, `QueueBuilder.as_dict` atrapa
		`InvalidEmailAddressError` y descarta la fila en silencio
		(frappe/email/doctype/email_queue/email_queue.py:820-838). El
		`Communication` en cambio se crea ANTES de ese intento, con
		`send_email=False`, y no depende de que exista una cuenta de correo
		(`frappe/core/doctype/communication/email.py:149-173`, `_make`,
		invocada desde `Notification.send_an_email`). Por eso es la señal
		correcta y estable para verificar aquí, sin navegador ni depender de
		infraestructura de correo del entorno.
		"""
		doc = self.make_consulta(consultado_a=TEST_USER_EMAIL)

		comunicacion_al_crear = frappe.db.exists(
			"Communication",
			{
				"reference_doctype": "Consulta Normativa",
				"reference_name": doc.name,
				"communication_type": "Automated Message",
			},
		)
		self.assertTrue(
			comunicacion_al_crear,
			"Se esperaba una Communication por la Notification 'New' hacia consultado_a",
		)

		# La Notification (b) envía al owner del documento. En este test el owner
		# real es "Administrator" (usuario de los tests), que no es un correo
		# válido, así que el destinatario se resolvería vacío y no probaría nada.
		# Se fuerza un owner con correo válido para poder verificar el envío.
		frappe.db.set_value("Consulta Normativa", doc.name, "owner", TEST_USER_EMAIL)
		doc.reload()

		doc.estado = "Respondida"
		doc.save(ignore_permissions=True)

		total_comunicaciones = frappe.db.count(
			"Communication",
			{
				"reference_doctype": "Consulta Normativa",
				"reference_name": doc.name,
				"communication_type": "Automated Message",
			},
		)
		self.assertGreaterEqual(
			total_comunicaciones,
			2,
			"Se esperaba una segunda Communication por la Notification 'Value Change' al owner",
		)
