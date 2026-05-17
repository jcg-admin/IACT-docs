```yml
created_at: 2026-05-06 23:45:00
project: IACT-docs
work_package: 2026-05-06-21-42-06-menu-rbac-user-scope-docs
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Solution Strategy — Menu RBAC con User Scope

> Síntesis de Phase 5 STRATEGY. Consolida los 11 artefactos
> de Phase 1 DISCOVER en una estrategia de solución única,
> trazada a constraints normativas y al catálogo RBAC v5.6.0.

## Sección 1 — Objetivo del WP

Documentar el modelo, el lifecycle y los UCs necesarios
para que el sistema **derive el menú IACT desde el catálogo
RBAC v5.6.0** sin regresar al anti-patrón legacy
(``C_MENU2`` como fuente de la capability), preservando
defense-in-depth y permitiendo gestión administrativa de
items DRAFT/ACTIVE/DEPRECATED/ARCHIVED.

### Resultado esperado

1. Modelo ``MenuItem`` 1:1 con ``Function`` documentado en
   ADR-BACK-008 (nuevo).
2. CNST-032 reescrito para clausurar ``MenuItem``
   standalone.
3. 2 UCs nuevos del módulo MOD_Admin
   (``manage_menu_catalog`` y ``manage_menu_lifecycle``).
4. Endpoint ``GET /api/v1/menu/`` documentado en
   UC_PERM_08 (extensión).
5. ``rbac-implementation-guide.rst`` §"Q9 — MenuItem UI
   metadata layer" extendido.
6. Frontend pattern ALL_NAV_LINKS + capability filter
   documentado.
7. Tests guardrail I-1..I-4 verbatim.

## Sección 2 — Key Ideas

Las tres ideas centrales que ordenan toda la estrategia:

### KI-1 — Lifecycle-Managed Wrapper UX

``MenuItem`` es un **wrapper UX** sobre ``Function``. Nunca
es fuente de capability. Tiene su propio ciclo de vida
(DRAFT → ACTIVE → DEPRECATED → ARCHIVED) gestionado por
admin (``system_admin`` AGR-010) sin que el usuario final
lo perciba como configuración.

**Por qué wrapper y no standalone:** un ``MenuItem``
standalone (sin FK a ``Function``) reproduce 1:1 el
anti-patrón legacy ``C_MENU2`` donde el menú **era** la
regla de acceso.
Ver ``discover/menuitem-standalone-vs-wrapper-clarification.md``
y ``discover/cmenu2-legacy-archeology.md``.

**Lifecycle-managed vs ALL_NAV_LINKS estático:** el
catálogo necesita CRUD trazado para auditoría,
deprecación gradual y rollback. ALL_NAV_LINKS estático
en frontend funciona como fallback conocido pero no
sustituye al modelo persistido — solo lo refleja en
runtime para usuarios.

### KI-2 — Defense-in-depth (la fuente de verdad es Function)

> *"La fuente de verdad de **'puede acceder'** es siempre
> ``Function`` (vía AGR). ``MenuItem`` solo controla
> **'¿lo muestro en el sidebar?'**."*

**Invariantes (I-1..I-4):**

| # | Invariante | Garantía |
|---|---|---|
| I-1 | Todo MenuItem tiene exactamente una Function | ``OneToOneField(null=False, blank=False)`` |
| I-2 | Borrar Function bloquea/protege el MenuItem | ``on_delete=PROTECT`` (correctivo de v1) |
| I-3 | Function puede existir sin MenuItem | OneToOne opcional desde el lado Function |
| I-4 | Desactivar Function (``is_active=False``) oculta MenuItem | filter del queryset manager (no signal) |

**Endpoint contract (UC_PERM_08 extension):**

```
GET /api/v1/menu/
Returns: { capabilities: [<codename>], menu_items: [{...}] }
```

El frontend consume ``capabilities`` (set de codenames
permitidos) y filtra ``ALL_NAV_LINKS`` localmente. El
backend **siempre** valida cada endpoint protegido por
``Function`` independientemente del menú devuelto.

### KI-3 — Eventual Consistency (cache TTL + invalidación explícita)

Cache de capabilities y menú con **TTL 300s** + **invalidación
explícita** dentro del UC transaccional (no signals). Si
el servicio de cache falla durante invalidación, el UC
**continúa** (degraded mode) emitiendo telemetría
obligatoria.

**Trade-off aceptado:** un usuario puede ver el menú con
una capability eliminada por hasta TTL segundos tras la
revocación. La defensa real (la verificación contra
``Function`` en cada endpoint) sigue siendo strong-consistent
porque consulta DB directamente sin pasar por cache de
menú.

## Sección 3 — Fundamental Decisions (P1-P4 confirmadas)

Decisiones cerradas en
``discover/final-decisions-p1-p4-and-pending-items.md``:

| ID | Decisión | Estado |
|---|---|---|
| P1 | ``MenuItem`` es wrapper UX sobre ``Function`` con OneToOneField, ``on_delete=PROTECT``, lifecycle DRAFT/ACTIVE/DEPRECATED/ARCHIVED | **Confirmada** |
| P2 | Frontend usa ALL_NAV_LINKS + filtro por capabilities; backend serve ``GET /api/v1/menu/`` flat con ``capabilities[]`` y ``menu_items[]`` | **Confirmada** |
| P3 | ``UserCapabilityResolver`` con O(1) query indexada (P95 ≤ 20ms cache MISS, ≤ 5ms cache HIT) | **Confirmada** |
| P4 | Cache TTL 300s con invalidación explícita en UCs transaccionales (no signals) | **Confirmada** |

### P1 — Modelo

```python
class MenuItem(models.Model):
    function = models.OneToOneField(
        Function,
        on_delete=models.PROTECT,           # cambio v1 → v2: PROTECT, no CASCADE
        related_name="menu_item",
    )
    display_label = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True)
    display_order = models.IntegerField(default=0)
    route_path = models.URLField(max_length=200)
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("DRAFT", "Borrador"),
            ("ACTIVE", "Activo"),
            ("DEPRECATED", "Deprecado"),
            ("ARCHIVED", "Archivado"),
        ],
        default="DRAFT",
    )
    deprecated_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name="menu_items_created",
    )

    class Meta:
        db_table = "menu_items"
        ordering = ("display_order",)
        indexes = [
            models.Index(fields=("status",)),
            models.Index(fields=("status", "display_order")),
            models.Index(fields=("deprecated_at",)),
        ]
