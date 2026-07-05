# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

import hashlib
from io import BytesIO

import frappe
from frappe.tests.utils import FrappeTestCase
from pypdf import PdfWriter

test_ignore = ["Company"]


def make_synthetic_pdf_bytes(width=200, height=200):
	"""Genera un PDF mínimo válido en memoria, para usar como archivo de prueba.

	No se usan datos reales de la empresa ni de clientes: es contenido
	sintético, sin relación con documentos normativos reales. Las dimensiones
	de página son ajustables para poder generar dos PDF de contenido distinto
	(y por tanto de hash distinto) en un mismo test.
	"""
	buffer = BytesIO()
	writer = PdfWriter()
	writer.add_blank_page(width=width, height=height)
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

	def test_cancelar_vigencia_validada_esta_permitido(self):
		vigencia = self.make_vigencia("v3", "2026-01-01")
		contenido = make_synthetic_pdf_bytes()
		archivo = self.attach_file(vigencia, contenido)
		vigencia.pdf_firmado = archivo.file_url
		vigencia.save()
		vigencia.submit()
		hash_antes_de_cancelar = vigencia.hash_sha256

		vigencia.cancel()

		self.assertEqual(vigencia.docstatus, 2)
		self.assertEqual(vigencia.hash_sha256, hash_antes_de_cancelar)

	def test_submit_permite_fecha_vigencia_retroactiva(self):
		vigencia = self.make_vigencia("v4", "2020-01-01")
		contenido = make_synthetic_pdf_bytes()
		archivo = self.attach_file(vigencia, contenido)
		vigencia.pdf_firmado = archivo.file_url
		vigencia.save()
		vigencia.submit()

		self.assertEqual(vigencia.docstatus, 1)

	def test_eliminar_vigencia_validada_lanza_excepcion(self):
		vigencia = self.make_vigencia("v5", "2026-01-01")
		contenido = make_synthetic_pdf_bytes()
		archivo = self.attach_file(vigencia, contenido)
		vigencia.pdf_firmado = archivo.file_url
		vigencia.save()
		vigencia.submit()

		self.assertRaises(frappe.ValidationError, frappe.delete_doc, "Vigencia Documental", vigencia.name)

	def test_eliminar_vigencia_cancelada_lanza_excepcion(self):
		vigencia = self.make_vigencia("v6", "2026-01-01")
		contenido = make_synthetic_pdf_bytes()
		archivo = self.attach_file(vigencia, contenido)
		vigencia.pdf_firmado = archivo.file_url
		vigencia.save()
		vigencia.submit()
		vigencia.cancel()

		self.assertRaises(frappe.ValidationError, frappe.delete_doc, "Vigencia Documental", vigencia.name)

	def test_eliminar_borrador_esta_permitido(self):
		vigencia = self.make_vigencia("v7", "2026-01-01")

		frappe.delete_doc("Vigencia Documental", vigencia.name)

		self.assertFalse(frappe.db.exists("Vigencia Documental", vigencia.name))

	def test_flujo_de_enmienda_recalcula_hash_con_nuevo_pdf(self):
		vigencia = self.make_vigencia("v8", "2026-01-01")
		contenido_a = make_synthetic_pdf_bytes(width=200, height=200)
		archivo_a = self.attach_file(vigencia, contenido_a)
		vigencia.pdf_firmado = archivo_a.file_url
		vigencia.save()
		vigencia.submit()
		hash_de_la_cancelada = vigencia.hash_sha256

		vigencia.cancel()
		self.assertEqual(vigencia.docstatus, 2)

		# Patrón canónico de Frappe para enmendar un documento cancelado:
		# copiarlo con `frappe.copy_doc`, volver a docstatus 0 (borrador) y
		# apuntar `amended_from` a la vigencia cancelada.
		enmienda = frappe.copy_doc(vigencia)
		enmienda.docstatus = 0
		enmienda.amended_from = vigencia.name
		enmienda.insert()

		contenido_b = make_synthetic_pdf_bytes(width=300, height=300)
		self.assertNotEqual(contenido_a, contenido_b)
		archivo_b = self.attach_file(enmienda, contenido_b)
		enmienda.pdf_firmado = archivo_b.file_url
		enmienda.save()
		enmienda.submit()

		self.assertEqual(enmienda.amended_from, vigencia.name)
		self.assertEqual(enmienda.hash_sha256, hashlib.sha256(contenido_b).hexdigest())
		self.assertNotEqual(enmienda.hash_sha256, hash_de_la_cancelada)
