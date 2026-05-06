.. meta::
 :artefacto: AT_DESIGN_CLASS_CALLER
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: caller
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_caller:

============================================================
Design View — MOD_Caller: Estructura de Clases
============================================================

Modulo de **modelo de llamada**: representa la entidad ``Call``
con su FSM (10 estados), navegacion IVR, y CSAT post-call. El
Caller es actor externo no autenticado (solo via PIN para CSAT).

.. uml::
 :caption: MOD_Caller — clases canonicas y relaciones internas.

 @startuml

 class Call
 class Menu
 class NavDomain
 class Campaign
 class CallerReportService <<sistema>>
 class PermissionService <<sistema>>
 class AuditService <<sistema>>

 Call --> Menu : navega
 Call --> Campaign : pertenece (opcional)
 Call --> NavDomain : registra navegacion
 Menu *-- NavDomain : opciones

 CallerReportService ..> Call : agrega CSAT
 PermissionService ..> Call : verify_function (Caller PIN)

 Call ..> AuditService : transitions FSM
 NavDomain ..> AuditService : on selection

 @enduml

----

UCs cubiertos
==============

UC_CLI_01..05 — ingresar IVR, navegar menu, escalar a operador,
escuchar opciones, calificar atencion (CSAT). Ver
:doc:`/arquitectura-tecnica/use-case-view/caller/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/call`
 - :doc:`/arquitectura-tecnica/domain-model/menu`
 - :doc:`/arquitectura-tecnica/domain-model/nav-domain`
 - :doc:`/arquitectura-tecnica/domain-model/campaign`
 - :doc:`/arquitectura-tecnica/domain-model/caller-report-service`
 - :doc:`/arquitectura-tecnica/domain-model/permission-service`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/caller/index`
 - :doc:`/arquitectura-tecnica/design-view/seq-caller`
 - :doc:`/arquitectura-tecnica/design-view/state-call`
