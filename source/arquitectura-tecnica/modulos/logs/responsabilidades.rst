.. _arq-mod-008-responsabilidades:

================================================
ARQ_MOD_008 — Responsabilidades del Modulo
================================================


PUEDE Hacer
===========

.. list-table::
 :widths: 55 20 25
 :header-rows: 1

 * - Responsabilidad
   - UC Relacionado
   - CNST
 * - Mostrar logs de aplicacion (INFO/WARN/ERROR)
   - UC_080
   - CNST_009
 * - Filtrar logs por nivel, fecha, componente
   - UC_080
   - -
 * - Mostrar estado de salud del sistema
   - UC_081
   - -
 * - Mostrar estado de servicios externos
   - UC_081
   - -
 * - Generar paquete comprimido de logs
   - UC_082
   - CNST_009
 * - Mostrar metricas tecnicas agregadas
   - UC_083
   - -

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**:

- **Registrar acciones de negocio**

  - Ejemplo: "Usuario exporto reporte X"
  - Responsabilidad de → :ref:`arq-mod-007`

- **Definir reglas de seguridad**

  - Ejemplo: "Si hay muchos errores de login, bloquear usuario"
  - Responsabilidad de → :ref:`arq-mod-003` (enforcers)

- **Exponer PII sin enmascarar**

  - Viola CNST_009 (proteccion de datos en logs)
  - Usernames, IPs deben enmascararse en logs publicos
