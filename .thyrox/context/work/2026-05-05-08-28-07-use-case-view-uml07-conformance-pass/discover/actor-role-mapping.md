```yml
created_at: 2026-05-05 08:29:00
project: IACT-docs
work_package: 2026-05-05-08-28-07-use-case-view-uml07-conformance-pass
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Actor Role Mapping — IACT canonical actors

## Fuente

Derivado de ``ejemplo-iact-diagrama-de-alto-nivel.rst`` y
``generalizacion-entre-actores.rst`` del corpus
``_metodologia-aplicacion``. Alineado con CNST-033 §6
(catálogo de grupos AGR-001..010).

## Jerarquía canónica de actores

.. code-block:: text

    User (base abstracta)
    ├── Caller          (externo — caller IVR sin autenticación)
    ├── Operator        (AGR-001 basic_operator_group)
    ├── Supervisor      (AGR-002,003,004,005 — viewer + quality + exporter + alert)
    ├── UserAdmin       (AGR-006 user_admin_group)
    ├── AccessAdmin     (AGR-007 permission_admin_group)
    ├── Auditor         (AGR-008 auditor_group)
    ├── PipelineAdmin   (AGR-009 pipeline_admin_group)
    └── SystemAdmin     (AGR-010 system_admin_group — superuser)

    Sistemas externos:
    ├── Scheduler       (cron, APScheduler — sistema interno automatizado)
    └── IvrSwitch       (IVR conmutador — sistema externo origen de datos)

## Reglas de mapeo

1. **Un UC tiene 1-3 actores** típicamente, no 5-25.
2. **El actor es quien INICIA** el UC. Los permisos son
   atributos del rol, no actores en el diagrama.
3. Los **codenames RBAC** se documentan en una **nota
   o caption** del diagrama, no como actores.
4. La **jerarquía de actores** se modela con
   ``<|--`` (generalización) cuando aporta clarity.

## Asignación rol → módulo

Basado en CNST-033 §6 + análisis del catálogo de
funciones (§5):

| Módulo | Actor primario | Actores secundarios |
|--------|----------------|---------------------|
| MOD_Auth | User (autenticado/anónimo) | SystemAdmin (force-close), Auditor |
| MOD_Users | UserAdmin | (todos los roles consumen view) |
| MOD_Access | AccessAdmin | Auditor (read-only) |
| MOD_Permissions | AccessAdmin | (todos los roles autenticados — verify) |
| MOD_Reports | Operator | Supervisor (export, schedule) |
| MOD_Alerts | Supervisor | Operator (view), AlertManager |
| MOD_Pipeline | PipelineAdmin | Scheduler (sistema), Auditor |
| MOD_Audit | Auditor | (todos — generate compliance) |
| MOD_Logs | SystemAdmin | Auditor, PipelineAdmin |
| MOD_Operator | Operator | Supervisor (monitor) |
| MOD_Supervision | Supervisor | Operator (broadcast target) |
| MOD_Caller | Caller (externo) | Scheduler |
| MOD_Admin | SystemAdmin | Auditor (read-only) |

## Convención de naming

- **PascalCase** para clases de actor: ``Operator``,
  ``Supervisor``, ``UserAdmin``.
- **Inglés obligatorio** (CNST-033 §2).
- ``User`` es la clase base abstracta — no se usa como
  actor concreto en diagramas.

## Excepciones

- ``UsuarioAnonimo`` y ``user_autenticado`` actuales en
  ``uc-auth.rst`` — son **estados de User**, no roles
  RBAC. Se modelan como ``User<<unauthenticated>>`` y
  ``User<<authenticated>>`` o como dos actores
  ``UnauthenticatedUser`` y ``AuthenticatedUser`` con
  generalización a ``User``.

## Codenames RBAC en el diagrama

Los codenames van en **nota** del diagrama, agrupados
por UC. Ejemplo:

.. code-block:: text

   note right of MOD_Reports
     Codenames RBAC requeridos:
       - VER_DASHBOARD_IVR: view_dashboard
       - EXPORTAR_REPORTE:  export_csv | export_pdf | export_excel
       - PROGRAMAR_REPORTE: schedule_report
   end note
