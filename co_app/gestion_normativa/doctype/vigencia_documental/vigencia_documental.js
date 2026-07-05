// Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vigencia Documental", {
	refresh(frm) {
		frm.set_intro();

		if (frm.doc.docstatus === 1) {
			frm.set_intro(
				__(
					"Cancelar esta acta es permanente: quedará marcada como cancelada dentro del rastro documental y no podrá eliminarse. Podrá enmendarla para crear la versión corregida."
				),
				"orange"
			);
		} else if (frm.doc.docstatus === 2) {
			frm.set_intro(
				__(
					"Acta cancelada. Se conserva como parte del rastro documental y no puede eliminarse."
				),
				"blue"
			);
		}
	},
});
