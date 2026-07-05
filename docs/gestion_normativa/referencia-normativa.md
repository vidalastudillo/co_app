# Referencia Normativa

**Para qué sirve.** Vínculo entre cualquier documento (factura, consulta, acta) y una sección específica de un Documento Normativo. Permite rastrear qué normas respaldan cada decisión. Tabla hija compartida: puede embeberse en Consulta Normativa, Vigencia Documental, Sales Invoice, Purchase Invoice, Journal Entry.

**Por qué.** Decisión de diseño del proyecto. Los códigos de sección son inmutables (siguiendo el modelo del **Estatuto Tributario** colombiano: una sección insertada, p. ej. Art. 513-1, jamás se renumera). Esto permite que una cita "§11.2" siga válida aún si la estructura se reorganiza — buscar referencias por número afectado es entonces una consulta manual de integridad.

**Cómo.** Tabla hija con [Dynamic Link](../referencias.md) para apuntar a cualquier tipo de documento, campo `seccion` (Data, opcional) para código canónico (p. ej. "§11.2", "Art. 513-1", "Sección 10"), y campo `nota` para contexto. El [Dynamic Link](../referencias.md) permite que la misma tabla hija se reutilice en múltiples DocTypes padre sin duplicación. Dashboard "Connections" inverso en documentos citados (Sales Invoice, Purchase Invoice, Journal Entry).

**Límites.** El formato del código de sección es libre (Data field, sin validación): requiere convención y disciplina humana. Los dashboards inversos ("este documento es citado por...") son lectura pura, no pueden editar la referencia desde allá. No hay búsqueda full-text de referencias: las citas se rastrean por documento + sección, no por contenido normativo.
