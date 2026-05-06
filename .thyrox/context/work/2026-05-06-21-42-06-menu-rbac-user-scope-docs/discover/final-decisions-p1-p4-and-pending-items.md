```yml
created_at: 2026-05-07 00:45:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/menuitem-design-corrections-v2.md
```

# Confirmación final P1-P4 + resolución de 3 items pendientes

## Trigger

El ejecutor confirmó las 4 respuestas (Opción 2, 2 UCs, NO
multi-tenancy, 4 estados) e identificó **3 items pendientes**
antes de cerrar Phase 5 STRATEGY:

1. Definir índices exactos en
   ``UserAccessGroupAssignment`` y ``FunctionGroupMembership``
   (Backend, Alta).
2. Documentar comportamiento del endpoint cuando Redis falla
   durante invalidación de cache (Arquitectura, Media).
3. Establecer política de tiempo máximo en estado DEPRECATED
   (Negocio + Backend, Media).

Este documento resuelve los 3 items con propuestas concretas
para la confirmación final del ejecutor.

## Sección 1 — Items confirmados (sin cambios)

| # | Decisión | Estado |
|---|---|---|
| **P1** | Opción 2 — MenuItem 1:1 con Function como wrapper UX obligatorio | ✅ Confirmado |
| **P2** | 2 UCs nuevos: UC_ADM_04 (manage_menu_catalog) + UC_ADM_05 (manage_menu_lifecycle) | ✅ Confirmado |
| **P3** | NO multi-tenancy en MenuItem (preserva BR-012) | ✅ Confirmado |
| **P4** | 4 estados: DRAFT, ACTIVE, DEPRECATED, ARCHIVED | ✅ Confirmado |

MOD_Admin pasa de 3 a **5 funciones** activas.

## Sección 2 — Item pendiente #1 (Alta prioridad): Índices exactos

### Diagnóstico

El SLO de ``UserCapabilityResolver`` (P95 ≤ 20ms) asume índices
correctos. Sin definirlos explícitamente, no es enforced.

### Propuesta de índices

#### `UserAccessGroupAssignment`

```python
class UserAccessGroupAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_group = models.ForeignKey(
        AccessGroup, on_delete=models.PROTECT,
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    assigned_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name="assignments_made",
    )

    class Meta:
        db_table = "user_function_group_assignments"
        unique_together = ("user", "access_group")
        indexes = [
            # IDX_UAGA_USER: lookup por user (filtrar assignments del user)
            models.Index(
                fields=("user",),
                name="idx_uaga_user",
            ),
            # IDX_UAGA_USER_EXPIRES: filtrar por user + expires_at
            # (el resolver usa: user=X AND (expires IS NULL OR expires > now))
            models.Index(
                fields=("user", "expires_at"),
                name="idx_uaga_user_expires",
            ),
            # IDX_UAGA_AG: join inverse desde AccessGroup
            models.Index(
                fields=("access_group",),
                name="idx_uaga_access_group",
            ),
            # IDX_UAGA_EXPIRES: para cleanup batch jobs (delete expired)
            models.Index(
                fields=("expires_at",),
                name="idx_uaga_expires_at",
                condition=models.Q(expires_at__isnull=False),
            ),
        ]
```

#### `FunctionGroupMembership`

```python
class FunctionGroupMembership(models.Model):
    group = models.ForeignKey(AccessGroup, on_delete=models.CASCADE)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "function_group_membership"
        unique_together = ("group", "function")
        indexes = [
            # IDX_FGM_GROUP_FUNCTION: lookup primary del JOIN
            # (UCQ: AccessGroup → Function via M2M)
            models.Index(
                fields=("group", "function"),
                name="idx_fgm_group_function",
            ),
            # IDX_FGM_FUNCTION: join inverse desde Function
            models.Index(
                fields=("function",),
                name="idx_fgm_function",
            ),
        ]
```

#### `Function`

```python
class Function(models.Model):
    # ... campos ya documentados

    class Meta:
        db_table = "functions"
        ordering = ("module", "codename")
        indexes = [
            # IDX_FUNCTION_CODENAME: lookup por codename (PRIMARY use case)
            # NOTA: codename ya tiene unique=True que crea índice implícito,
            # pero declaramos explícito por documentación.
            models.Index(
                fields=("codename",),
                name="idx_function_codename",
            ),
            # IDX_FUNCTION_MODULE: filtros por módulo
            models.Index(
                fields=("module",),
                name="idx_function_module",
            ),
            # IDX_FUNCTION_ACTIVE: filtrar visible items
            # (UCQ: function__is_active=True)
            models.Index(
                fields=("is_active",),
                name="idx_function_active",
            ),
            # IDX_FUNCTION_ACTIVE_MODULE: combinado para
            # filtros típicos del admin
            models.Index(
                fields=("is_active", "module"),
                name="idx_function_active_module",
            ),
        ]
```

