.. _arq-mod-004-responsabilidades:

================================================
ARQ_MOD_004 — Responsabilidades del Modulo
================================================


PUEDE Hacer
===========

.. list-table::
 :widths: 55 20 25
 :header-rows: 1

 * - Responsabilidad
   - UC Relacionado
   - CNST
 * - Listar ejecuciones ETL historicas
   - UC_051
   - -
 * - Mostrar duracion, resultado, volumen
   - UC_051
   - -
 * - Ver detalle de ejecucion (errores, metricas)
   - UC_052
   - CNST_004
 * - Consultar que fechas/trimestres estan disponibles
   - UC_053
   - CNST_003
 * - Listar incidencias de calidad de datos
   - UC_054
   - -
 * - Reintentar transformacion sobre datos ya extraidos
   - UC_055
   - CNST_004

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**:

- **Generar tablas/graficos operativos para usuario final**

  - Ejemplo: Dashboard de llamadas por centro
  - Responsabilidad de → :ref:`arq-mod-005`

- **Exponer logs tecnicos crudos del sistema**

  - Ejemplo: Stack traces, errores de servidor
  - Responsabilidad de → :ref:`arq-mod-008`

- **Consultar BD IVR directamente**

  - Solo puede usar vista vw_llamadas
  - Viola CNST_003 (BD dual inmutable)

- **Definir reglas de seguridad**

  - Ejemplo: "Si falla N veces, bloquear algo"
  - Responsabilidad de → :ref:`arq-mod-003` (enforcers)
