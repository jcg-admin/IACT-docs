.. meta::
 :artefacto: ARQ_MOD_005_DIAG_COMPONENTES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/reports/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_005_componentes_mod_reports:

=====================================
Diagrama de componentes — MOD_Reports
=====================================

.. uml::
 :caption: Componentes de MOD_Reports y sus dependencias de datos.

 @startuml

 component "apps.reports\n(API views)" as MODULO_REPORTES
 component "SegmentResolver\n(DID_MAP)" as Segmentresolver
 component "ReportingService\n(cursor.callproc)" as Servicioreportes
 component "apps.exports\n(CSV/Excel)" as AppsExports
 component "InternalMailbox" as Internalmailbox

 database "base_ivr_detalle\nbase_ivr_clientes\n(Almacen de Datos — solo lectura)" as base_ivr_detalle
 database "auth_user\naudit_log\n(PostgreSQL)" as auth_user

 MODULO_REPORTES --> Segmentresolver : resolve segmentos
 MODULO_REPORTES --> Servicioreportes : invocar sp_rpt_*
 Servicioreportes --> base_ivr_detalle : CALL sp_rpt_* (lectura)
 MODULO_REPORTES --> auth_user : leer DIDs del usuario (RBAC)
 MODULO_REPORTES --> AppsExports : generar archivo exportado
 AppsExports --> Internalmailbox : notificar disponibilidad

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/reports/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
