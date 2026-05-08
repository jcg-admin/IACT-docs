```yml
project: IACT-docs
work_package: 2026-05-08-03-18-31-wpf-serializer-viewset-view
created_at: 2026-05-08 03:18:31
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (re-audit muestra ~21 clases framework-coupled in-scope, no ~115+)
target: WP-F del roadmap. Aplica CLEAN_CODE §6.2 prohibicion de sufijos framework-coupled (Serializer/ViewSet/View/Permission/Backend) en clases que extienden bases DRF/Django. Re-audit detecta que el estimado original ~115+ clases incluia 199 referencias de narrativa arquitectonica Kruchten 4+1 (UseCaseView, ArchView, DesignView, ImplementationView, ProcessView, ContextView, UMLSystemView, UCModuleView) que NO son clases — son vocabulario de viewpoints arquitectonicos.
predecessor_wp: 2026-05-08-03-08-21-wpg-std010-cleanup (cerrado)
trigger: directiva del ejecutor "Procede con WP-F primero. TD-D5 despues."
```

# WP-F — Serializer/ViewSet/View/Permission rename

## Pre-condicion verificada

`backend/conventions.rst` v2.0.0 (con prohibicion §6.2 alineada
a CLEAN_CODE) esta presente en `feature/cnst-033-uml-conformance`
desde WP-D `naming-rules-resolution`. WP-F NO depende de merge
a develop.

## Re-audit del scope

Audit por sufijo retorna estos counts en `source/`:

| Sufijo | Refs totales | Clases unicas (def) | Narrativa |
|---|---|---|---|
| Serializer | ~50 | 4 def + ~45 type refs | 0 |
| ViewSet | ~15 | 4 def | 1 (ModelViewSet ext) |
| View | ~432 | 11 def | **199 narrativa Kruchten** |
| Permission | ~180 | 3 def + ~120 entidad dominio | — |
| Backend | ~50 | 1 def + ~30 ext libs | — |

**Hallazgo critico:** las 432 refs de `View` se descomponen en:

| Categoria | Cuenta | Naturaleza |
|---|---|---|
| `UseCaseView` | 91 | Directorio `arquitectura-tecnica/use-case-view/` (no clase) |
| `SavedView` | 63 | Domain entity (vista guardada de reporte) |
| `DesignView` | 38 | Kruchten 4+1 viewpoint (narrativa) |
| `APIView` | 23 | DRF base externa (preservar) |
| `ImplementationView` | 14 | Kruchten viewpoint (narrativa) |
| `UCModuleView` | 14 | Kruchten viewpoint UML metamodel |
| `UMLSystemView` | 13 | Kruchten viewpoint UML metamodel |
| `ArchView` | 15 | Alias plantuml metamodelo (`class "View" as ArchView`) |
| `OperationalView` | 5 | Kruchten viewpoint |
| `ProcessView` | 5 | Kruchten viewpoint |
| `ContextView` | 4 | Kruchten viewpoint |
| Clases DRF reales | ~30 | LoginView, LogoutView, etc. (in-scope) |

Total narrativa arquitectonica preservable: **199 refs**.
Total in-scope CLEAN_CODE §6.2: **~30 refs DRF View**.

## Decision para este WP

Aplicar CLEAN_CODE §6.2 a clases que cumplen el criterio
**framework-coupled** (analogo al criterio D3 de WP-E sobre
fluent vs no-fluent):

**Criterio in-scope (rename):**

- Clase extiende base de framework: `APIView`, `ModelViewSet`,
  `ReadOnlyModelViewSet`, `ModelSerializer`, `BasePermission`,
  `BaseBackend`, `ModelBackend`, `TemplateView`.
- O el sufijo identifica rol del framework por contexto.

**Criterio out-of-scope (preservar):**

- Vocabulario Kruchten 4+1 (`UseCaseView`, `ProcessView`,
  `DesignView`, `LogicalView`, `ImplementationView`,
  `DeploymentView`, `OperationalView`, `ContextView`,
  `DevelopmentView`, `ArchView`) — paralelo a §5.4 STD-010
  para RBAC: vocabulario disciplinar de la arquitectura.
- Domain entities con sufijo nominal: `SavedView`,
  `AuditEventView`, `ExceptionalPermission`,
  `TemporaryPermission`, `DirectPermission`,
  `GranularPermission` (cuando NO extienden BasePermission),
  `StorageBackend` (cuando NO extiende ModelBackend).
- Clases de libreria externa: `APIView`, `ModelSerializer`,
  `BasePermission`, `BaseBackend`, `ModelBackend`,
  `ModelViewSet`, `ReadOnlyModelViewSet`, `TemplateView`.

## Inventario de clases in-scope

### Serializer (4 clases unicas, ~50 refs totales)

