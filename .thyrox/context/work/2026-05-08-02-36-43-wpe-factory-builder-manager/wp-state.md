```yml
project: IACT-docs
work_package: 2026-05-08-02-36-43-wpe-factory-builder-manager
created_at: 2026-05-08 02:36:43
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (13 renames + ~80-120 cross-refs)
target: WP-E del roadmap clean-code-naming. Rename de clases con sufijos prohibidos Factory/Builder/Manager (CLEAN_CODE §1.2, §6.2). Verificacion caso-por-caso del rol (D3) para distinguir Builder fluent legitimo (preservar) vs Builder no-fluent (renombrar a Assembler), y Manager Django ORM (preservar como API) vs Manager generico (renombrar).
predecessor_wp: 2026-05-08-02-11-08-sprint2-sod-narrative-and-classes (cerrado)
trigger: directiva del ejecutor "Procede con WP-E antes de Sprint 3"
```

# WP-E — Factory/Builder/Manager rename

## Estado al abrir el WP

Tras Sprints 1+2:

| Categoria | Clases unicas detectadas |
|---|---|
| Factory | 8 (incluye 2 librerias: `DjangoModelFactory`, `SubFactory`) |
| Builder | 7 (incluye 1 ya renombrado: `ResumenSaludBuilder` historico) |
| Manager | 4 |
| **Total** | **19** |

Out-of-scope (clases base de libreria externa):

- `DjangoModelFactory`, `SubFactory` — `factory_boy` library

Renames a aplicar: **5 Factory + 5 Builder + 3 Manager = 13 renames**.

## Pre-condicion verificada

`backend/conventions.rst` v2.0.0 esta en esta rama
(`feature/cnst-033-uml-conformance`) tras D1 del WP
`naming-rules-resolution`. En `origin/develop` aun esta v1.0.0.

**WP-F (siguiente) requiere merge a develop antes de
ejecutar.** Este WP-E NO depende de develop — opera solo en
clases de Factory/Builder/Manager que no estan en
`backend/conventions.rst`.

## Decisiones por clase

### Factory (5 a renombrar)

| Clase actual | Contexto | Nuevo nombre | Razon |
|---|---|---|---|
| `EventFactory` (uc-perm-09 produccion) | Crea AuditEvent con UUID v7 + request_id | `AuditEventCreator` | Rol de produccion: creacion completa de eventos |
| `GrupoPermisoFactory` (backend ADR-003) | factory_boy en ejemplo tests | `GrupoPermisoTestData` | Tests data §1.3 |
| `SessionFactory` (uc-auth-02 testing) | `class SessionFactory(factory.django.DjangoModelFactory)` | `SessionTestData` | Tests data §1.3 |
| `UserFactory` (uc-usr-01 patrones produccion) | Patron Factory Method de creacion User + side-effects | `UserOnboardingService` | Rol de dominio: orquestar provisioning completo de User |
| `UserFactory` (uc-auth-01 testing) | factory_boy en tests | `UserTestData` | Tests data §1.3 |
| `UsuarioGrupoFactory` (backend ADR-003) | factory_boy en tests | `UsuarioGrupoTestData` | Tests data §1.3 |

Out-of-scope (preservar):

- `ReportFactory` ya renombrado a `ReportTypeRegistry` en
  Sprint 1 (WP-H). Refs remanentes son **historicas** en la
  nota del archivo renombrado.
- `DjangoModelFactory`, `SubFactory` — librerias externas.

### Builder (5 a renombrar; 1 preservar)

| Clase | Tiene fluent? | Decision | Nuevo nombre |
|---|---|---|---|
| `ComparativeBuilder` | NO (`build()` solo) | Renombrar | `ComparativeAssembler` |
| `DisponibilidadBuilder` | NO (`build()` solo) | Renombrar | `DisponibilidadAssembler` |
| `HeatmapBuilder` | NO (construye matriz desde rows) | Renombrar | `HeatmapAssembler` |
| `MenuBuilder` | NO (`build(user, locale)`) | Renombrar | `MenuAssembler` |
| `QueryBuilder` | **SI** (`.where().apply().order_by()`) | **PRESERVAR** | (sin cambio) |
| `SummaryBuilder` | NO (legacy del ResumenSalud) | Renombrar (alinear) | `ResumenSaludAssembler` |
| `ResumenSaludBuilder` | (ya renombrado en WP previo) | (refs historicas legitimas) | (sin cambio) |

`QueryBuilder` es **caso testigo del criterio D3**: tiene
interfaz fluent real (`.where().apply().order_by()`) que
hace el sufijo Builder semanticamente correcto. Preservar.

### Manager (3 a renombrar; 1 preservar)

| Clase | Contexto | Decision | Nuevo nombre |
|---|---|---|---|
| `AccessGroupManager` | Django ORM Manager (`queryset.system()/.custom()`) | Renombrar | `AccessGroupQueryRepository` |
| `AlertManager` | 1 ref plantilla (sin spec) | Renombrar | `AlertOperationsCoordinator` |
| `TransactionManager` | API Django ORM real (`transaction.atomic()`) | **PRESERVAR** | (sin cambio - es API Django) |
| `TxManager` | alias plantuml | Renombrar | `TransactionalContext` |

`TransactionManager` es la API publica de Django ORM. Es
vocabulario externo del framework, no del proyecto. Preservar.

## Output esperado

13 renames + cross-refs derivados. Estimado ~80-120 ediciones,
~6-10 commits.

## Post-WP-E

WP-F (Serializer/ViewSet/View) puede iniciar tras:

1. Cierre de este WP-E.
2. Merge a develop de `backend/conventions.rst` v2.0.0.

WP-G (STD-010 cleanup vocabulario) independiente.

## Refs

- WP `naming-rules-resolution` (D3 criterio Builder fluent).
- WP `sprint1-filenames-and-factory` (precedente: ReportFactory).
- CLEAN_CODE §1.2, §1.3, §1.4, §6.2.
- STD-010 v1.1.0.
