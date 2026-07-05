# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

import frappe
from frappe import _
from frappe.desk.form import assign_to
from frappe.model.document import Document
from frappe.utils import today


class ConsultaNormativa(Document):
	def validate(self):
		self.set_fecha_respuesta_on_transition()

	def set_fecha_respuesta_on_transition(self):
		"""Registra `fecha_respuesta` cuando el estado TRANSICIONA a "Respondida".

		Detecta la transición (no la mera presencia del estado) comparando contra
		`get_doc_before_save()`, siguiendo el patrón canónico de esta app para
		lógica de snapshot/estado (ver `vigencia_documental.py`). Nunca sobrescribe
		un valor ya existente ni lo limpia si el estado sale de "Respondida".
		"""
		doc_before_save = self.get_doc_before_save()
		estado_anterior = doc_before_save.estado if doc_before_save else None

		transiciona_a_respondida = self.estado == "Respondida" and estado_anterior != "Respondida"

		if transiciona_a_respondida and not self.fecha_respuesta:
			self.fecha_respuesta = today()

	def after_insert(self):
		"""Asigna la consulta al usuario de `consultado_a`, si se indicó uno.

		Usa la API canónica `frappe.desk.form.assign_to.add`, que crea el ToDo y
		dispara el aviso nativo de asignación (ver `frappe/desk/form/assign_to.py`).
		"""
		if not self.consultado_a:
			return

		assign_to.add(
			{
				"assign_to": [self.consultado_a],
				"doctype": self.doctype,
				"name": self.name,
				"description": _("Consulta normativa asignada: {0}").format(self.titulo),
			}
		)
