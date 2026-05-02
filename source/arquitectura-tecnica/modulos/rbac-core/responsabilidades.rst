.. _arq-mod-003-responsabilidades:

================================================
ARQ_MOD_003 — Responsabilidades del Modulo
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

PUEDE Hacer
===========

.. list-table::
 :widths: 55 20 25
 :header-rows: 1

 * - Responsabilidad
   - UC Relacionado
   - CNST
 * - CRUD de roles funcionales
   - UC_041
   - CNST_005
 * - Calcular permisos efectivos
   - UC_042
   - CNST_005
 * - Aplicar precedencia (Directo > Rol > Segmento)
   - UC_042
   - -
 * - Validar reglas SoD
   - UC_042
   - -
 * - Asignar/retirar roles a usuarios
   - UC_043
   - -
 * - Configurar segmentos de datos
   - UC_044
   - -
 * - Asignar permisos directos con vigencia
   - UC_045
   - -
 * - Simular acceso de un usuario
   - UC_046
   - -
 * - Generar matriz de roles/permisos
   - UC_047
   - -
 * - Aplicar restricciones criticas (enforcers)
   - Transversal
   - CNST_001-010

----

NO PUEDE Hacer (Violaciones)
=============================

.. warning::

 Las siguientes acciones **violan la separacion de responsabilidades**:

- **Mostrar UI funcional final**

  - Ejemplo: Renderizar dashboards o reportes
  - Responsabilidad de → :ref:`arq-mod-005`

- **Implementar logica de negocio de reportes**

  - Ejemplo: "Aplicar este filtro SQL concreto para metricas"
  - Responsabilidad de → :ref:`arq-mod-005`

- **Ejecutar ETL o agendar jobs**

  - Responsabilidad de → :ref:`arq-mod-004`

- **Validaciones propias del dominio IVR**

  - Ejemplo: Reglas de menus, transferencias, etc.
  - Responsabilidad de → :ref:`arq-mod-005`
