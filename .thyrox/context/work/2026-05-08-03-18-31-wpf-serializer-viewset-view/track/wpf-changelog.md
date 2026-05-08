```yml
created_at: 2026-05-08 03:35:00
project: IACT-docs
work_package: 2026-05-08-03-18-31-wpf-serializer-viewset-view
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — WP-F (Serializer/ViewSet/View/Permission/Backend rename)

## [1.0.0] — 2026-05-08

### Renamed (22 clases en 5 commits)

#### Bloque 1 — Serializer (4 clases)

| Clase antigua | Clase nueva | Razon |
|---|---|---|
| `LoginSerializer` | `LoginRequestContract` | Suffix `Serializer` framework-coupled |
| `RefreshTokenSerializer` | `RefreshTokenRequestContract` | Idem |
| `TokenSerializer` | `TokenResponseContract` | Idem |
| `ReportSerializer` | `ReportContract` | Idem |

#### Bloque 2 — ViewSet (4 clases)

| Clase antigua | Clase nueva | Razon |
|---|---|---|
| `MenuItemAdminViewSet` | `MenuItemAdminEndpoints` | Suffix `ViewSet` framework-coupled |
| `ReportViewSet` | `ReportEndpoints` | Idem |
| `MyViewSet` | `MyEndpoints` | Idem |
| `DashboardViewSet` | `DashboardEndpoints` | Idem |

#### Bloque 3 — View DRF (10 clases)

| Clase antigua | Clase nueva |
|---|---|
| `LoginView` | `LoginEndpoint` |
| `LogoutView` | `LogoutEndpoint` |
| `RefreshTokenView` | `RefreshTokenEndpoint` |
| `ResetPasswordView` | `ResetPasswordEndpoint` |
| `MenuItemBulkReorderView` | `MenuItemBulkReorderEndpoint` |
| `MyView` | `MyEndpoint` |
| `ReportListView` | `ReportListEndpoint` |
| `ReportExportView` | `ReportExportEndpoint` |
| `DashboardView` | `DashboardEndpoint` |
| `UserMenuView` | `UserMenuEndpoint` |

#### Bloque 4 — Permission DRF (3 clases)

| Clase antigua | Clase nueva | Razon |
|---|---|---|
| `GranularPermission` | `GranularAccessPolicy` | Extiende `BasePermission` |
| `FunctionPermission` | `FunctionAccessPolicy` | Idem |
| `HasFunctionPermission` | `RequireFunctionPolicy` | Idem |

#### Bloque 5 — Backend Django auth (1 clase)

| Clase antigua | Clase nueva | Razon |
|---|---|---|
| `FunctionAuthBackend` | `FunctionAuthProvider` | Backend Django auth (BaseBackend) |

### Preserved (excepciones intencionales)

#### Domain entities (criterio D3 — sufijo nominal, no framework-coupling)

| Clase | Razon |
|---|---|
| `SavedView` (63 refs) | Domain entity de reportes guardados — "View" como noun |
| `AuditEventView` (8 refs) | CQRS read model (DTO) — no extiende DRF View |
| `ExceptionalPermission` (124 refs) | RBAC domain entity — "Permission" como noun |
| `TemporaryPermission` | RBAC domain entity |
| `DirectPermission` | RBAC domain entity |
| `StorageBackend`, `CacheBackend` | Roles de infraestructura, no Django auth |

#### Vocabulario Kruchten 4+1 (~199 refs preservadas)

`UseCaseView` (91), `SavedView` (63), `DesignView` (38), `ArchView`
(15), `UCModuleView` (14), `ImplementationView` (14),
`UMLSystemView` (13), `OperationalView` (5), `ProcessView` (5),
`ContextView` (4), `LogicalView`, `DeploymentView`,
`DevelopmentView` — vocabulario de viewpoints arquitectonicos
disciplinares (paralelo a §5.4 STD-010 para RBAC).

#### Librerias externas (preservar bases del framework)

`APIView`, `ModelSerializer`, `ModelViewSet`, `ReadOnlyModelViewSet`,
`BasePermission`, `BaseBackend`, `ModelBackend`, `TemplateView`.

#### Anti-patterns literales (refs preservadas como ejemplos)

- `RBACPermission` — std-010 §5.4 y cnst-033 §4 lo muestran como
  clase prohibida (vs `AccessPolicy` canonico)
- `RBACBackend` — std-010 §5.4 y cia-rbac-002 lo muestran como
  prohibido (vs `AuthProvider` canonico)

### Verification

```bash
# Class definitions con sufijos prohibidos en source/
$ grep -rohE 'class\s+[A-Z][a-zA-Z]+(Serializer|ViewSet|View|Permission|Backend)\b' \
   source/ | sort -u
class AuditEventView           # CQRS read model — preserved
class ExceptionalPermission    # RBAC domain entity — preserved
class SavedView                # domain entity — preserved
```

✅ Cero clases framework-coupled remanentes; preservaciones
documentadas y verificadas por criterio D3.

## Commits del WP (7 commits)

1. `9952aca3` — Open WP-F (wp-state.md + audit)
2. `56abdc71` — Rename Serializer classes (1/5)
3. `d4eeb78e` — Rename ViewSet classes (2/5)
4. `447f8d29` — Rename DRF View classes (3/5)
5. `8c8817b3` — Rename DRF Permission classes (4/5)
6. `f0a80b6a` — Rename Django auth backend (5/5)
7. (este commit) — TR cierre

## Roadmap status

| WP | Estado |
|---|---|
| WP-A | ✅ Sprint 1 |
| WP-B | ✅ Sprint 2 |
| WP-C | ✅ Sprint 2 |
| WP-D | ✅ naming-rules-resolution |
| WP-E | ✅ Factory/Builder/Manager |
| WP-F | ✅ **este WP** — Serializer/ViewSet/View/Permission/Backend |
| WP-G | ✅ STD-010 cleanup vocabulario |
| WP-H | ✅ Sprint 1 |
| TD-D5 | ⏳ siguiente — STD-010 §2.5 ampliacion (identity files + procedimientos + ADRs) |

**Sprint 3 completo.** Todos los WPs activos del roadmap CLEAN_CODE
remediation cerrados. Pendiente solo TD-D5 (decision normativa
sobre exenciones de scope STD-010).

## Refs

- WP `naming-rules-resolution` (D1 backend/conventions.rst v2.0.0).
- WP `2026-05-08-02-36-43-wpe-factory-builder-manager` (D3 criterio).
- CLEAN_CODE §6.2.
- backend/conventions.rst v2.0.0 §6.2.
- STD-010 v1.1.0 §5.4 (canonical replacements AuthProvider/AccessPolicy).
