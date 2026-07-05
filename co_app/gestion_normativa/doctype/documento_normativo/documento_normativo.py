# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

from frappe.model.document import Document

from co_app.gestion_normativa.api import clear_pautas_cache


class DocumentoNormativo(Document):
	def on_update(self):
		# Criterio de aceptación 2 (spec): cambiar la URL de un Documento
		# Normativo debe reflejarse en los enlaces de Pauta de Uso sin tocar
		# ningún otro registro. Un cache que retenga URLs viejas lo violaría.
		clear_pautas_cache()
