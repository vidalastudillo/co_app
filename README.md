# CoApp — *Colombia App*

**Cumplimiento colombiano para ERPNext**

CoApp (Colombia App) es una aplicación pública de cumplimiento normativo colombiano construida sobre Frappe/ERPNext. "CO" es el código de país de Colombia (ccTLD `.co`).

## Qué es

CoApp implementa guías de punto de uso en formularios, registro formal de consultas al contador, y actas de vigencia (snapshots firmados con hash) de documentos normativos colombianos.

El primer módulo, **Politicas Contables**, proporciona:

- Guías de punto de uso en formularios de ERPNext
- Registro formal de consultas al contador
- Actas de vigencia (snapshots firmados con hash) de normas

## Estado

En desarrollo activo. Aún sin release.

## Compatibilidad

- Frappe v15 y v16
- ERPNext v15 y v16

## Instalación

```bash
bench get-app https://github.com/vidalastudillo/co_app
bench --site <site> install-app co_app
```

## Descargo de responsabilidad

Este software no constituye asesoría contable ni tributaria; verifique toda regla con la norma citada y con su asesor.

## Privacidad

Esta app no envía datos a ningún servicio externo.

## Mantenimiento

Mantenida por VIDAL & ASTUDILLO para su propia operación. Contribuciones bienvenidas; no garantizamos tiempos de respuesta.

## Principio del proyecto

Toda funcionalidad cita la norma colombiana que la justifica (el *qué*) y el mecanismo canónico de Frappe/ERPNext que la implementa (el *cómo*).

## English

CoApp is a Colombian regulatory compliance application for Frappe/ERPNext. It provides accounting policy guidance, consultant inquiry logs, and regulatory document snapshots. Under active development. See CONTRIBUTING.md for contribution guidelines.

---

Copyright (C) 2026 VIDAL & ASTUDILLO Ltda — Licencia GPL-3.0-or-later. Autores: ver historial de git y página de contribuidores.
