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

Definicion arquitectonica de los **13 modulos UC del sistema** (9 RBAC activos + ADM nuevo v5.6.0 + 2 reservados open-closed + Caller sin RBAC)
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
 * - :ref:`arq_mod_access` ACCESS
   - :doc:`/requisitos/casos-uso/access/index`
   - 9
 * - :ref:`arq_mod_admin` ADMIN
   - (futuros UC_ADM_*)
   - en construccion
 * - :ref:`arq-mod-006` ALERTS
   - :doc:`/requisitos/casos-uso/alerts/index`
   - 5
 * - :ref:`arq-mod-007` AUDIT
   - :doc:`/requisitos/casos-uso/audit/index`
   - 4
 * - :ref:`arq-mod-001` AUTH
   - :doc:`/requisitos/casos-uso/auth/index`
   - 5
 * - :ref:`arq-mod-011` CALLER
   - :doc:`/requisitos/casos-uso/caller/index`
   - 5
 * - :ref:`arq-mod-008` LOGS (antes SYS_LOGS)
   - :doc:`/requisitos/casos-uso/logs/index`
   - 7
 * - :ref:`arq-mod-009` OPERATOR
   - :doc:`/requisitos/casos-uso/operator/index`
   - 10
 * - :ref:`arq-mod-003` PERMISSIONS (antes RBAC_CORE)
   - :doc:`/requisitos/casos-uso/permissions/index`
   - 10
 * - :ref:`arq-mod-004` PIPELINE (antes ETL_MONITORING)
   - :doc:`/requisitos/casos-uso/pipeline/index`
   - 4
 * - :ref:`arq-mod-005` REPORTS (antes VIS_REPORTS)
   - :doc:`/requisitos/casos-uso/reports/index`
   - 14
 * - :ref:`arq-mod-010` SUPERVISION
   - :doc:`/requisitos/casos-uso/supervision/index`
   - 3
 * - :ref:`arq-mod-002` USERS (antes USER_IDENTITY)
   - :doc:`/requisitos/casos-uso/users/index`
   - 4

Catalogo
--------

.. toctree::
 :maxdepth: 1
 :caption: Decisiones transversales

 coexistence-with-design-implementation-view

.. toctree::
 :maxdepth: 2

 access/index
 admin/index
 alerts/index
 audit/index
 auth/index
 caller/index
 logs/index
 operator/index
 permissions/index
 pipeline/index
 reports/index
 supervision/index
 users/index
