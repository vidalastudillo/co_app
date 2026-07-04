# Contribuir a CoApp

Al contribuir, el aporte queda licenciado bajo GPL-3.0-or-later y quien contribuye conserva su copyright. Se aplica el modelo inbound=outbound, sin CLA.

## Criterio: doble cita

Todo PR que agregue o cambie comportamiento debe citar:

1. **La norma colombiana** que lo justifica, con enlace oficial (ley, decreto, resolución, concepto DIAN, sección NIIF)
2. **La API o patrón canónico de Frappe/ERPNext** usado, con referencia a la documentación

Los PR sin citas no se revisan.

## Convenciones de código

- **Identificadores** (variables, funciones, clases): inglés
- **Interfaz de usuario** (labels, textos de ayuda, mensajes): español con tildes
- Traducciones: archivo `translations/es.csv`
- Documentación y mensajes en registro impersonal (sin tuteo)

## Prohibiciones

- **`import erpnext`**: los internos de ERPNext no son API pública y cambian entre versiones sin garantía de compatibilidad; además, sin imports la app funciona en cualquier bench Frappe, incluso sin ERPNext. El acoplamiento se hace únicamente por mecanismos estables y citables: datos (`frappe.get_doc`), hooks (`doc_events`) y fixtures. Excepción solo por decisión de diseño explícita y documentada.
- **Datos reales** (NITs, nombres de clientes, URLs internas): los datos de prueba deben ser siempre sintéticos.

## Licencia

GPL-3.0-or-later. Ver `license.txt`.