#### `MenuItem`

```python
class MenuItem(models.Model):
    # ... campos ya documentados

    class Meta:
        db_table = "menu_items"
        ordering = ("display_order",)
        indexes = [
            # IDX_MI_STATUS: filtrar items renderable
            # (UCQ: status IN [ACTIVE, DEPRECATED])
            models.Index(
                fields=("status",),
                name="idx_mi_status",
            ),
            # IDX_MI_PARENT_ORDER: render del árbol ordenado
            models.Index(
                fields=("parent", "display_order"),
                name="idx_mi_parent_order",
            ),
            # IDX_MI_FUNCTION: lookup inverse
            # (cuando Function se desactiva, encontrar su MenuItem)
            models.Index(
                fields=("function",),
                name="idx_mi_function",
            ),
        ]
```

### Verificación de cobertura

**Query crítica de `UserCapabilityResolver.resolve(user)`:**

```sql
SELECT DISTINCT f.codename
FROM functions f
INNER JOIN function_group_membership fgm ON fgm.function_id = f.id
INNER JOIN access_groups ag ON ag.id = fgm.group_id
INNER JOIN user_function_group_assignments uaga ON uaga.access_group_id = ag.id
WHERE f.is_active = true
  AND uaga.user_id = ?
  AND (uaga.expires_at IS NULL OR uaga.expires_at > NOW());
```

**Plan de ejecución esperado con índices propuestos:**

1. ``uaga`` filter por ``user_id`` → usa ``idx_uaga_user_expires``
   (cobertura compuesta).
2. ``ag`` join por ``access_group_id`` → usa PK + cascade.
3. ``fgm`` join por ``group_id`` → usa ``idx_fgm_group_function``.
4. ``f`` filter por ``is_active = true`` → usa
   ``idx_function_active``.

Total queries: 1 (single SELECT con 4 INNER JOINs).
Tiempo estimado con índices: ~5-15ms en BD local con 64
funciones activas + 12 AccessGroups + 100-1000 user assignments.

### Tests de cobertura de índices

```python
@pytest.mark.django_db
def test_indexes_exist_for_capability_resolver():
    """Verifica que todos los índices documentados existen en DB."""
    expected_indexes = {
        "user_function_group_assignments": [
            "idx_uaga_user", "idx_uaga_user_expires",
            "idx_uaga_access_group", "idx_uaga_expires_at",
        ],
        "function_group_membership": [
            "idx_fgm_group_function", "idx_fgm_function",
        ],
        "functions": [
            "idx_function_codename", "idx_function_module",
            "idx_function_active", "idx_function_active_module",
        ],
        "menu_items": [
            "idx_mi_status", "idx_mi_parent_order", "idx_mi_function",
        ],
    }

    for table, indexes in expected_indexes.items():
        existing = list_indexes(table)  # raw SQL helper
        for idx_name in indexes:
            assert idx_name in existing, f"Missing index: {table}.{idx_name}"
```

## Sección 3 — Item pendiente #2 (Media): Comportamiento ante Redis falla

### Diagnóstico

Si Redis no está disponible cuando se ejecuta la invalidación
dentro de una transición atómica (G-3), el comportamiento no
estaba definido. Dos opciones:

- **Opción A — Rollback de la transacción**: la transición
  falla, el estado del MenuItem no cambia, el user recibe
  error. Garantiza consistencia.
- **Opción B — Degraded mode**: la transición se completa, el
  cache queda stale hasta TTL (5min), el user puede ver el
  menú anterior por hasta 5 minutos. Garantiza availability.

### Análisis de trade-offs

| Aspecto | Opción A (Rollback) | Opción B (Degraded) |
|---|---|---|
| Consistencia | Inmediata | Eventual (max 5 min) |
| Availability del UC | Bloqueado si Redis caído | UC sigue funcionando |
| Riesgo de seguridad | Bajo (estado consistente) | Bajo-Medio (item stale visible 5min) |
| UX del admin | Error operacional ("vuelva a intentar") | Operación confirmada (con cache stale) |
| Resiliencia | Baja (Redis es SPOF) | Alta |
| Complejidad de código | Baja (raise) | Media (try/except + log + circuit breaker) |
| Patrón industria | Atomic-strict | Eventual consistency (más común) |

### Decisión recomendada

**Opción B — Degraded mode con telemetría obligatoria.**

Razones:

1. La transición es **atómica en BD** (es lo que importa para
   audit/data integrity). El cache es **derivado**.
