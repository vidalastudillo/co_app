// Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pauta de Uso", {
	refresh(frm) {
		frm.add_custom_button(__("Probar condición"), () => co_app_probar_condicion(frm));
	},

	validate(frm) {
		// El error de sintaxis de la condición se atrapa EN LA AUTORÍA
		// (decisión sellada por JM): bloquea el guardado de la Pauta con
		// mensaje claro. El usuario del doctype destino nunca ve errores (el
		// console.warn del bundle en refresh se conserva tal cual).
		//
		// Guardia: si el bundle no está cargado (p. ej. bench sin reiniciar
		// tras cambiar hooks), NO se bloquea el guardado — un bundle ausente
		// no debe impedir guardar; la validación simplemente se omite.
		if (typeof co_app === "undefined" || !co_app.pautas) {
			return;
		}

		if (!frm.doc.condicion) {
			return;
		}

		const error = co_app.pautas.parse_error(frm.doc.condicion);
		if (error) {
			frappe.validated = false;
			frappe.msgprint(
				__(
					"La condición tiene un error de sintaxis y la pauta no puede guardarse: {0}<br>Consulte el recetario en la descripción del campo «Condición».",
					[frappe.utils.escape_html(error.message || String(error))]
				)
			);
		}
	},
});

function co_app_probar_condicion(frm) {
	// Guardia contra el bundle ausente: sin ella, co_app.pautas no existe y
	// el catch de abajo mostraría el engañoso "Error de sintaxis: co_app is
	// not defined".
	if (typeof co_app === "undefined" || !co_app.pautas) {
		frappe.msgprint(
			__(
				"El paquete de pautas no está cargado. Recargue el escritorio (Cmd/Ctrl+Shift+R) e intente de nuevo."
			)
		);
		return;
	}

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
