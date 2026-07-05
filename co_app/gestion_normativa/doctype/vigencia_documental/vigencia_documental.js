// Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vigencia Documental", {
	before_cancel(frm) {
		return new Promise((resolve) => {
			const d = frappe.warn(
				__("¿Cancelar esta acta de forma permanente?"),
				__(
					"El acta cancelada se conservará como parte del rastro documental y no podrá eliminarse. Podrá enmendarla para crear la versión corregida."
				),
				() => resolve(),
				__("Continuar"),
				false
			);

			// frappe.warn no expone un callback de rechazo; d.onhide y
			// d.primary_action_fulfilled son genéricos de frappe.ui.Dialog
			// (dialog.js:105,186,251) y replican la detección de cierre-sin-
			// proceder que usa frappe.confirm internamente.
			d.onhide = () => {
				if (!d.primary_action_fulfilled) {
					frappe.validated = false;
					resolve();
				}
			};
		});
	},
});