```

### P2 — Endpoint

```
GET /api/v1/menu/
Authorization: Bearer <jwt>

200 OK
{
  "capabilities": ["view_reports", "manage_menu_catalog", ...],
  "menu_items": [
    {
      "id": 12,
      "codename": "view_reports",
      "display_label": "Mis Reportes",
      "icon": "BarChartIcon",
      "route_path": "/reports",
      "display_order": 10,
      "parent_id": null,
      "status": "ACTIVE"
    }
  ]
}
```

Estructura **flat** (no jerárquica). Frontend reconstruye
árbol vía ``parent_id`` solo si necesita render anidado.

### P3 — UserCapabilityResolver

```python
class UserCapabilityResolver:
    @staticmethod
    def resolve(user) -> set[str]:
        if not user or not user.is_authenticated:
            return set()
        now = timezone.now()
        codenames = (
            Function.objects
            .filter(is_active=True)
            .filter(access_groups__useraccessgroupassignment__user=user)
            .filter(
                Q(access_groups__useraccessgroupassignment__expires_at__isnull=True)
                | Q(access_groups__useraccessgroupassignment__expires_at__gt=now)
            )
            .values_list("codename", flat=True)
            .distinct()
        )
        return set(codenames)
```

**Índices que sostienen P95 ≤ 20ms** (13 totales en 4 tablas):

- ``UserAccessGroupAssignment``: 4 índices (user, group, user+expires_at, expires_at).
- ``FunctionGroupMembership``: 2 índices (group, function).
- ``Function``: 4 índices (codename, is_active, module, codename+is_active).
- ``MenuItem``: 3 índices (status, status+display_order, deprecated_at).

Detalle verbatim en ``discover/final-decisions-p1-p4-and-pending-items.md`` §1.

### P4 — Política de cache

| Item | Decisión |
|---|---|
| TTL | 300s |
| Key pattern | ``caps:user:{id}`` |
| Invalidación | Explícita en UC transaccional (post-COMMIT) |
| Falla del servicio de cache | **Degraded mode** — UC continúa, log + telemetría |
| Race condition (TTL stale) | Aceptado (defense-in-depth en endpoint absorbe) |

> Cláusula STD-010: "el servicio de cache" / "Planificador
> de Tareas" en narrativa UC. La elección concreta (Redis,
> Celery beat) vive en ``arquitectura-tecnica/`` y en
> ``implementacion-tecnica.rst`` por UC.

### Items pendientes resueltos

| # | Item | Resolución |
|---|---|---|
| 1 | Índices exactos | 13 índices definidos verbatim |
| 2 | Comportamiento del servicio de cache ante falla | Degraded mode + telemetría obligatoria + ADR-BACK-009 (nuevo) |
| 3 | Política tiempo DEPRECATED | 30d recomendado, warning 30d / critical 90d, NO auto-archive, Planificador de Tareas con job diario |

## Sección 4 — Technology Stack

> **Nota STD-010:** los nombres concretos de la sección
> 4.1 son **decisiones de implementación** y viven en
> ``source/arquitectura-tecnica/`` o
> ``implementacion-tecnica.rst`` por UC. La narrativa UC
> usa los términos canónicos de la sección 4.2.

### 4.1 Tecnologías concretas (arquitectura-técnica)

| Capa | Tecnología | Versión |
|---|---|---|
| Backend framework | Django + DRF | (versión del proyecto) |
| Permission backend | Custom (FunctionAuthBackend) | — |
| Repositorio operacional | PostgreSQL | (versión del proyecto) |
| Servicio de cache | Redis | 7+ |
| Planificador de Tareas | Celery beat | (versión del proyecto) |
| Frontend framework | React | (versión del proyecto) |
| Gestor de Estado | (TBD — no decidido en este WP) | — |
| Migrations | Django RunPython data migration (canónica) + management command (wrapper) | — |

### 4.2 Vocabulario canónico (narrativa UC, STD-010 §3)

| Concreto (4.1) | Canónico (UC narrative) |
|---|---|
| Django + DRF | Servicio de Aplicación |
| PostgreSQL | repositorio operacional / Almacén de Datos |
| Redis | el servicio de cache |
| Celery beat | el Planificador de Tareas |
| React | la Interfaz de Usuario |
| FunctionAuthBackend | el Backend de Permisos |

### 4.3 Naming conventions

| Capa | Idioma | Ejemplo |
|---|---|---|
| Narrativa UC | Español (canónico STD-010) | "el servicio de cache" |
| Modelo de dominio (clases Python) | Inglés | ``MenuItem``, ``Function``, ``AccessGroup``, ``UserCapabilityResolver`` |
| Codenames de Function | Inglés snake_case | ``view_reports``, ``manage_menu_catalog`` |
| Identifiers DB heredados | Español (vocabulario de dominio) | ``pipeline_runs.estado`` |

## Sección 5 — Architecture Patterns

### AP-1 — Wrapper UX over Authorization Source

``MenuItem`` (UX) wraps ``Function`` (authorization). Two
layers, one direction: UX depende de auth, auth nunca
depende de UX.

```
┌──────────────────┐                ┌──────────────────┐
│   MenuItem (UX)  │  --1:1 PROTECT->│  Function (auth) │
│  status, label   │                │  codename, module │
│  display_order   │                │  is_active        │
└──────────────────┘                └──────────────────┘
                                           │
                                           │ M:N
                                           ▼
                                    ┌──────────────────┐
                                    │  AccessGroup     │
                                    │  (AGR-001..012)  │
                                    └──────────────────┘
                                           │
                                           │ M:N
                                           ▼
                                    ┌──────────────────┐
                                    │     User         │
                                    └──────────────────┘
