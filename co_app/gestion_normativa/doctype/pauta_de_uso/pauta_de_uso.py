# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

from frappe.model.document import Document

from co_app.gestion_normativa.api import clear_pautas_cache


class PautadeUso(Document):
	def on_update(self):
		clear_pautas_cache()

	def on_trash(self):
		clear_pautas_cache()
