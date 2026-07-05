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

	def test_notificaciones_encolan_correo(self):
		"""Pieza 3 / pieza 7(e): verificación real, no simulada.

		`Document.run_notifications` (frappe/model/document.py) solo se omite
		bajo `frappe.flags.in_import/in_patch/in_install`; NO bajo `in_test`.
		El envío SMTP se omite en test (`frappe.flags.in_test`, ver
		frappe/email/doctype/email_queue/email_queue.py líneas ~180-189), pero
		la fila en *Email Queue* se inserta de forma síncrona igualmente
		(`frappe.sendmail` con `delayed=True` solo difiere el envío, no el
		encolamiento). Por eso esto es verificable aquí, sin navegador.
		"""
		doc = self.make_consulta(consultado_a=TEST_USER_EMAIL)

		encolado_al_crear = frappe.db.exists(
			"Email Queue", {"reference_doctype": "Consulta Normativa", "reference_name": doc.name}
		)
		self.assertTrue(
			encolado_al_crear,
			"Se esperaba una fila en Email Queue por la Notification 'New' hacia consultado_a",
		)

		# La Notification (b) envía al owner del documento. En este test el owner
		# real es "Administrator" (usuario de los tests), que no es un correo
		# válido, así que el destinatario se resolvería vacío y no probaría nada.
		# Se fuerza un owner con correo válido para poder verificar el encolado.
		frappe.db.set_value("Consulta Normativa", doc.name, "owner", TEST_USER_EMAIL)
		doc.reload()

		doc.estado = "Respondida"
		doc.save(ignore_permissions=True)

		total_encolados = frappe.db.count(
			"Email Queue", {"reference_doctype": "Consulta Normativa", "reference_name": doc.name}
		)
		self.assertGreaterEqual(
			total_encolados,
			2,
			"Se esperaba una segunda fila en Email Queue por la Notification 'Value Change' al owner",
		)
