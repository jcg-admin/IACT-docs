.. meta::
 :artefacto: INDEX_ARQ_MODULOS
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: modulos
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-04-29
 :autor: NestorMonroy
 :clasificacion: Interno

=======================
Modulos Arquitectonicos
=======================

Definicion arquitectonica de los **8 modulos funcionales** del sistema
IACT. Cada ``ARQ_MOD_NNN`` documenta el proposito, responsabilidades,
componentes internos, interfaces, dependencias y consideraciones
tecnicas del modulo correspondiente.

Mapeo modulo ↔ casos de uso:

.. list-table::
 :widths: 25 50 25
 :header-rows: 1

 * - Modulo arquitectonico
   - UCs en requisitos
   - # UCs
 * - :ref:`arq-mod-001` AUTH
   - :doc:`/requisitos/casos-uso/auth/index`
   - 5
 * - :ref:`arq-mod-002` USER_IDENTITY
   - :doc:`/requisitos/casos-uso/users/index`
   - 4
 * - :ref:`arq-mod-003` RBAC_CORE
   - :doc:`/requisitos/casos-uso/access/index` + :doc:`/requisitos/casos-uso/permissions/index`
   - 19 (9 ACC + 10 PERM)
 * - :ref:`arq-mod-004` ETL_MONITORING
   - :doc:`/requisitos/casos-uso/pipeline/index`
   - 4
 * - :ref:`arq-mod-005` VIS_REPORTS
   - :doc:`/requisitos/casos-uso/reports/index`
   - 14
 * - :ref:`arq-mod-006` ALERTS
   - :doc:`/requisitos/casos-uso/alerts/index`
   - 5
 * - :ref:`arq-mod-007` AUDIT
   - :doc:`/requisitos/casos-uso/audit/index`
   - 4
 * - :ref:`arq-mod-008` SYS_LOGS
   - :doc:`/requisitos/casos-uso/logs/index`
   - 4

Catalogo
--------

.. toctree::
 :maxdepth: 2

 auth/index
 user-identity/index
 rbac-core/index
 etl-monitoring/index
 vis-reports/index
 alerts/index
 audit/index
 sys-logs/index
