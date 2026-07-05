# Vigencia Documental

**Para qué sirve.** Snapshot inmutable de una versión certificada de un documento normativo en una fecha específica. Registra el PDF escaneado del documento firmado e integra automáticamente su huella digital (hash SHA-256), certificando que no ha sido alterado. Una vez validada, solo administradores pueden enmendar (creando una nueva vigencia) o cancelar (histórico, sin poder borrarse).

**Por qué.** [Ley 527 de 1999, arts. 8–9](../referencias.md). La integridad de documentos electrónicos requiere registro inmutable y corrección con rastro: si un acta es incorrecta, se cancela (queda visible) y se enmienda (crea una nueva). Jamás puede borrarse sin dejar huella, porque destruiría el rastro probatorio.

**Cómo.** Frappe [Submittable DocType](../referencias.md) con estados Borrador/Enviado/Cancelado, integrado con [hooks server (`before_submit`, `on_trash`)](../referencias.md) para calcular hash y bloquear borrado de documentos no-borrador. [Track Changes](../referencias.md) registra automáticamente cada enmienda. Los campos `cancel` y `amend` están restringidos a System Manager por seguridad operativa.

**Límites.** Depende de disciplina humana: sin vigencia validada, no hay versión certificada (la norma lo requiere, no lo fuerza el sistema). El acta cancelada queda visible pero inmóvil (no se puede borrar ni editar más). La fecha de vigencia puede ser retroactiva (válido según la norma), pero requiere cuidado operativo para evitar inconsistencias. El nombre de la versión, una vez validado, no se renumera.
