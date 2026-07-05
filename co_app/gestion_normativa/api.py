# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

import frappe

CACHE_KEY = "co_app_pautas_de_uso"


@frappe.whitelist()
def get_pautas():
	"""Pautas de Uso activas, agrupadas por `doctype_destino`.

	Cada pauta trae sus referencias ya compuestas: por cada renglón de
	`referencias` que apunte a un Documento Normativo, se resuelve
	{label, url, seccion, nota} — la URL sale SIEMPRE del Documento Normativo
	(única copia), nunca se guarda en la Pauta.

	Cacheado con `frappe.cache()` (ver patrón en
	`erpnext.accounts.doctype.fiscal_year` / `hrms.hr.doctype.leave_type`).
	Invalidado desde los controladores de Pauta de Uso (`on_update`,
	`on_trash`) y de Documento Normativo (`on_update`): cambiar la URL de un
	Documento Normativo debe reflejarse en los enlaces sin tocar la Pauta.
	"""
	return frappe.cache().get_value(CACHE_KEY, generator=_build_pautas_by_doctype)


def clear_pautas_cache():
	frappe.cache().delete_value(CACHE_KEY)


def _build_pautas_by_doctype():
	pautas = frappe.get_all(
		"Pauta de Uso",
		filters={"activo": 1},
		fields=["name", "doctype_destino", "titulo", "texto", "condicion", "company"],
	)

	pautas_by_doctype = {}
	for pauta in pautas:
		pautas_by_doctype.setdefault(pauta.doctype_destino, []).append(
			{
				"titulo": pauta.titulo,
				"texto": pauta.texto,
				"condicion": pauta.condicion,
				"company": pauta.company,
				"referencias": _get_referencias_resueltas(pauta.name),
			}
		)

	return pautas_by_doctype


def _get_referencias_resueltas(pauta_name):
	"""Referencias de una Pauta de Uso que apuntan a un Documento Normativo.

	La tabla hija `Referencia Normativa` es genérica (Dynamic Link a cualquier
	DocType); en Pauta de Uso, solo tiene sentido de surfacing la que apunta a
	Documento Normativo (de ahí sale la URL). Renglones a otro DocType se
	ignoran aquí (no aplica a este caso de uso).
	"""
	filas = frappe.get_all(
		"Referencia Normativa",
		filters={"parenttype": "Pauta de Uso", "parent": pauta_name, "documento_tipo": "Documento Normativo"},
		fields=["documento", "seccion", "nota"],
		order_by="idx asc",
	)

	referencias = []
	for fila in filas:
		if not fila.documento:
			continue
		documento = frappe.db.get_value(
			"Documento Normativo", fila.documento, ["nombre", "url"], as_dict=True
		)
		if not documento:
			continue
		referencias.append(
			{
				"label": documento.nombre,
				"url": documento.url,
				"seccion": fila.seccion,
				"nota": fila.nota,
			}
		)

	return referencias
