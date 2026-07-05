# Pauta de Uso

**Para qué sirve.** Guía condicional de punto de uso: muestra automáticamente (banner `set_intro`) un texto y sus enlaces normativos en el formulario del DocType destino cuando se cumple una condición opcional, sin que el usuario tenga que ir a buscarla. El botón «Probar condición» permite verificar contra un documento real antes de activarla.

**Por qué.** Decisión de diseño del proyecto: guía en el punto de uso, no un documento aparte que nadie consulta. El antecedente descartado, IPUSUI (`va_app/va_dian/page/guia_ipusui/`), fallaba por ser un destino (Page de workspace) al que había que ir a buscar; el patrón correcto ya existía en `va_app/public/js/dian_related_document_link.js` (UI condicionada a datos vía hook de `refresh`). Pauta de Uso generaliza ese patrón a cualquier doctype y cualquier condición.

**Cómo.** [`co_app.gestion_normativa.api.get_pautas`](../referencias.md) (whitelisted, cacheado con `frappe.cache()`) agrupa las pautas activas por doctype y resuelve sus referencias — la URL sale siempre de [Documento Normativo](documento-normativo.md), nunca se guarda en la pauta. El cache se invalida al editar/borrar la Pauta y también al editar el Documento Normativo referenciado (si no, cambiar su URL no se vería reflejado). Un bundle ([asset bundling](../referencias.md) vía `app_include_js`) llama esa API una vez al cargar el Desk y registra `frappe.ui.form.on(doctype, "refresh", ...)` por cada doctype con pautas. La condición usa sintaxis `eval:` evaluada con el MISMO mecanismo que Frappe usa para `depends_on` (`Layout.evaluate_depends_on_value`, `frappe/public/js/frappe/form/layout.js`) — no un eval propio. Error de sintaxis: try/catch silencioso + `console.warn`; el formulario queda intacto. El botón «Probar condición» (client script del propio DocType) reutiliza la misma función (`co_app.pautas.pauta_aplica`, expuesta por el bundle) contra un documento real elegido con Dynamic Link, y llama a [`frappe.client.get`](../referencias.md) para traerlo.

Recetario del campo «Condición» (sintaxis `eval:`, con `doc` en alcance):
- Vacía → siempre aplica.
- Campo vale X → `eval:doc.origen == "Externo"`
- Campo no vacío → `eval:doc.remarks`
- Algún renglón de tabla hija cumple → `eval:doc.items.length && doc.items.filter(i => i.item_code == "SERV-IPUSUI").length`
- Combinación `&&` / `||` → `eval:doc.docstatus == 1 && doc.company == "Mi Empresa S.A.S."`

**Límites.** v1 evalúa solo en `refresh`, no campo a campo ni por renglón de tabla hija: un cambio en tiempo real dentro del formulario no reevalúa la pauta hasta el próximo refresh (documentado, no se "arregla" en este incremento). `set_intro()` en esta versión de Frappe reemplaza el mensaje del formulario completo (no admite `append=true`): varias pautas aplicables se combinan en un único HTML antes de una sola llamada; un intro puesto por otro script en el mismo refresh puede sobrescribirse o ser sobrescrito. Filtro por `company`: vacío = todas; si el doctype destino no tiene campo `company`, una pauta con `company` nunca aplica.
