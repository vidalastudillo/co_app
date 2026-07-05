# Referencias

Tabla de normas colombianas y documentación técnica citada.

| Identificador | URL | Descripción |
|---|---|---|
| Ley 527 de 1999, arts. 8–9 | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=4276 | Norma colombiana que fundamenta la integridad de documentos electrónicos y corrección trazable (Gestor Normativo de Función Pública; suin-juriscol es fuente alternativa). |
| Frappe v15 — Submittable DocTypes | https://docs.frappe.io/framework/user/en/api/document | Mecanismo de DocTypes con estados (Borrador/Enviado/Cancelado) y control de versiones mediante `submit`, `cancel`, `amend` (docstatus). |
| Frappe v15 — Hooks y eventos server | https://docs.frappe.io/framework/user/en/python-api/hooks | Patrones `before_submit`, `on_trash`, `after_insert`, `on_update` para lógica automática ligada al ciclo de vida del documento. |
| Frappe v15 — Dynamic Link field | https://docs.frappe.io/framework/user/en/basics/doctypes/fieldtypes | Campo que vincula a un registro cuyo tipo se define dinámicamente en otro campo. |
| Frappe v15 — Text Editor field | https://docs.frappe.io/framework/user/en/basics/doctypes/fieldtypes | Campo de edición enriquecida (WYSIWYG) para prosa larga. |
| Frappe v15 — Track Changes | https://docs.frappe.io/erpnext/user/manual/en/document-versioning | Mecanismo nativo de registro de cambios y versiones de un DocType. |
| Frappe v15 — Notifications | https://docs.frappe.io/erpnext/user/manual/en/notifications | Sistema de notificaciones automáticas por condición (email, SMS, Slack). |
| Frappe v15 — Auto Email Report | https://docs.frappe.io/erpnext/user/manual/en/auto-email-reports | Envío automático recurrente de reportes vía email según condiciones (horario, datos). |
| Frappe v15 — ToDo y assign | https://docs.frappe.io/erpnext/user/manual/en/assignment | Creación automática de tareas asignadas desde scripts server (`doc.add_assignment`). |
| Frappe v15 — Form API (`set_intro`) | https://docs.frappe.io/framework/user/en/api/form | API de formulario client-side: `set_intro`, `set_df_property`, `add_custom_button`, etc. |
| Frappe v15 — Asset bundling | https://docs.frappe.io/framework/user/en/basics/asset-bundling | Convención de bundles JS/CSS (`*.bundle.js`) cargados vía `app_include_js`. |
| Frappe v15 — Llamadas whitelisted desde JS | https://docs.frappe.io/framework/user/en/guides/basics/frappe_ajax_call | `frappe.call`/`frappe.whitelist()` para invocar métodos Python desde el cliente. |
