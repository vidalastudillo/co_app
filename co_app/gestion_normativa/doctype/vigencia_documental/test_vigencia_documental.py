# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

import hashlib
from io import BytesIO

import frappe
from frappe.tests.utils import FrappeTestCase
from pypdf import PdfWriter

test_ignore = ["Company"]


def make_synthetic_pdf_bytes():
	"""Genera un PDF mínimo válido en memoria, para usar como archivo de prueba.

	No se usan datos reales de la empresa ni de clientes: es contenido
	sintético, sin relación con documentos normativos reales.
	"""
	buffer = BytesIO()
	writer = PdfWriter()
	writer.add_blank_page(width=200, height=200)
	writer.write(buffer)
	return buffer.getvalue()


class TestVigenciaDocumental(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.documento = frappe.get_doc(
			{
				"doctype": "Documento Normativo",
				"nombre": "Manual de Pruebas - Vigencia Documental",
				"origen": "Interno",
				"url": "https://example.com/manual-de-pruebas",
			}
		).insert()

	def make_vigencia(self, version, fecha_vigencia, pdf_firmado="pendiente"):
		return frappe.get_doc(
			{
				"doctype": "Vigencia Documental",
				"documento_normativo": self.documento.name,
				"fecha_vigencia": fecha_vigencia,
				"version": version,
				"pdf_firmado": pdf_firmado,
			}
		).insert(ignore_mandatory=True)

	def attach_file(self, vigencia, content):
		return frappe.get_doc(
			{
				"doctype": "File",
				"file_name": f"{vigencia.name}.pdf",
				"attached_to_doctype": "Vigencia Documental",
				"attached_to_name": vigencia.name,
				"content": content,
			}
		).insert()

	def test_submit_calcula_hash_sha256(self):
		vigencia = self.make_vigencia("v1", "2026-01-01")
		contenido = make_synthetic_pdf_bytes()
		archivo = self.attach_file(vigencia, contenido)

		vigencia.pdf_firmado = archivo.file_url
		vigencia.save()
		vigencia.submit()

		self.assertEqual(vigencia.hash_sha256, hashlib.sha256(contenido).hexdigest())

	def test_submit_falla_si_archivo_no_existe(self):
		vigencia = self.make_vigencia(
			"v2",
			"2026-01-01",
			pdf_firmado="/private/files/archivo-inexistente-de-prueba.pdf",
		)

		self.assertRaises(frappe.ValidationError, vigencia.submit)

	def test_cancel_de_vigencia_validada_lanza_excepcion(self):
		vigencia = self.make_vigencia("v3", "2026-01-01")
		contenido = make_synthetic_pdf_bytes()
		archivo = self.attach_file(vigencia, contenido)
		vigencia.pdf_firmado = archivo.file_url
		vigencia.save()
		vigencia.submit()

		self.assertRaises(frappe.ValidationError, vigencia.cancel)

	def test_submit_permite_fecha_vigencia_retroactiva(self):
		vigencia = self.make_vigencia("v4", "2020-01-01")
		contenido = make_synthetic_pdf_bytes()
		archivo = self.attach_file(vigencia, contenido)
		vigencia.pdf_firmado = archivo.file_url
		vigencia.save()
		vigencia.submit()

		self.assertEqual(vigencia.docstatus, 1)