2. Stale por max 5 minutos NO es problema de seguridad real:
   los users con la capability pueden ver el item viejo, pero
   el endpoint sigue protegido por permission backend en cada
   request. Defense-in-depth no se rompe.
3. Bloquear UCs cuando Redis cae transforma cache de
   *optimization layer* a *critical dependency* — anti-patrón.
4. El patrón industrial estándar es eventual consistency con
   degradación graceful.

### Implementación

```python
class MenuItemLifecycleService:

    @staticmethod
    @transaction.atomic
    def transition(menu_item, target, by_user):
        # ... validar + cambiar status + audit log ...
        menu_item.save(update_fields=("status", "updated_at"))

        # Invalidación con degraded mode
        cls._invalidate_caches_for_function(menu_item.function)

        return menu_item

    @staticmethod
    def _invalidate_caches_for_function(function):
        """Invalida cache. Si Redis falla, log + telemetría + continúa.

        Trade-off: cache stale por max 5 min (TTL) vs UC bloqueado.
        Decisión per ADR-BACK-009: preferir availability del UC.
        """
        try:
            user_ids = list(
                User.objects.filter(
                    useraccessgroupassignment__access_group__functions=function,
                ).values_list("id", flat=True).distinct()
            )

            for user_id in user_ids:
                cache.delete(f"menu:user:{user_id}")
                cache.delete(f"caps:user:{user_id}")

        except CacheError as e:
            # Redis no disponible — continúa, log obligatorio
            logger.error(
                "cache_invalidation_failed",
                extra={
                    "function_codename": function.codename,
                    "error": str(e),
                    "fallback": "stale_until_ttl",
                    "ttl_seconds": 300,
                },
            )
            # Telemetría: contador de fallos para alerting
            metrics.counter(
                "menu_cache_invalidation_failures",
                tags={"function": function.codename},
            ).inc()
            # NO raise — degraded mode aceptado
```

### Compromisos de la decisión

| Compromiso | Mitigación |
|---|---|
| Cache stale por max 5 min (TTL) | TTL corto (5 min); usuario puede force-refresh con header `Cache-Control: no-cache` |
| Invalidación silenciosamente perdida | Telemetría obligatoria + alert si counter > threshold por minuto |
| Race condition: user invalida + Redis falla + Redis recupera + user lee stale | Aceptado por TTL corto; si crítico, agregar `cache.set` con timestamp para detect-and-evict en GET |

### Documentación obligatoria en ADR-BACK-009

> *"En caso de falla de Redis durante invalidación de cache,
> la transición se completa exitosamente y el cache queda
> stale hasta que el TTL expire (max 5 minutos). El sistema
> emite log de error + métrica
> ``menu_cache_invalidation_failures`` para alerting. Esta
> decisión preserva availability del UC sobre consistencia
> inmediata, asumiendo que defense-in-depth garantiza
> seguridad real (cada request al endpoint verifica permission
> backend independientemente del cache de menú)."*

## Sección 4 — Item pendiente #3 (Media): Política de tiempo en DEPRECATED

### Diagnóstico

El estado DEPRECATED es transitorio por diseño — su propósito
es **avisar a usuarios** durante una ventana de migración antes
de archivar. Sin política de tiempo máximo, se vuelve "estado
zombie" donde items quedan deprecated indefinidamente.

### Propuesta de política

**Política recomendada:**

| Aspecto | Valor |
|---|---|
| Tiempo recomendado en DEPRECATED | **30 días** |
| Tiempo mínimo (no menor que) | 7 días |
| Tiempo máximo (alerta) | 90 días |
| Acción al exceder | Alert al `system_admin` (AGR-010) — no auto-archive |

### Implementación

#### Campos adicionales en `MenuItem`

```python
class MenuItem(models.Model):
    # ... campos ya documentados

    # Audit de transiciones temporales
    deprecated_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    # ...
```

Estos campos se actualizan en `MenuItemLifecycleService.transition`:

```python
@staticmethod
@transaction.atomic
def transition(menu_item, target, by_user):
    # ... validación y permission check ...

    now = timezone.now()
    menu_item.status = target

    if target == "DEPRECATED":
        menu_item.deprecated_at = now
    elif target == "ARCHIVED":
        menu_item.archived_at = now

    menu_item.save(update_fields=(
        "status", "updated_at", "deprecated_at", "archived_at",
    ))
    # ... audit + cache invalidation ...
```

#### Job de monitoreo (Celery beat)

