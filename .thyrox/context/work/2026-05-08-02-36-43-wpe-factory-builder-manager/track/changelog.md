```yml
created_at: 2026-05-08 03:30:00
project: IACT-docs
work_package: 2026-05-08-02-36-43-wpe-factory-builder-manager
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — WP-E (Factory/Builder/Manager rename)

## [1.0.0] — 2026-05-08

### Renamed (13 clases en 7 commits)

#### Factory (6 renames)

| Clase antigua | Clase nueva | Razon |
|---|---|---|
| `EventFactory` (uc-perm-09) | `AuditEventCreator` | Produccion: rol de creacion de AuditEvent |
| `UserFactory` (uc-usr-01 patrones) | `UserOnboardingService` | Produccion: orquestar provisioning |
| `UserFactory` (uc-auth-01 testing) | `UserTestData` | factory_boy tests §1.3 |
| `SessionFactory` (uc-auth-02) | `SessionTestData` | factory_boy tests §1.3 |
| `GrupoPermisoFactory` (ADR-003) | `GrupoPermisoTestData` | factory_boy tests §1.3 |
| `UsuarioGrupoFactory` (ADR-003) | `UsuarioGrupoTestData` | factory_boy tests §1.3 |

#### Builder (5 renames + 1 preservada)

| Clase | Nuevo nombre | Razon |
|---|---|---|
| `ComparativeBuilder` | `ComparativeAssembler` | No fluent (build only) |
| `DisponibilidadBuilder` | `DisponibilidadAssembler` | No fluent |
| `HeatmapBuilder` | `HeatmapAssembler` | No fluent |
| `MenuBuilder` | `MenuAssembler` | No fluent |
| `SummaryBuilder` | `ResumenSaludAssembler` | Mismo concepto que ya renombrado |
| `QueryBuilder` | **PRESERVADO** | Interfaz fluent real `.where().apply().order_by()` |

#### Manager (3 renames + 1 preservada)

| Clase | Nuevo nombre | Razon |
|---|---|---|
| `AccessGroupManager` | `AccessGroupQueryRepository` | Django Manager con custom queryset |
| `AlertManager` | `AlertOperationsCoordinator` | Sufijo Manager generico |
| `TxManager` (alias plantuml) | `TransactionalContext` | Alias plantuml |
| `TransactionManager` | **PRESERVADO** | API Django ORM real (`transaction.atomic()`) |

### Preserved (excepciones intencionales)

- `DjangoModelFactory`, `SubFactory` — `factory_boy` library externa.
- `QueryBuilder` — interfaz fluent legitima.
- `TransactionManager` — API publica Django ORM.
- `ReportFactory` (2 refs) — notas historicas en
  `factory-method-reportes.rst` documentando rename Sprint 1.
- `ResumenSaludBuilder` (1 ref) — nota historica en
  `resumen-salud-assembler.rst` documentando rename del WP
  `naming-rules-resolution`.

### Verification

```bash
$ grep -rohE "\b[A-Z][a-zA-Z]+Factory\b" source/ | sort -u
DjangoModelFactory   # external lib
ReportFactory         # historical note only
SubFactory            # external lib

$ grep -rohE "\b[A-Z][a-zA-Z]+Builder\b" source/ | sort -u
QueryBuilder          # fluent interface preserved
ResumenSaludBuilder   # historical note only

$ grep -rohE "\b[A-Z][a-zA-Z]+Manager\b" source/ | sort -u
TransactionManager    # Django ORM API preserved
```

✅ Todos los sufijos prohibidos eliminados; preservaciones
documentadas y verificadas.

## Commits del WP (8 commits)

1. WP setup + Phase 1 audit.
2. EventFactory → AuditEventCreator.
3. UserFactory (uc-usr-01) → UserOnboardingService.
4. UserFactory/SessionFactory/GrupoPermisoFactory/UsuarioGrupoFactory → *TestData.
5. ComparativeBuilder/DisponibilidadBuilder/HeatmapBuilder/MenuBuilder/SummaryBuilder → *Assembler.
6. AccessGroupManager/AlertManager/TxManager rename.
7. (este commit) — TR cierre.

## Roadmap status

| WP | Estado |
|---|---|
| WP-A | ✅ Sprint 1 |
| WP-B | ✅ Sprint 2 |
| WP-C | ✅ Sprint 2 |
| WP-D | ✅ naming-rules-resolution |
| WP-E | ✅ **este WP** |
| WP-F (Serializer/ViewSet/View) | ⏸ requiere merge a develop de conventions.rst v2.0.0 |
| WP-G (STD-010 cleanup vocabulario) | ⏸ Sprint 3 |
| WP-H | ✅ Sprint 1 |

## Refs

- WP `naming-rules-resolution` (D3 criterio Builder fluent).
- WP `sprint1-filenames-and-factory` (precedente ReportFactory).
- WP `sprint2-sod-narrative-and-classes` (cleanup SoD).
- CLEAN_CODE §1.2, §1.3, §1.4, §6.2.
