.. _arq-mod-007-responsabilidades:

================================================
ARQ_MOD_007 — Responsabilidades del Modulo
================================================


PUEDE Hacer
===========

.. list-table::
 :widths: 55 20 25
 :header-rows: 1

 * - Responsabilidad
   - UC Relacionado
   - CNST
 * - Registrar evento de auditoria
   - Transversal
   - CNST_009
 * - Consultar bitacora de auditoria
   - UC_070
   - CNST_009
 * - Filtrar por usuario, fecha, recurso
   - UC_071
   - -
 * - Exportar eventos a CSV/Excel
   - UC_072
   - CNST_007
 * - Generar reporte de cambios de permisos
   - UC_073
   - -
 * - Almacenar quien, que, cuando, desde donde
   - Transversal
   - CNST_009

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**:

- **Guardar stack traces o errores tecnicos**

  - Ejemplo: Tracebacks de excepciones Python
  - Responsabilidad de → :ref:`arq-mod-008`

- **Definir reglas de acceso**

  - Ejemplo: "Solo auditor ve esto"
  - Responsabilidad de → :ref:`arq-mod-003`

- **Almacenar logs de infraestructura**

  - Ejemplo: Estado de servicios, timeouts, conexiones
  - Responsabilidad de → :ref:`arq-mod-008`
