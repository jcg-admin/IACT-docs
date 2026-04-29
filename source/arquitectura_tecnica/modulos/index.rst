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
 * - ARQ_MOD_001 AUTH
   - :doc:`/requisitos/casos_uso/auth/index`
   - 5
 * - ARQ_MOD_002 USER_IDENTITY
   - :doc:`/requisitos/casos_uso/users/index`
   - 4
 * - ARQ_MOD_003 RBAC_CORE
   - :doc:`/requisitos/casos_uso/access/index` + :doc:`/requisitos/casos_uso/permissions/index`
   - 19 (9 ACC + 10 PERM)
 * - ARQ_MOD_004 ETL_MONITORING
   - :doc:`/requisitos/casos_uso/pipeline/index`
   - 4
 * - ARQ_MOD_005 VIS_REPORTS
   - :doc:`/requisitos/casos_uso/reports/index`
   - 14
 * - ARQ_MOD_006 ALERTS
   - :doc:`/requisitos/casos_uso/alerts/index`
   - 5
 * - ARQ_MOD_007 AUDIT
   - :doc:`/requisitos/casos_uso/audit/index`
   - 4
 * - ARQ_MOD_008 SYS_LOGS
   - :doc:`/requisitos/casos_uso/logs/index`
   - 4

Catalogo
--------

.. toctree::
 :maxdepth: 1

 ARQ_MOD_001_AUTH
 ARQ_MOD_002_USER_IDENTITY
 ARQ_MOD_003_RBAC_CORE
 ARQ_MOD_004_ETL_MONITORING
 ARQ_MOD_005_VIS_REPORTS
 ARQ_MOD_006_ALERTS
 ARQ_MOD_007_AUDIT
 ARQ_MOD_008_SYS_LOGS
