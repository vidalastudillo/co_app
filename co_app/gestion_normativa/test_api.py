# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

from co_app.gestion_normativa.api import clear_pautas_cache, get_pautas

# Doctype destino usado en las pautas de prueba: "ToDo" es un DocType core,
# siempre disponible, sin campo `company` — evita crear datos de facturación
# solo para probar el agrupamiento/cache de get_pautas. Nunca datos reales.
DOCTYPE_DESTINO_PRUEBA = "ToDo"


class TestGetPautas(FrappeTestCase):
	def setUp(self):
		# frappe.db.rollback() en tearDown deshace los inserts en BD, pero NO
		# el cache de redis (no forma parte de la transacción SQL): sin este
		# clear, un test siguiente leería el cache que dejó el anterior.
		clear_pautas_cache()
		self.sufijo = frappe.generate_hash(length=8)
		self.documento = frappe.get_doc(
			{
				"doctype": "Documento Normativo",
				"nombre": f"Manual sintetico de prueba {self.sufijo}",
				"origen": "Interno",
				"url": "https://example.com/manual-v1",
			}
		).insert(ignore_permissions=True)

	def tearDown(self):
		frappe.db.rollback()
		clear_pautas_cache()

	def make_pauta(self, **kwargs):
		data = {
			"doctype": "Pauta de Uso",
			"doctype_destino": DOCTYPE_DESTINO_PRUEBA,
			"titulo": f"Pauta sintetica {self.sufijo}",
			"texto": "Texto de prueba **en negrita**.",
			"activo": 1,
			"referencias": [
				{
					"documento_tipo": "Documento Normativo",
					"documento": self.documento.name,
					"seccion": "1.1",
					"nota": "Nota de prueba",
				}
			],
		}
		data.update(kwargs)
		return frappe.get_doc(data).insert(ignore_permissions=True)

	def test_agrupa_por_doctype_destino_y_excluye_inactivas(self):
		activa = self.make_pauta()
		inactiva = self.make_pauta(
			titulo=f"Pauta inactiva {self.sufijo}",
			activo=0,
		)

		pautas = get_pautas()

		self.assertIn(DOCTYPE_DESTINO_PRUEBA, pautas)
		titulos = [p["titulo"] for p in pautas[DOCTYPE_DESTINO_PRUEBA]]
		self.assertIn(activa.titulo, titulos)
		self.assertNotIn(inactiva.titulo, titulos)

	def test_referencias_incluyen_url_del_documento_normativo(self):
		pauta = self.make_pauta()

		pautas = get_pautas()
		encontrada = next(p for p in pautas[DOCTYPE_DESTINO_PRUEBA] if p["titulo"] == pauta.titulo)

		self.assertEqual(len(encontrada["referencias"]), 1)
		referencia = encontrada["referencias"][0]
		self.assertEqual(referencia["label"], self.documento.nombre)
		self.assertEqual(referencia["url"], "https://example.com/manual-v1")
		self.assertEqual(referencia["seccion"], "1.1")
		self.assertEqual(referencia["nota"], "Nota de prueba")

	def test_invalida_cache_al_actualizar_pauta(self):
		pauta = self.make_pauta()

		pautas = get_pautas()
		encontrada = next(p for p in pautas[DOCTYPE_DESTINO_PRUEBA] if p["titulo"] == pauta.titulo)
		self.assertEqual(encontrada["texto"], "Texto de prueba **en negrita**.")

		pauta.texto = "Texto actualizado tras editar la pauta."
		pauta.save(ignore_permissions=True)

		pautas_tras_editar = get_pautas()
		encontrada_tras_editar = next(
			p for p in pautas_tras_editar[DOCTYPE_DESTINO_PRUEBA] if p["titulo"] == pauta.titulo
		)
		self.assertEqual(encontrada_tras_editar["texto"], "Texto actualizado tras editar la pauta.")

	def test_invalida_cache_al_desactivar_o_borrar_pauta(self):
		pauta = self.make_pauta()
		get_pautas()  # llena el cache

		pauta.delete(ignore_permissions=True)

		pautas_tras_borrar = get_pautas()
		titulos = [p["titulo"] for p in pautas_tras_borrar.get(DOCTYPE_DESTINO_PRUEBA, [])]
		self.assertNotIn(pauta.titulo, titulos)

	def test_invalida_cache_al_actualizar_url_del_documento_normativo(self):
		"""Criterio de aceptación 2: cambiar la URL del Documento Normativo se
		refleja en los enlaces de la pauta sin tocar la Pauta de Uso."""
		pauta = self.make_pauta()

		pautas = get_pautas()  # llena el cache con la URL original
		encontrada = next(p for p in pautas[DOCTYPE_DESTINO_PRUEBA] if p["titulo"] == pauta.titulo)
		self.assertEqual(encontrada["referencias"][0]["url"], "https://example.com/manual-v1")

		self.documento.url = "https://example.com/manual-v2-migrado"
		self.documento.save(ignore_permissions=True)

		pautas_tras_cambio_url = get_pautas()
		encontrada_tras_cambio = next(
			p for p in pautas_tras_cambio_url[DOCTYPE_DESTINO_PRUEBA] if p["titulo"] == pauta.titulo
		)
		self.assertEqual(
			encontrada_tras_cambio["referencias"][0]["url"],
			"https://example.com/manual-v2-migrado",
		)