```

### AP-2 — Defense-in-depth con derived UI

| Capa | Verifica | Stronk-consistent |
|---|---|---|
| Frontend filter (ALL_NAV_LINKS) | Capabilities en token | Eventual (cache TTL) |
| Endpoint backend (Django middleware) | ``Function.codename`` vía ``UserCapabilityResolver`` | Eventual (cache TTL) |
| DB constraint (FK + check) | Estado real | **Strong** (DB) |

Una capability revocada se ve por la UI hasta el TTL del
cache; pero el endpoint **siempre** vuelve a verificar
contra DB en el peor caso (cache MISS).

### AP-3 — Eventual Consistency con escape hatch

```
UC transaccional
┌────────────────────────────────────┐
│ BEGIN TRANSACTION                  │
│   INSERT/UPDATE permission         │
│ COMMIT                             │
│ try:                               │
│   cache.delete("caps:user:{id}")   │
│ except CacheError:                 │
│   logger.error(...)                │
│   metrics.increment("cache.fail")  │
│   # UC succeeds — degraded mode    │
└────────────────────────────────────┘
```

### AP-4 — Custom RBAC sin auth.Group (ADR-BACK-007)

``Function`` y ``AccessGroup`` son modelos propios. NO se
usa ``django.contrib.auth.Permission``/``Group``. El
``FunctionAuthBackend`` resuelve permisos via codename.

### AP-5 — Modelo flat sin jerarquía de permisos (ADR-BACK-001)

Una ``Function`` no hereda de otra. ``parent_id`` en
``MenuItem`` es **override visual**, no jerarquía de
permisos. CNST-029 (RBAC modelo plano) preservado.

### AP-6 — Lifecycle-managed catalog

| Estado | Visible al user | Accesible (capability) | Editable (admin) |
|---|---|---|---|
| DRAFT | No | Sí (URL directa) | Sí |
| ACTIVE | Sí | Sí | Sí |
| DEPRECATED | Sí (tag legacy) | Sí | Sí |
| ARCHIVED | No | Sí (URL directa) | Solo reactivar |

Transiciones documentadas en UC_ADM_05 (``manage_menu_lifecycle``).

### AP-7 — Resolver pattern + indexed query

``UserCapabilityResolver.resolve(user)`` es el único punto
de cómputo. Endpoints, middlewares y signals consumen
``resolve()``, nunca calculan capabilities ad-hoc.

## Sección 6 — Adherence to Constraints

### BR-012 (Usuario Segmento Único)

| Aspecto | Cumplimiento |
|---|---|
| ``segment_id`` permanente | El diseño NO modifica BR-012 — ``MenuItem`` es independiente de ``segment_id`` |
| No switchable en runtime | Preservado — no hay context-switch de menú por segmento |

**Decisión interpretativa documentada:** ``ID_CONVENIO``
del legacy NO tiene equivalente directo en v5.6.0 porque
era contexto switchable, mientras ``segment_id`` es
permanente. Detalle en
``discover/menu-v560-design-and-id-convenio-equivalent.md``.

### CNST-029 (RBAC modelo plano)

| Aspecto | Cumplimiento |
|---|---|
| Sin jerarquía de Function | ``Function`` no tiene FK a sí misma |
| Sin herencia de permisos | ``MenuItem.parent_id`` es UI, no permiso |
| Single role per assignment | Preservado (UAGA con expires_at) |

### CNST-032 (Reescritura propuesta)

**Versión actual:** prohíbe que el menú sea fuente de
capability.

**Versión v2.0.0 propuesta** (a producir en Phase 7):
prohíbe explícitamente:

1. ``MenuItem`` standalone (sin FK a ``Function``).
2. ``MenuItem`` con ``codename`` propio que no exista en
   ``Function``.
3. Frontend que pinte un item de menú sin verificar
   capability del usuario.

### ADR-BACK-001 (Grupos funcionales sin jerarquía)

Preservado: el diseño no introduce herencia entre
``AccessGroup`` ni entre ``Function``. ``MenuItem.parent``
es exclusivamente ordenamiento visual.

### ADR-BACK-007 (RBAC custom vs auth.Group)

Preservado: no se usa ``django.contrib.auth.Group``. El
``FunctionAuthBackend`` sigue siendo el único resolver.

### ADR-BACK-008 (nuevo, a producir en Phase 7)

> *"MenuItem como wrapper UX sobre Function — prohibición
> explícita de Diseño A standalone."*

### ADR-BACK-009 (nuevo, a producir en Phase 7)

> *"Cache de capabilities — degraded mode ante falla del
> servicio de cache, telemetría obligatoria."*

### STD-010 (Vocabulario abstracto)

Cumplimiento explícito en este WP:

- Audit padre: ``discover/std-010-vocabulario-abstracto-audit.md``.
- Audit corpus + correcciones aplicadas:
  WP ``2026-05-06-23-25-08-std-010-corpus-compliance``.
- Cláusula de filtro WP → UC en Phase 7 (A-1..A-7 del
  audit padre).

### UC_PERM_08 §10 (Generar Menu Dinámico)

Compatible. La extensión documenta el endpoint
``GET /api/v1/menu/`` y refina la respuesta como flat
``{capabilities, menu_items}``. No reescribe la lógica
existente.

## Sección 7 — Roadmap Phase 7 DESIGN

9 artefactos a producir, ordenados por dependencia:

| Orden | Artefacto | Tipo | Dependencias |
|---|---|---|---|
| 1 | ADR-BACK-008 (MenuItem wrapper UX) | ADR backend | Decisiones P1 |
| 2 | ADR-BACK-009 (Cache degraded mode) | ADR backend | Decisión P4 |
| 3 | CNST-032 v2.0.0 (reescritura) | Constraint normativa | ADR-BACK-008 |
| 4 | ``rbac-implementation-guide.rst`` §Q9 ext. | Guía técnica | ADR-BACK-008, P1, P3 |
| 5 | UC_ADM_04 (manage_menu_catalog) | UC narrativa | Modelo P1 |
| 6 | UC_ADM_05 (manage_menu_lifecycle) | UC narrativa | UC_ADM_04 |
| 7 | UC_PERM_08 extensión (endpoint GET /api/v1/menu/) | UC update | P2 |
| 8 | ``arquitectura-tecnica/cache-strategy.rst`` (nueva) | Tech-arq | P4, ADR-BACK-009 |
| 9 | ``arquitectura-tecnica/scheduled-tasks.rst`` (nueva o ext.) | Tech-arq | Política DEPRECATED |

**Filtro STD-010 obligatorio antes de cada commit en
Phase 7:**

```bash
grep -rE "bcrypt|React|MySQL|MariaDB|Celery|mod_wsgi|simplejwt|OperationalError|Pillow|Redis" \
  source/requisitos/casos-uso/menu/ \
  --include="*.rst" \
  --exclude="implementacion-tecnica.rst" \
  --exclude="testing.rst"
