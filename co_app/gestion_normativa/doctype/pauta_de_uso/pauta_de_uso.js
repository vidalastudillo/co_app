// Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pauta de Uso", {
	refresh(frm) {
		frm.add_custom_button(__("Probar condición"), () => co_app_probar_condicion(frm));
	},
});

function co_app_probar_condicion(frm) {
	if (!frm.doc.doctype_destino) {
		frappe.msgprint(__("Seleccione primero un «DocType destino»."));
		return;
	}

	const dialog = new frappe.ui.Dialog({
		title: __("Probar condición contra un documento real"),
		fields: [
			{
				fieldname: "documento",
				fieldtype: "Dynamic Link",
				label: __("Documento de {0}", [frm.doc.doctype_destino]),
				// Dynamic Link en un diálogo resuelve el DocType vía
				// `get_options` (frappe/public/js/frappe/form/controls/dynamic_link.js);
				// no necesita un campo auxiliar porque doctype_destino ya es fijo.
				get_options: () => frm.doc.doctype_destino,
				reqd: 1,
			},
		],
		primary_action_label: __("Probar"),
		primary_action: (values) => {
			frappe.call({
				// Método whitelisted canónico para leer un documento por
				// nombre (frappe.client.get). Ver docs/referencias.md.
				method: "frappe.client.get",
				args: { doctype: frm.doc.doctype_destino, name: values.documento },
				callback: (r) => {
					const target_doc = r.message;

					// Reutiliza la MISMA lógica de condición del bundle
					// (co_app.pautas, definida en pauta_de_uso.bundle.js) en
					// lugar de duplicar el eval aquí.
					try {
						const aplica = co_app.pautas.pauta_aplica(
							{ condicion: frm.doc.condicion, company: frm.doc.company },
							target_doc
						);
						frappe.msgprint(aplica ? __("Aplicaría") : __("No aplicaría"));
					} catch (e) {
						frappe.msgprint(__("Error de sintaxis: {0}", [e.message || e]));
					}
					dialog.hide();
				},
			});
		},
	});

	dialog.show();
}