```python
# apps/access/tasks.py
from celery import shared_task

DEPRECATED_WARNING_DAYS = 30  # alerta amarilla
DEPRECATED_CRITICAL_DAYS = 90  # alerta roja


@shared_task
def check_deprecated_menu_items():
    """Daily job — alerta si MenuItems llevan demasiado en DEPRECATED."""
    now = timezone.now()
    warning_threshold = now - timedelta(days=DEPRECATED_WARNING_DAYS)
    critical_threshold = now - timedelta(days=DEPRECATED_CRITICAL_DAYS)

    warning_items = MenuItem.objects.filter(
        status="DEPRECATED",
        deprecated_at__lt=warning_threshold,
        deprecated_at__gte=critical_threshold,
    )
    critical_items = MenuItem.objects.filter(
        status="DEPRECATED",
        deprecated_at__lt=critical_threshold,
    )

    if warning_items.exists():
        notify_admins(
            level="WARNING",
            subject=f"{warning_items.count()} MenuItems en DEPRECATED >30d",
            items=list(warning_items.values("id", "display_label",
                                            "deprecated_at")),
        )

    if critical_items.exists():
        notify_admins(
            level="CRITICAL",
            subject=f"{critical_items.count()} MenuItems en DEPRECATED >90d",
            items=list(critical_items.values("id", "display_label",
                                             "deprecated_at")),
        )
```

#### NO auto-archive

**Decisión:** el sistema **NO** archiva automáticamente al
exceder los 90 días. Razones:

- El admin debe **decidir explícitamente** archivar (audit
  trail intacto).
- Auto-archive puede sorprender a users que aún usan el item.
- 90 días es **alerta, no SLA**: hay casos válidos donde el
  item debe vivir más tiempo (compliance, regulación).

El job solo **notifica**, no actúa.

### Documentación en UC_ADM_05

> *"Política de tiempo en DEPRECATED:*
>
> - *Recomendado: 30 días desde transición ACTIVE → DEPRECATED.*
> - *Warning automático: emitido a system_admin via
>   InternalMailbox tras 30 días.*
> - *Critical alert: emitida tras 90 días — requiere acción
>   explícita (archive o reactivar a ACTIVE).*
> - *NO hay auto-archive: la decisión de archivar es siempre
>   manual del system_admin (AGR-010).*"

## Sección 5 — Resumen de los 3 items pendientes resueltos

| # | Item | Resolución |
|---|---|---|
| 1 | Índices exactos | **13 índices definidos** distribuidos en 4 tablas (UAGA: 4, FGM: 2, Function: 4, MenuItem: 3) + test de cobertura verbatim |
| 2 | Comportamiento Redis falla | **Degraded mode** con telemetría obligatoria. Transición no se hace rollback. Documentado en ADR-BACK-009. |
| 3 | Política tiempo DEPRECATED | **30 días recomendado**, warning 30d / critical 90d, NO auto-archive. Job Celery diario + notificación a system_admin. |

## Sección 6 — Estado del WP — listo para Phase 5 STRATEGY

Phase 1 DISCOVER está **completa** con los siguientes
artefactos:

```
discover/
├── menu-rbac-user-scope-docs-analysis.md         (principal)
├── cmenu2-legacy-archeology.md                   (G0 legacy)
├── inserta-modulos-menu-sql-analysis.md          (G1 SQL)
├── index-asp-legacy-render-analysis.md           (G2 ASP render)
├── menu-v560-design-and-id-convenio-equivalent.md (decisiones canónicas)
├── lifecycle-managed-menu-vs-static-analysis.md  (replanteo arquitectónico)
├── menuitem-standalone-vs-wrapper-clarification.md (4 invariantes)
├── menuitem-design-corrections.md                (C-1..C-4)
├── menuitem-design-corrections-v2.md             (G-1..G-4)
└── final-decisions-p1-p4-and-pending-items.md    (este artefacto)
```

Phase 5 STRATEGY puede iniciar con todas las decisiones
arquitectónicas resueltas. Próximo artefacto:
``strategy/menu-rbac-user-scope-solution-strategy.md``.

## Refs

- Análisis padre v2: ``discover/menuitem-design-corrections-v2.md``.
- Análisis padre v1: ``discover/menuitem-design-corrections.md``.
- Análisis padre estructura: ``discover/menuitem-standalone-vs-wrapper-clarification.md``.
- Lifecycle managed: ``discover/lifecycle-managed-menu-vs-static-analysis.md``.
- Diseño canónico: ``discover/menu-v560-design-and-id-convenio-equivalent.md``.
- Arqueología:

  - ``discover/cmenu2-legacy-archeology.md``
  - ``discover/inserta-modulos-menu-sql-analysis.md``
  - ``discover/index-asp-legacy-render-analysis.md``

- Análisis principal: ``discover/menu-rbac-user-scope-docs-analysis.md``.
- BR-012, ADR-BACK-001, ADR-BACK-007, CNST-029, CNST-032, UC_PERM_08
  (corpus vigente referenciado).