```

Resultado vacío = conforme.

## Sección 8 — Traceability matrix

| Strategy element | Origen (DISCOVER) | Constraint normativa | Stage que lo materializa |
|---|---|---|---|
| KI-1 Wrapper UX | ``menuitem-standalone-vs-wrapper-clarification.md`` §1 | CNST-032 | Phase 7 — ADR-BACK-008 |
| KI-1 Lifecycle managed | ``lifecycle-managed-menu-vs-static-analysis.md`` Opción 2 | — | Phase 7 — UC_ADM_05 |
| KI-2 Defense-in-depth | ``menuitem-standalone-vs-wrapper-clarification.md`` §3 | UC_PERM_08 §10 | Phase 7 — UC_PERM_08 ext. |
| KI-3 Eventual consistency | ``final-decisions-p1-p4-and-pending-items.md`` §3 | — | Phase 7 — ADR-BACK-009 |
| P1 Modelo MenuItem | ``menuitem-design-corrections-v2.md`` G-1..G-4 | CNST-029, ADR-BACK-001 | Phase 7 — modelo en rbac-impl-guide |
| P2 Endpoint flat | ``menuitem-design-corrections.md`` C-1..C-4 + v2 G-3 | UC_PERM_08 | Phase 7 — UC_PERM_08 ext. |
| P3 UserCapabilityResolver | ``menuitem-design-corrections-v2.md`` G-1 + ``final-decisions-p1-p4`` §1 | ADR-BACK-007 | Phase 7 — rbac-impl-guide §Q9 |
| P4 Cache TTL + invalidación | ``final-decisions-p1-p4-and-pending-items.md`` §3 | — | Phase 7 — ADR-BACK-009 + cache-strategy.rst |
| Indices (13 totales) | ``final-decisions-p1-p4-and-pending-items.md`` §1 | — | Phase 7 — modelo en rbac-impl-guide |
| DEPRECATED policy | ``final-decisions-p1-p4-and-pending-items.md`` §4 | — | Phase 7 — UC_ADM_05 + scheduled-tasks.rst |
| STD-010 compliance | ``std-010-vocabulario-abstracto-audit.md`` + WP corpus-compliance | STD-010 | Phase 7 ongoing (filtro pre-commit) |
| segment_id no switchable | ``menu-v560-design-and-id-convenio-equivalent.md`` | BR-012 | Phase 7 — UC_PERM_08 ext. (clarification) |
| Legacy C_MENU2 anti-pattern | ``cmenu2-legacy-archeology.md`` + ``inserta-modulos-menu-sql-analysis.md`` + ``index-asp-legacy-render-analysis.md`` | CNST-032 | Phase 7 — ADR-BACK-008 (rationale) |

## Sección 9 — Evidence Classification

Cada elemento de la estrategia clasificado según
``evidence-classification.md``:

### OBSERVABLE (PROVEN)

- Schema legacy ``C_MENU2``, ``BD_MENU2``, ``BD_MENU_CONVENIO``
  reconstruido desde el SQL real (``inserta-modulos-menu-sql-analysis.md``,
  ``cmenu2-legacy-archeology.md``).
- Render legacy ASP analizado del archivo real
  (``index-asp-legacy-render-analysis.md``).
- ``UserCapabilityResolver`` query producida con tool_use y
  validada en EXPLAIN ANALYZE simulada
  (``final-decisions-p1-p4-and-pending-items.md`` §1).
- 13 índices definidos verbatim con campo y tabla.
- STD-010 v1.0.0 leído del archivo del proyecto
  (``source/normativa/estandares/std-010-vocabulario-abstracto.rst``).
- Build Sphinx strict EXIT=0 post-correcciones STD-010
  (log ``2026-05-06-23-25-08-std-010-corpus-compliance/discover/build-logs/``).

### INFERRED

- KI-1 (wrapper UX) inferido desde la combinación de:
  ADR-BACK-001 + ADR-BACK-007 + análisis de regresión
  legacy. Razonamiento explícito en
  ``menuitem-standalone-vs-wrapper-clarification.md`` §4-5.
- P95 ≤ 20ms inferido desde modelo de query +
  índices + supuesto razonable de carga (sin medición
  empírica en este WP).
- Política 30d/90d DEPRECATED inferida de buenas
  prácticas, no de SLA contractual.

### SPECULATIVE (no usadas como fundamento de gate)

- Cantidad real de ``MenuItem`` ACTIVE esperados (TBD —
  depende del catálogo definitivo a producir en Phase 7).
- Comportamiento real bajo carga de `n` usuarios
  concurrentes (requeriría Phase 9 PILOT con benchmark).
- Decisión de ``Gestor de Estado`` concreto en frontend
  (no decidido en este WP — fuera de alcance).

## Sección 10 — Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Phase 7 propaga "Celery"/"Redis" a narrativa UC | Media | Medio | Filtro STD-010 §6 pre-commit + checklist A-1..A-7 |
| Migración en proyectos con ``Function`` huérfanas | Baja | Alto | RunPython data migration valida 1:1 antes de crear FK |
| Regresión a Diseño A standalone en futuras iteraciones | Baja | **Crítico** | Test guardrail I-1..I-4 verbatim + CNST-032 v2.0.0 + ADR-BACK-008 |
| Cache stale tras revocación masiva | Media | Bajo | Defense-in-depth absorbe — endpoint siempre verifica |
| Falla del servicio de cache afecta UCs | Baja | Medio | Degraded mode + telemetría + alertas (ADR-BACK-009) |
| MenuItems en DEPRECATED >90d sin acción | Media | Bajo | Planificador de Tareas con notificación a system_admin |

## Sección 11 — Out of scope (NO se decide aquí)

1. Elección concreta de ``Gestor de Estado`` frontend
   (Redux Toolkit, Zustand, MobX, etc.).
2. Migración de datos legacy ``C_MENU2`` → ``MenuItem``
   (no aplica — sistema legacy no se importa).
3. Internacionalización de ``display_label`` (i18n).
4. Auditoría de ``Frontend``/``Backend``/``localStorage``
   en STD-010 (Tier 3 candidates — WP separado).
5. Reescritura de UCs existentes para alinear vocabulario
   STD-010 fuera del scope de este WP (corpus compliance
   ya aplicado en WP hermano
   ``2026-05-06-23-25-08-std-010-corpus-compliance``).

## Sección 12 — Exit criteria de Phase 5

- [x] Key Ideas (KI-1, KI-2, KI-3) documentadas.
- [x] Fundamental Decisions (P1-P4) consolidadas.
- [x] Technology Stack mapeado a vocabulario canónico STD-010.
- [x] Architecture Patterns (AP-1..AP-7) descritos.
- [x] Adherence to Constraints (BR-012, CNST-029, CNST-032,
  ADR-BACK-001, ADR-BACK-007, ADR-BACK-008/009, STD-010,
  UC_PERM_08) documentado con cumplimiento explícito.
- [x] Roadmap Phase 7 con 9 artefactos ordenados por
  dependencia.
- [x] Traceability matrix strategy → discover artefactos →
  constraints → Phase 7 outputs.
- [x] Evidence classification OBSERVABLE/INFERRED/SPECULATIVE
  aplicada.
- [x] Riesgos y mitigaciones identificados.
- [x] Out-of-scope explícito.

**Phase 5 STRATEGY listo para gate Stage→Stage.** Si el
ejecutor aprueba, siguiente paso es Phase 7 DESIGN
ejecutando el roadmap §7.

## Refs

### Discover artefactos consolidados (orden cronológico del WP)

- ``discover/menu-rbac-user-scope-docs-analysis.md``
  (síntesis principal — 8 gap analyses).
- ``discover/cmenu2-legacy-archeology.md``.
- ``discover/inserta-modulos-menu-sql-analysis.md``.
- ``discover/index-asp-legacy-render-analysis.md``.
- ``discover/menu-v560-design-and-id-convenio-equivalent.md``.
- ``discover/lifecycle-managed-menu-vs-static-analysis.md``.
- ``discover/menuitem-standalone-vs-wrapper-clarification.md``.
- ``discover/menuitem-design-corrections.md``.
- ``discover/menuitem-design-corrections-v2.md``.
- ``discover/final-decisions-p1-p4-and-pending-items.md``.
- ``discover/std-010-vocabulario-abstracto-audit.md``.

### WP hermano (corpus compliance)

- ``2026-05-06-23-25-08-std-010-corpus-compliance/`` —
  audit + 7 correcciones aplicadas + build EXIT=0.

### Constraints normativas

- BR-012 — :doc:`/requisitos/reglas-negocio/usuario-segmento-unico`.
- CNST-029 — :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
- CNST-032 — :doc:`/normativa/restricciones/cnst-032-menu-no-fuente-permiso`.
- ADR-BACK-001 — :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`.
- ADR-BACK-007 — :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
- STD-010 — :doc:`/normativa/estandares/std-010-vocabulario-abstracto`.
- UC_PERM_08 — :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.
- Catálogo de Function — :doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones`.
