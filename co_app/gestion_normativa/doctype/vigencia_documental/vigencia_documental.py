# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

import hashlib

import frappe
from frappe import _
from frappe.model.document import Document


class VigenciaDocumental(Document):
	def before_submit(self):
		self.hash_sha256 = self.get_pdf_hash()

	def get_pdf_hash(self):
		"""Calcula el SHA-256 del contenido del archivo adjunto en `pdf_firmado`.

		Usa la API canónica de Frappe para leer el contenido de un documento
		File a partir de su `file_url` (cubre tanto archivos públicos como
		privados): `frappe.get_doc("File", {"file_url": ...}).get_content()`.
		"""
		try:
			file_doc = frappe.get_doc("File", {"file_url": self.pdf_firmado})
			content = file_doc.get_content()
		except Exception:
			frappe.throw(
				_(
					"No fue posible leer el archivo adjunto en «PDF firmado». Verifique que el "
					"archivo exista y sea accesible antes de validar esta Vigencia Documental."
				)
			)

		if isinstance(content, str):
			content = content.encode("utf-8")

		return hashlib.sha256(content).hexdigest()

	def on_cancel(self):
		frappe.throw(
			_(
				"Una Vigencia Documental validada es inmutable: no puede cancelarse ni "
				"corregirse (amend). Si necesita registrar un cambio, cree una nueva "
				"Vigencia Documental."
			)
		)
