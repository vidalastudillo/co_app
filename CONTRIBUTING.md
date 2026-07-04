# Contribuyendo a CoApp

Al contribuir, licencias tu aporte bajo GPL-3.0-or-later y conservas tu copyright. Aplicamos el modelo inbound=outbound, sin CLA.

## Criterio: Doble cita

Todo PR que agregue o cambie comportamiento debe citar:

1. **La norma colombiana** que lo justifica, con enlace oficial (p.ej., norma DIAN, resolución fiscal, decreto)
2. **La API/patrón canónico de Frappe/ERPNext** usado, con referencia a la documentación

PRs sin citas no se revisan.

## Convenciones de código

- **Identificadores** (variables, funciones, clases): inglés
- **Interfaz de usuario** (labels, help text, mensajes): español con tildes
- Traducciones: archivo `translations/es.csv`

## Prohibiciones

- `import erpnext` — evita acoplamiento directo; usa datos, hooks, fixtures
- Datos reales (NITs, nombres de clientes, URLs internas)
- Datos de prueba deben ser siempre sintéticos

## Licencia

GPL-3.0-or-later. Ver LICENSE.
