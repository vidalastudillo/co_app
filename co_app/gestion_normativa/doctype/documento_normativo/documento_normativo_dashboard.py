# Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and Contributors
# See license.txt

from frappe import _


def get_data():
	return {
		"fieldname": "documento_normativo",
		"transactions": [
			{"label": _("Vigencias"), "items": ["Vigencia Documental"]},
		],
	}
