```yml
project: IACT-docs
work_package: 2026-05-05-08-28-07-use-case-view-uml07-conformance-pass
created_at: 2026-05-05 08:28:07
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-05-08-17-04-cnst-033-system-design-view-pass
target: Asegurar que use-case-view/* contenga solo diagramas conforme a uml-07-diagramas-casos-uso
```

# WP — Use Case View UML-07 Conformance Pass

## Trigger

Hallazgo: ``source/arquitectura-tecnica/use-case-view/uc-*.rst``
(13 archivos) usa **codenames RBAC como actores**
(``view_dashboard``, ``assign_functions``,
``manage_sessions``, etc.). Esto viola la convención
canónica documentada en:

- ``source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/`` —
  los actores son **roles** (Empleado, Consultor,
  Vendedor, Administrador), no permisos.
- ``source/requisitos/_metodologia-aplicacion/casos-uso-diagramas/`` —
  los ejemplos canónicos IACT
  (``ejemplo-iact-diagrama-de-alto-nivel``,
  ``ejemplo-iact-uc-rpt-04-exportar-reporte``) usan
  ``Operador``, ``Supervisor``, ``Admin Acceso``,
  ``Admin Pipeline``, ``Auditor``, ``Sistema/Scheduler``,
  ``IVR Conmutador``.

## Hallazgo conceptual

Los **codenames RBAC** son **funciones de autorización**,
no actores. Un actor es **quien ejecuta** un caso de uso
(``Operator``, ``Supervisor``, ``Caller``); un permiso
(``view_dashboard``) es lo que el actor **necesita poseer**
para iniciar el UC.

Confundir actor con permiso causa que:

- el diagrama tenga 7-25 "actores" cuando solo hay 1-3
  roles reales;
- la jerarquía de generalización entre roles
  (``Usuario <|-- Operator <|-- Supervisor``) sea
  imposible de modelar;
- el diagrama no se pueda leer al estilo
  *"actor inicia caso de uso"* del libro UML-07.

## Alcance

13 archivos a re-escribir:

| Archivo | Módulo | Actores RBAC actuales (incorrectos) |
|---------|--------|-------------------------------------|
| uc-auth.rst | MOD_Auth | UsuarioAnonimo, user_autenticado, view_all_active_sessions… |
| uc-users.rst | MOD_Users | create_users, update_users, delete_users… |
| uc-access.rst | MOD_Access | assign_functions, revoke_functions… |
| uc-permissions.rst | MOD_Permissions | assign_function_groups… |
| uc-reports.rst | MOD_Reports | view_dashboard, view_kpis, export_csv, schedule_report… |
| uc-alerts.rst | MOD_Alerts | configure_team_alerts, view_alerts, acknowledge_alert… |
| uc-pipeline.rst | MOD_Pipeline | view_pipeline_status, request_pipeline_retry, APScheduler |
| uc-audit.rst | MOD_Audit | view_audit_log, search_audit_log… |
| uc-logs.rst | MOD_Logs | view_application_logs, view_pipeline_logs… |
| uc-operator.rst | MOD_Operator | manage_own_agent_state, answer_inbound_calls… |
| uc-supervision.rst | MOD_Supervision | monitor_live_calls, barge_in_calls… |
| uc-caller.rst | MOD_Caller | (Caller — único correcto) |
| uc-admin.rst | MOD_Admin | admin_sistema, manage_function_catalog… |

## Output esperado

- 13 archivos re-escritos con **actores como roles** y
  permisos RBAC trasladados a notas/anotaciones donde
  aplique.
- ``discover/actor-role-mapping.md`` — tabla canónica
  de roles del proyecto IACT.
- ``decisions-log.md`` — D-NN.
- Pre-render PlantUML 0 errores.

## Referencias canónicas consultadas

- ``source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/``
  - ``representacion-de-un-modelo-de-caso-de-uso.rst``
  - ``comprension-de-los-usuarios.rst`` (jerarquía
    de actores)
  - ``inclusion.rst``, ``extension.rst``,
    ``generalizacion.rst``
- ``source/requisitos/_metodologia-aplicacion/casos-uso-diagramas/``
  - ``ejemplo-iact-diagrama-de-alto-nivel.rst``
  - ``ejemplo-iact-uc-rpt-04-exportar-reporte.rst``
  - ``generalizacion-entre-actores.rst``
  - ``posicionamiento.rst``
