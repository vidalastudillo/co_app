# Consulta Normativa

**Para qué sirve.** Solicitud formal de orientación sobre una norma o política, registrada en el ERP con timeline completo, respuesta consolidada y referencias normativas. Genera automáticamente un recordatorio al asesor asignado y notifica por email cuando hay respuesta. Sin Workflow: los estados (Abierta, Respondida, Aplicada, Descartada) reflejan situación sin forzar transiciones.

**Por qué.** Decisión de diseño del proyecto. No se reutilizó Support/Issue porque ese módulo cerraría por sí solo las consultas respondidas (su `auto_close_tickets`), y Help Article no existe en v15. Toda la maquinaria necesaria —timeline, notificaciones, [track_changes](../referencias.md)— la provee Frappe base para cualquier DocType.

**Cómo.** DocType regular con [Text Editor](../referencias.md) para pregunta y respuesta, [Track Changes](../referencias.md) para historial de versiones, campo `estado` como Select (no workflow), [after_insert hook](../referencias.md) que crea un ToDo automático, [Notifications](../referencias.md) por email (fixtures), y [Auto Email Report](../referencias.md) semanal de consultas abiertas. [Referencia Normativa](referencia-normativa.md) vincula la consulta a secciones de normas.

**Límites.** Sin gates de rol en transiciones de estado: disciplina manual. El timeline vive en comentarios nativos, no como entradas modeladas (conversación no se busca por índice en el ERP). Los recordatorios automáticos (email semanal) dependen de Email Account configurada en producción. Evaluación de "está respondida" es manual, no automática por condición.
