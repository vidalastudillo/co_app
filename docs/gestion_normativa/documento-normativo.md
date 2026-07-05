# Documento Normativo

**Para qué sirve.** Registro centralizado de documentos que contienen normas — manuales internos aprobados y referencias externas a normas de terceros. Permite indirección: cambiar la URL de un documento actualiza automáticamente todos los enlaces que lo citan, sin tocar otros registros.

**Por qué.** Decisión de diseño del proyecto. La indirección de URLs es crítica para migración futura de fuentes (p. ej. de Google Docs a Frappe Drive, o cambio de proveedor): el identificador durable es documento + sección canónica ("§11.2"), no anchor. Guardar la URL en un único lugar central reduce riesgo de inconsistencia.

**Cómo.** DocType simple con un campo URL de única copia. Las pautas y consultas referencian el Documento Normativo, no su URL; Referencia Normativa (tabla hija) usa Dynamic Link para apuntar a cualquier documento origen. Ver [Frappe — DocType basics](../referencias.md).

**Límites.** La URL es única por documento: no se pueden publicar múltiples versiones (eso lo resuelve [Vigencia Documental](vigencia-documental.md)). Documentos externos se registran como referencia sola, sin versionado en el ERP. Requiere disciplina humana: cambiar una URL afecta todas las citas inmediatamente, sin historial de cambio de fuente.
