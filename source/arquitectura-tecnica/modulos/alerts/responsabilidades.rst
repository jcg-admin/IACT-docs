.. _arq-mod-006-responsabilidades:

================================================
ARQ_MOD_006 — Responsabilidades del Modulo
================================================


PUEDE Hacer
===========

.. list-table::
 :widths: 55 20 25
 :header-rows: 1

 * - Responsabilidad
   - UC Relacionado
   - CNST
 * - Crear configuracion de alerta operativa
   - UC_036
   - -
 * - Definir tipo (THRESHOLD/ANOMALY/TREND)
   - UC_036
   - -
 * - Definir severidad y destinatarios
   - UC_036
   - -
 * - Enviar notificacion a buzon interno
   - UC_037
   - CNST_001
 * - Listar bandeja de notificaciones
   - UC_038
   - -
 * - Filtrar por severidad, tipo, estado
   - UC_038
   - -
 * - Aplicar snooze (1h, 8h, 24h, personalizado)
   - UC_039
   - -
 * - Confirmar/cerrar alerta atendida
   - UC_040
   - -

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**:

- **Enviar email**

  - Viola restriccion critica CNST_001
  - Todo va por InternalMessage (buzon interno)

- **Consultar BD IVR directamente**

  - Debe usar datos de BD Analytics (ya transformados)
  - Responsabilidad de → :ref:`arq-mod-004`

- **Implementar logica de permisos**

  - Ejemplo: "Solo admin ve estas alertas"
  - Debe pasar por → :ref:`arq-mod-003`

- **Generar reportes de negocio**

  - Responsabilidad de → :ref:`arq-mod-005`