| Clase actual | Contexto | Nuevo nombre propuesto |
|---|---|---|
| `LoginSerializer` | DRF auth uc-auth-01 | `LoginRequestContract` |
| `RefreshTokenSerializer` | DRF auth uc-auth-04 | `RefreshTokenRequestContract` |
| `TokenSerializer` | DRF auth | `TokenResponseContract` |
| `ReportSerializer` | DRF reports uc-rpt-* | `ReportContract` |

Otros nombres `*Serializer` mencionados en docs (UserSerializer,
SupervisionSerializer, AuthSerializer, etc.) no tienen `class
def` localizada en source — son referencias de tipo
ilustrativas. Aplicar transformacion en bloque si aplica.

### ViewSet (4 clases unicas)

| Clase actual | Tipo | Nuevo nombre |
|---|---|---|
| `MenuItemAdminViewSet(ModelViewSet)` | DRF | `MenuItemAdminEndpoints` |
| `ReportViewSet(ReadOnlyModelViewSet)` | DRF | `ReportEndpoints` |
| `MyViewSet(ModelViewSet)` | DRF (ejemplo) | `MyEndpoints` |
| `DashboardViewSet` | DRF | `DashboardEndpoints` |

### View — DRF clases (~11 def + refs)

| Clase actual | Contexto | Nuevo nombre |
|---|---|---|
| `LoginView(APIView)` | uc-auth-01 | `LoginEndpoint` |
| `LogoutView(APIView)` | uc-auth-03 | `LogoutEndpoint` |
| `RefreshTokenView(APIView)` | uc-auth-04 | `RefreshTokenEndpoint` |
| `ResetPasswordView(APIView)` | auth | `ResetPasswordEndpoint` |
| `MenuItemBulkReorderView(APIView)` | uc-adm-04 | `MenuItemBulkReorderEndpoint` |
| `MyView(APIView)` | rbac-impl-guide ejemplo | `MyEndpoint` |
| `ReportListView(APIView)` | rbac-impl-guide | `ReportListEndpoint` |
| `ReportExportView` | reports | `ReportExportEndpoint` |
| `DashboardView(TemplateView)` | adr-back-005 | `DashboardEndpoint` |
| `UserMenuView(APIView)` | uc-perm-* | `UserMenuEndpoint` |
| `AuditEventView` (si DRF) | audit-query-service | revisar caso-por-caso |

### Permission (DRF, ~3 def + ~33 refs)

| Clase actual | Tipo | Nuevo nombre |
|---|---|---|
| `GranularPermission(BasePermission)` | DRF | `GranularAccessPolicy` |
| `FunctionPermission(BasePermission)` | DRF | `FunctionAccessPolicy` |
| `HasFunctionPermission` | DRF | `RequireFunctionPolicy` |

### Backend (~1 def + refs externos)

| Clase actual | Tipo | Nuevo nombre |
|---|---|---|
| `FunctionAuthBackend` | Django auth backend | `FunctionAuthProvider` |
| `RBACBackend` | Django auth backend | `RBACAuthProvider` |

### Preservados (criterio out-of-scope)

**Domain entities (no extienden framework):**

- `SavedView` (63 refs) — domain entity de reportes guardados.
  El sufijo "View" es nominal de dominio.
- `ExceptionalPermission` (124 refs) — domain entity RBAC.
  "Permission" es nominal del dominio.
- `TemporaryPermission`, `DirectPermission` — domain RBAC.
- `AuditEventView` (8 refs) — query/CQRS read model.

**Vocabulario Kruchten 4+1 / metamodelo UML (~199 refs):**

- `UseCaseView`, `LogicalView`, `ProcessView`,
  `ImplementationView`, `DeploymentView`, `OperationalView`,
  `ContextView`, `DesignView`, `DevelopmentView`,
  `UMLSystemView`, `UCModuleView`, `ArchView`.

**Librerias externas:**

- `APIView`, `ModelSerializer`, `ModelViewSet`,
  `ReadOnlyModelViewSet`, `BasePermission`, `BaseBackend`,
  `ModelBackend`, `TemplateView`.

## Output esperado

~21 renames de clases framework-coupled + cross-refs derivados.
Estimado ~80-150 ediciones, ~5-7 commits.

## Stopping points

- **SP-01:** caso `AuditEventView` — verificar si es DRF view
  o domain query model antes de decidir.
- **SP-02:** revision de `*Serializer` sin def encontrado —
  solo referencias narrativas, decidir si renombrar.
- **SP-03:** validacion final con grep §6.2.

## Refs

- WP `naming-rules-resolution` (D1 backend/conventions.rst v2.0.0).
- WP `2026-05-08-02-36-43-wpe-factory-builder-manager` (D3 criterio
  framework-coupled vs domain-entity).
- CLEAN_CODE §6.2.
- backend/conventions.rst v2.0.0 §6.2.
