.. meta::
 :artefacto: AT_UC_ACTORES
 :tipo: Diagrama Arquitectonico — Jerarquia de Actores
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_jerarquia_actores:

==========================
Jerarquía de Actores IACT
==========================

Modelo de actores del sistema IACT con generalización
``<|--`` per uml-07 ``comprension-de-los-usuarios.rst``:

  > Sería conveniente mostrar a los usuarios en una
  > **jerarquía de generalización**.

.. uml::
 :caption: Jerarquía de actores IACT — roles autenticados,
           actor externo y sistemas internos.

 @startuml

 actor User <<abstract>>
 actor Operator
 actor Supervisor
 actor UserAdmin
 actor AccessAdmin
 actor Auditor
 actor PipelineAdmin
 actor SystemAdmin

 User <|-- Operator
 Operator <|-- Supervisor
 User <|-- UserAdmin
 User <|-- AccessAdmin
 User <|-- Auditor
 User <|-- PipelineAdmin
 User <|-- SystemAdmin

 actor "Caller\n<<external>>" as Caller
 actor "Scheduler\n<<system>>" as Scheduler
 actor "IvrSwitch\n<<system>>" as IvrSwitch
 actor "AlertEngine\n<<system>>" as AlertEngine

 note right of User
   Clase abstracta: no instanciable.
   Provee login(), logout(),
   changePassword().
 end note

 note bottom of Caller
   Externo no autenticado.
   Origina llamadas vía IvrSwitch.
 end note

 note bottom of Scheduler
   Cron / APScheduler.
   Dispara pipeline batch nocturno.
 end note

 @enduml

Mapeo a grupos RBAC (CNST-033 §6)
==================================

.. list-table::
 :header-rows: 1
 :widths: 20 20 60

 * - Actor
   - AGR
   - Funciones representativas
 * - ``Operator``
   - AGR-001
   - ``manage_own_agent_state``,
     ``answer_inbound_calls``, ``view_reports``,
     ``view_alerts``
 * - ``Supervisor``
   - AGR-002, 003, 004, 005
   - hereda Operator + ``export_csv``,
     ``schedule_report``, ``configure_team_alerts``,
     ``acknowledge_alert``, ``monitor_live_calls``,
     ``barge_in_calls``, ``broadcast_team_messages``
 * - ``UserAdmin``
   - AGR-006
   - ``create_users``, ``update_users``,
     ``block_users``, ``reactivate_users``
 * - ``AccessAdmin``
   - AGR-007
   - ``assign_functions``, ``revoke_functions``,
     ``assign_function_groups``,
     ``manage_separation_rules``,
     ``grant_exceptional_permission``
 * - ``Auditor``
   - AGR-008
   - ``view_audit_log``, ``search_audit_log``,
     ``export_audit_log``,
     ``generate_compliance_report``
 * - ``PipelineAdmin``
   - AGR-009
   - ``view_pipeline_errors``,
     ``request_pipeline_retry``
 * - ``SystemAdmin``
   - AGR-010
   - superuser — gestiona catálogo de funciones
     y agrupadores (UC_ADM_*)
 * - ``Caller``
   - — (externo)
   - sin codenames RBAC; origina ``UC_CLI_*``
 * - ``Scheduler``
   - — (sistema)
   - dispara pipeline batch sin actor humano
 * - ``IvrSwitch``
   - — (sistema)
   - PBX externo: origina llamadas en
     ``UC_OPR_02``
 * - ``AlertEngine``
   - — (sistema)
   - evalúa reglas y emite ``UC_ALR_05``

.. seealso::

 :doc:`/base-cognitiva/_uml/uml-07-diagramas-casos-uso/comprension-de-los-usuarios`
 :doc:`/base-cognitiva/_uml/uml-07-diagramas-casos-uso/generalizacion`
 :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`
