// Copyright (c) 2026, VIDAL & ASTUDILLO Ltda and contributors
// For license information, please see license.txt

// Surfacing de "Pauta de Uso" (spec §Surfacing de pautas / incremento 3):
// al cargar el Desk se llama una única vez el método whitelisted
// `co_app.gestion_normativa.api.get_pautas` (cacheado server-side) y, por
// cada doctype con pautas activas, se registra un
// `frappe.ui.form.on(doctype, "refresh", ...)` que evalúa la condición de
// cada pauta y, si aplica, la muestra con `frm.set_intro()`.
//
// La lógica de evaluación se expone en el namespace `co_app.pautas` para que
// el cliente script de Pauta de Uso (botón "Probar condición") la reutilice
// sin duplicarla.

frappe.provide("co_app.pautas");

// Reutiliza el MISMO mecanismo que Frappe usa para evaluar `depends_on`:
// Layout.evaluate_depends_on_value en
// frappe/public/js/frappe/form/layout.js (rama "eval:"), que llama
// `frappe.utils.eval(expression, { doc, parent })`. Condición vacía = aplica
// siempre. No se inventa un eval propio.
co_app.pautas.evaluate_condicion = function (condicion, doc) {
	if (!condicion || !condicion.trim()) {
		return true;
	}

	let expression = condicion.trim();
	if (expression.startsWith("eval:")) {
		expression = expression.slice(5);
	}

	// Un error de sintaxis debe propagarse: cada llamador decide cómo
	// tratarlo (refresh: try/catch silencioso + console.warn; "Probar
	// condición": msgprint con el detalle).
	return !!frappe.utils.eval(expression, { doc });
};

// Chequeo de sintaxis de una condición SIN ejecutarla: devuelve null si la
// condición está vacía o parsea bien, o el Error de sintaxis si no. Usa el
// constructor de Function, que PARSEA el cuerpo sin ejecutarlo (parseo puro,
// no evaluación: jamás toca datos ni ejecuta la expresión). Lo usa el
// handler `validate` de Pauta de Uso para bloquear el guardado de una
// condición rota en la autoría, donde el error sí es accionable.
co_app.pautas.parse_error = function (condicion) {
	if (!condicion || !condicion.trim()) {
		return null;
	}

	let expression = condicion.trim();
	if (expression.startsWith("eval:")) {
		expression = expression.slice(5);
	}

	try {
		new Function("doc", "return (" + expression + ")");
		return null;
	} catch (e) {
		return e;
	}
};

// company vacía en la pauta = aplica a todas las compañías. Con company, solo
// aplica si `doc.company` coincide; si el doctype destino no tiene campo
// company, `doc.company` es undefined y la pauta con company nunca aplica.
co_app.pautas.company_aplica = function (pauta_company, doc) {
	if (!pauta_company) {
		return true;
	}
	return !!doc && doc.company === pauta_company;
};

// Condición completa de aplicación de una pauta: filtro de company + eval de
// `condicion`. Puede lanzar (error de sintaxis en `condicion`); el llamador
// decide cómo tratarlo.
co_app.pautas.pauta_aplica = function (pauta, doc) {
	if (!co_app.pautas.company_aplica(pauta.company, doc)) {
		return false;
	}
	return co_app.pautas.evaluate_condicion(pauta.condicion, doc);
};

// Arma el HTML de una pauta aplicable: texto en markdown + enlaces de sus
// referencias (URL del Documento Normativo + "§sección" como texto del
// enlace, target _blank). Ver Form API (`frappe.markdown`, `set_intro`) en
// docs/referencias.md.
co_app.pautas.build_pauta_html = function (pauta) {
	let html = `<div class="co-app-pauta">${frappe.markdown(pauta.texto || "")}`;

	const referencias = pauta.referencias || [];
	if (referencias.length) {
		const enlaces = referencias
			.map((ref) => {
				const texto_enlace = ref.seccion ? `${ref.label} §${ref.seccion}` : ref.label;
				return (
					`<a href="${frappe.utils.escape_html(ref.url)}" target="_blank" ` +
					`rel="noopener noreferrer">${frappe.utils.escape_html(texto_enlace)}</a>`
				);
			})
			.join(" &middot; ");
		html += `<div class="co-app-pauta-referencias">${enlaces}</div>`;
	}

	html += "</div>";
	return html;
};

function co_app_mostrar_pautas(frm, pautas) {
	// set_intro(txt, color) en esta versión de Frappe reemplaza el mensaje
	// completo del formulario (frappe/public/js/frappe/form/form.js →
	// dashboard.set_headline_alert → layout.show_message); no admite un
	// parámetro append=true. Para mostrar varias pautas aplicables a la vez
	// se acumulan todas en un único HTML y se llama set_intro() una sola vez
	// (declarado como desviación del brief en el informe del PR).
	const aplicables = [];

	pautas.forEach((pauta) => {
		try {
			if (co_app.pautas.pauta_aplica(pauta, frm.doc)) {
				aplicables.push(pauta);
			}
		} catch (e) {
			console.warn(
				`co_app: la Pauta de Uso "${pauta.titulo}" tiene una condición con error de sintaxis y no se evaluó.`,
				e
			);
		}
	});

	if (!aplicables.length) {
		return;
	}

	const html = aplicables.map(co_app.pautas.build_pauta_html).join("");
	frm.set_intro(html, "blue");
}

frappe.call({ method: "co_app.gestion_normativa.api.get_pautas" }).then((r) => {
	const pautas_by_doctype = r.message || {};

	Object.keys(pautas_by_doctype).forEach((doctype) => {
		frappe.ui.form.on(doctype, {
			refresh(frm) {
				co_app_mostrar_pautas(frm, pautas_by_doctype[doctype] || []);
			},
		});
	});
});
