# CoApp — *Colombia App*

**Cumplimiento colombiano para ERPNext** — CO es Colombia (ISO 3166-1).

CoApp es una aplicación pública de cumplimiento normativo colombiano construida sobre Frappe/ERPNext.

## Principio del proyecto

Toda funcionalidad cita la norma colombiana que la justifica (el *qué*) y el mecanismo canónico de Frappe/ERPNext que la implementa (el *cómo*). Lo que no puede citar ninguna de las dos fuentes, no se construye.

## Qué es

El primer módulo, **Gestión Normativa**, proporciona:

- Guías de punto de uso en formularios de ERPNext
- Registro formal de consultas al contador
- Vigencias documentales (snapshots firmados con hash) de documentos normativos

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

Este software no constituye asesoría contable ni tributaria. Toda regla debe verificarse contra la norma citada y con un profesional competente en la materia.

## Privacidad

CoApp, por sí misma, no envía datos a ningún servicio externo. Este compromiso cubre exclusivamente el código de esta app; no puede extenderse a Frappe, ERPNext ni a otras dependencias, que están fuera de su alcance.

## Mantenimiento

Mantenida por VIDAL & ASTUDILLO para su propia operación. Las contribuciones son bienvenidas; no se garantizan tiempos de respuesta.

## English

CoApp is a Colombian regulatory compliance application for Frappe/ERPNext. It provides accounting policy guidance, consultant inquiry logs, and regulatory document snapshots. Under active development. See CONTRIBUTING.md for contribution guidelines.

---

Copyright (C) 2026 VIDAL & ASTUDILLO Ltda — Licencia GPL-3.0-or-later. Autores: ver historial de git y página de contribuidores.
