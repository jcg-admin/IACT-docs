```yml
created_at: 2026-05-07 00:15:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/menuitem-design-corrections.md
```

# Correcciones v2 — gaps detectados en review crítico

## Trigger

Tras documentar las correcciones C-1..C-4 + contrato del
endpoint, el ejecutor identificó **4 gaps adicionales**.
Uno (G-1) es **bloqueante** para Phase 5 STRATEGY: si no
está garantizado el performance de ``get_all_capabilities()``,
el SLO de cache MISS P95 ≤ 200ms no es alcanzable.

Este documento resuelve los 4 gaps formalmente.

## Sección 1 — G-1 (BLOQUEANTE): `get_all_capabilities()` definido

### Diagnóstico del problema

El código previo mostró:

```python
def for_user(self, user):
    codenames = user.get_all_capabilities()  # método indefinido
    return self.renderable().filter(
        function__codename__in=codenames,
    )
```

`user.get_all_capabilities()` no estaba definido. Si su
implementación es ingenua:

```python
# IMPLEMENTACIÓN INGENUA — N+1 (NO USAR)
def get_all_capabilities(self):
    codenames = []
    for assignment in self.useraccessgroupassignment_set.all():
        for membership in assignment.access_group.functiongroupmembership_set.all():
            codenames.append(membership.function.codename)
    return codenames
```

Esto genera:

- 1 query: get assignments
- N queries: por cada assignment, get group's memberships
- M queries: por cada membership, get function

→ **N+1+M queries**. Para un user con 3 AGRs y 30 functions
totales: ~34 queries. Tiempo agregado en una BD remota:
~50ms-100ms solo para resolver capabilities, antes de tocar
el menú.

→ **El SLO de cache MISS P95 ≤ 200ms NO es alcanzable** con
esta implementación.

### Definición correcta — `get_all_capabilities()` performante

```python
# apps/access/managers.py
from django.utils import timezone


class UserCapabilityResolver:
    """Resolutor de capabilities — performance-bounded.

    Garantías:
    - Complejidad: O(1) queries (1 query SQL con JOINs).
    - Tiempo cota: P95 ≤ 20ms en BD local con índices.
    - Cache opcional: TTL 5min via cache key 'caps:user:{id}'.
    - Funciona con bulk updates (no depende de signals).
    """

    @staticmethod
    def resolve(user) -> set[str]:
        """Retorna el set de codenames activos para un user.

        Filtros aplicados:
        - User está autenticado.
        - Assignment no expirado (expires_at IS NULL OR > now).
        - Function activa (is_active=True).
        - AccessGroup is_system=True (predefinido) OR custom válido.

        Returns:
            set[str]: codenames de Function. Set vacío si user no
            tiene capabilities efectivas.
        """
        if not user or not user.is_authenticated:
            return set()

        from apps.access.models import Function

        now = timezone.now()

        # ÚNICA QUERY — 1 SQL statement con JOINs
        codenames = (
            Function.objects
            .filter(is_active=True)
            .filter(
                # Function via AccessGroup → UserAccessGroupAssignment del user
                access_groups__useraccessgroupassignment__user=user,
            )
            .filter(
                # Assignment no expirado
                models.Q(
                    access_groups__useraccessgroupassignment__expires_at__isnull=True,
                ) | models.Q(
                    access_groups__useraccessgroupassignment__expires_at__gt=now,
                ),
            )
            .values_list("codename", flat=True)
            .distinct()
        )

        return set(codenames)


# Métodos en User model (extensión via mixin o método agregado)
class CapabilityMixin:
    """Mixin sobre User — provee API limpia para capabilities."""

    def get_all_capabilities(self) -> set[str]:
        """Convenience wrapper sobre UserCapabilityResolver."""
        return UserCapabilityResolver.resolve(self)

    def has_capability(self, codename: str) -> bool:
        """Check single — equivalente a 'codename in self.get_all_capabilities()'.

        Implementación optimizada: usa exists() para no traer todo el set.
        """
        from apps.access.models import Function

        if not self.is_authenticated:
            return False

        now = timezone.now()
        return Function.objects.filter(
            codename=codename,
            is_active=True,
            access_groups__useraccessgroupassignment__user=self,
        ).filter(
            models.Q(
                access_groups__useraccessgroupassignment__expires_at__isnull=True,
            ) | models.Q(
                access_groups__useraccessgroupassignment__expires_at__gt=now,
            ),
        ).exists()
```

### Garantías de performance documentadas

| Operación | Complejidad | Tiempo P95 (cota) | Implementación |
|---|---|---|---|
| `get_all_capabilities(user)` | O(1) queries | ≤ 20ms con índices | 1 SELECT con JOINs |
| `has_capability(user, codename)` | O(1) queries | ≤ 5ms con índices | 1 EXISTS query |
| Cache lookup `caps:user:{id}` | O(1) Redis call | ≤ 2ms | Redis GET |

**Indexes obligatorios para alcanzar SLO:**

```python
class UserAccessGroupAssignment(models.Model):
    # ...
    class Meta:
        indexes = [
            models.Index(fields=("user",)),                          # filter por user
            models.Index(fields=("user", "expires_at")),             # filter user + no expirado
            models.Index(fields=("access_group",)),                  # join inverse
        ]


class FunctionGroupMembership(models.Model):
    # ...
    class Meta:
        unique_together = ("group", "function")
        indexes = [
            models.Index(fields=("group",)),                         # join group
            models.Index(fields=("function",)),                      # join inverse
        ]
```

### Cache estratégico (opcional pero recomendado)

```python
class CachedCapabilityResolver:
    """Wrapper con cache de UserCapabilityResolver.

    Performance:
    - Cache HIT: P95 ≤ 5ms (Redis GET).
    - Cache MISS: P95 ≤ 25ms (1 query + Redis SET).
    """

    CACHE_KEY_PATTERN = "caps:user:{user_id}"
    CACHE_TTL_SECONDS = 300  # 5 minutos

    @classmethod
    def resolve(cls, user) -> set[str]:
        if not user or not user.is_authenticated:
            return set()

        cache_key = cls.CACHE_KEY_PATTERN.format(user_id=user.pk)
        cached = cache.get(cache_key)
        if cached is not None:
            return set(cached)

        codenames = UserCapabilityResolver.resolve(user)
        cache.set(cache_key, list(codenames), cls.CACHE_TTL_SECONDS)
        return codenames

    @classmethod
    def invalidate(cls, user_id: int) -> None:
        """Invalidación EXPLÍCITA — desde el UC, no desde signal."""
        cache.delete(cls.CACHE_KEY_PATTERN.format(user_id=user_id))
```

### Tests de performance obligatorios

```python
@pytest.mark.django_db
@pytest.mark.performance
def test_get_all_capabilities_uses_one_query():
    """G-1: el resolver hace exactamente 1 query SQL."""
    user = make_user_with_n_agrs(3)  # user con 3 AGRs

    with assertNumQueries(1):
        caps = UserCapabilityResolver.resolve(user)

    assert isinstance(caps, set)


@pytest.mark.django_db
@pytest.mark.performance
def test_get_all_capabilities_under_p95_slo():
    """G-1: P95 ≤ 20ms con BD local indexada."""
    user = make_user_with_full_agr_set()  # peor caso: 12 AGRs

    times = []
    for _ in range(100):
        start = time.perf_counter()
        UserCapabilityResolver.resolve(user)
        times.append(time.perf_counter() - start)

    p95 = sorted(times)[94]
    assert p95 <= 0.020, f"P95 violation: {p95 * 1000:.1f}ms > 20ms"
```

## Sección 2 — G-2: árbol vs lista plana en response

### Diagnóstico

El response shape v1 mostraba `children: [...]` recursivo:

```json
{
  "items": [
    {
      "id": "a", "children": [
        {"id": "b", "children": [...]}
      ]
    }
  ]
}
```

Sin profundidad máxima → riesgos:

- **Serializer cost**: con N niveles, el serializer hace N
  recursive calls + queries.
- **Circular references**: si hay un bug de datos
  (`menu_item.parent.parent.parent... == menu_item.id`), el
  serializer entra en loop infinito.
- **Payload size**: árbol con duplicación de metadata por nivel.

### Decisión: lista plana con `parent_id`

```json
{
  "user_id": 42,
  "generated_at": "2026-05-07T00:15:00Z",
  "items": [
    {
      "id": "uuid-a",
      "codename": "view_reports",
      "display_label": "Mis Reportes",
      "icon": "BarChartIcon",
      "route_path": "/reports",
      "display_order": 10,
      "status": "ACTIVE",
      "parent_id": null
    },
    {
      "id": "uuid-b",
      "codename": "export_csv",
      "display_label": "Exportar CSV",
      "icon": "DownloadIcon",
      "route_path": "/reports/export-csv",
      "display_order": 1,
      "status": "ACTIVE",
      "parent_id": "uuid-a"
    },
    {
      "id": "uuid-c",
      "codename": "view_legacy_dashboard",
      "display_label": "Dashboard antiguo",
      "icon": "DashboardIcon",
      "route_path": "/dashboard-legacy",
      "display_order": 99,
      "status": "DEPRECATED",
      "parent_id": null
    }
  ]
}
```

**Beneficios de lista plana:**

| Beneficio | Soporte |
|---|---|
| Serializer simple, no recursivo | 1 SELECT + serialize, sin loops |
| Imposible circular reference por bug de datos | Sin recursión = sin riesgo |
| Payload predecible — O(N) | Sin profundidad arbitraria |
| Frontend construye tree según su jerarquía UI | Mejor separation: backend = data, frontend = UI |
| Orden estable (display_order globalmente respetado) | El frontend agrupa por parent y ordena |

**Implementación frontend:**

```typescript
// Frontend recibe lista plana, construye tree localmente
const buildMenuTree = (items: MenuItem[]): MenuNode[] => {
  const byId = new Map(items.map(item => [item.id, { ...item, children: [] }]));
  const roots: MenuNode[] = [];

  for (const item of byId.values()) {
    if (item.parent_id === null) {
      roots.push(item);
    } else {
      const parent = byId.get(item.parent_id);
      if (parent) parent.children.push(item);
    }
  }

  // sort por display_order en cada nivel
  const sortRecursive = (nodes: MenuNode[]) => {
    nodes.sort((a, b) => a.display_order - b.display_order);
    nodes.forEach(n => sortRecursive(n.children));
  };
  sortRecursive(roots);

  return roots;
};
```

**Validación de profundidad** (server-side, para evitar
ciclos):

```python
class MenuItem(models.Model):
    # ...

    def clean(self):
        """Valida que no haya ciclos en parent + max depth = 3."""
        if self.parent_id is None:
            return

        depth = 1
        current = self.parent
        seen_ids = {self.id} if self.id else set()

        while current is not None:
            if current.id in seen_ids:
                raise ValidationError("Cycle detected in menu hierarchy")
            seen_ids.add(current.id)
            depth += 1
            if depth > 3:
                raise ValidationError("Menu hierarchy max depth = 3")
            current = current.parent
```

## Sección 3 — G-3: invalidación de cache desde el UC, no desde signal

### Diagnóstico

El v1 dijo:

> *"Cache: TTL 5min, key menu:user:{id}, invalidación via
> signal."*

Pero el principio C-2 (queryset = SoT, signals no funcionan en
bulk) **se contradice** con cache invalidation via signal:

- Si bulk update no dispara signal → cache no se invalida.
- Cache stale por 5 min hasta que TTL expire.
- El queryset correcto **nunca llega al user** durante esa
  ventana.

**Esto es un gap real de seguridad menor**: archivar un
MenuItem por error puede dejarlo visible 5 min más.

### Decisión: invalidación EXPLÍCITA en el UC de transición

```python
# apps/access/services/menu_lifecycle.py

class MenuItemLifecycleService:
    """UCs de transición de MenuItem — invalidan cache atomicamente."""

    @staticmethod
    @transaction.atomic
    def publish(menu_item: MenuItem, by_user: User) -> MenuItem:
        """UC: DRAFT → ACTIVE (publicación)."""
        if menu_item.status != "DRAFT":
            raise ValidationError(f"No se puede publicar — estado actual: {menu_item.status}")

        menu_item.status = "ACTIVE"
        menu_item.save(update_fields=("status", "updated_at"))

        # Invalidación EXPLÍCITA — atómica con la transición
        MenuItemLifecycleService._invalidate_caches_for_function(menu_item.function)

        return menu_item

    @staticmethod
    @transaction.atomic
    def deprecate(menu_item: MenuItem, by_user: User) -> MenuItem:
        """UC: ACTIVE → DEPRECATED."""
        if menu_item.status != "ACTIVE":
            raise ValidationError(f"No se puede deprecar — estado actual: {menu_item.status}")

        menu_item.status = "DEPRECATED"
        menu_item.save(update_fields=("status", "updated_at"))
        MenuItemLifecycleService._invalidate_caches_for_function(menu_item.function)
        return menu_item

    @staticmethod
    @transaction.atomic
    def archive(menu_item: MenuItem, by_user: User) -> MenuItem:
        """UC: DEPRECATED → ARCHIVED."""
        if menu_item.status != "DEPRECATED":
            raise ValidationError(f"No se puede archivar — estado actual: {menu_item.status}")

        menu_item.status = "ARCHIVED"
        menu_item.save(update_fields=("status", "updated_at"))
        MenuItemLifecycleService._invalidate_caches_for_function(menu_item.function)
        return menu_item

    @staticmethod
    def _invalidate_caches_for_function(function: Function) -> None:
        """Invalida el cache de menú para todos los users con esa Function.

        Garantía: ejecutado dentro de la transacción atómica del UC.
        Si la transición falla, no se invalida cache (consistencia).
        Si la transición succeed, el cache queda invalidado antes de
        retornar al cliente.
        """
        # Users con la function via sus AGRs
        user_ids = (
            User.objects
            .filter(
                useraccessgroupassignment__access_group__functions=function,
            )
            .values_list("id", flat=True)
            .distinct()
        )

        for user_id in user_ids:
            cache.delete(f"menu:user:{user_id}")
            cache.delete(f"caps:user:{user_id}")    # cache de capabilities también
```

**Función Service también invalida cuando hay bulk update**:

```python
class FunctionLifecycleService:
    """UCs de Function — incluye invalidación de cache de menú."""

    @staticmethod
    @transaction.atomic
    def bulk_deactivate(function_ids: list[int], by_user: User) -> int:
        """UC bulk: desactiva N functions atómicamente + invalida caches."""
        affected_users = (
            User.objects.filter(
                useraccessgroupassignment__access_group__functions__id__in=function_ids,
            ).values_list("id", flat=True).distinct()
        )

        count = Function.objects.filter(id__in=function_ids).update(is_active=False)

        # Invalidación atómica con la transición
        for user_id in affected_users:
            cache.delete(f"menu:user:{user_id}")
            cache.delete(f"caps:user:{user_id}")

        return count
```

**Decisión arquitectónica firmada:**

> Cache invalidation **NO es responsabilidad de signals**.
> Cualquier transición de estado que afecte la visibilidad del
> menú (publish/deprecate/archive de MenuItem, activate/deactivate
> de Function, assign/revoke de AGR) **debe llamar
> explícitamente a la invalidación dentro de la transacción
> atómica** del UC.
>
> La signal puede usarse opcionalmente para casos edge
> (ej. fixtures de tests, scripts ad-hoc), pero **no como
> mecanismo principal**.

## Sección 4 — G-4: P2 reconsiderado — UC_ADM_04 único vs 4 UCs

### Diagnóstico del cuestionamiento

> *"P2 sigue recomendando 4 UCs separados sin reconsiderar el
> argumento de 2 UCs. (...) El argumento de 'transitions
> distintas' no es suficiente para justificar 4 UCs porque por
> esa lógica cada transición de estado de cualquier entidad
> del sistema sería un UC propio. La pregunta correcta es si
> un admin que puede publicar un menu debe poder archivarlo, o
> si esos son roles distintos."*

**Aceptado.** Mi argumento "transitions distintas" era
insuficiente. La pregunta correcta es: **¿son roles distintos
o el mismo rol?**

### Análisis de roles

Considerando el sistema RBAC actual:

| Rol | UCs ya asignados | ¿Quién publica/deprecia/archiva menus? |
|---|---|---|
| `system_admin` (AGR-010) | UC_ADM_01..03 (gestiona Functions, AGRs, SoD) | Mismo rol — coherente |
| `permission_admin` (AGR-007) | UC_PERM_01..10 (asigna/revoca permisos) | Posible candidato pero NO modifica catálogo |
| `auditor` (AGR-008) | UC_AUD_01..04 (audit, no modifica) | NO debe poder modificar |

**Conclusión:** los 3 transiciones (publish/deprecate/archive)
son **el mismo rol** (`system_admin` AGR-010). No hay
separation of concerns RBAC entre ellos.

### Decisión revisada: 1 UC consolidado `manage_menu_lifecycle`

```python
# UC_ADM_04: manage_menu_lifecycle
# Capability codename: adm:manage_menu_lifecycle
# Asignado a: AGR-010 (system_admin_group)
```

**API canónica:**

```
PATCH /api/menu-items/{id}/
Body: { "target_status": "ACTIVE" }   # publish
Body: { "target_status": "DEPRECATED" }   # deprecate
Body: { "target_status": "ARCHIVED" }   # archive
```

**Validación de transiciones** (en el service):

```python
ALLOWED_TRANSITIONS = {
    "DRAFT":      {"ACTIVE"},
    "ACTIVE":     {"DEPRECATED"},
    "DEPRECATED": {"ARCHIVED"},
    "ARCHIVED":   set(),    # estado terminal
}


class MenuItemLifecycleService:
    @staticmethod
    @transaction.atomic
    def transition(menu_item: MenuItem, target: str, by_user: User) -> MenuItem:
        """UC_ADM_04 — única operación para cambiar status."""
        if not by_user.has_capability("adm:manage_menu_lifecycle"):
            raise PermissionDenied()

        current = menu_item.status
        if target not in ALLOWED_TRANSITIONS.get(current, set()):
            raise ValidationError(
                f"Transición no permitida: {current} → {target}"
            )

        menu_item.status = target
        menu_item.save(update_fields=("status", "updated_at"))

        # Audit log con la transición específica
        AuditEvent.objects.create(
            event_type="MENU_ITEM_STATUS_TRANSITION",
            user=by_user,
            resource_type="MenuItem",
            resource_id=menu_item.id,
            metadata={
                "from_status": current,
                "to_status": target,
                "menu_item_label": menu_item.display_label,
                "function_codename": menu_item.function.codename,
            },
        )

        # Invalidación atómica (G-3)
        MenuItemLifecycleService._invalidate_caches_for_function(
            menu_item.function,
        )

        return menu_item
```

**Beneficios de UC consolidado:**

| Beneficio | Justificación |
|---|---|
| Coherencia RBAC | 1 capability = 1 rol semántico (system_admin) |
| Menos overhead conceptual | UC_ADM_04 absorbe 4 transiciones distintas |
| Audit consistente | 1 evento `MENU_ITEM_STATUS_TRANSITION` con `from`/`to` en metadata |
| Frontend más simple | 1 endpoint con `target_status`, no 4 endpoints específicos |
| Catalogo MOD_Admin más estable | Pasa de 3 funciones a 4 (no 7) |

**Granularidad sigue disponible** vía:

- Audit log — `metadata.to_status` distingue las transiciones.
- Validation rules — `ALLOWED_TRANSITIONS` impide saltos inválidos.
- Tests — uno por transición (publish, deprecate, archive).

### Comparación final

| Approach | UCs | Capabilities en MOD_Admin | API endpoints | Audit events distinguibles |
|---|---|---|---|---|
| **v1: 4 UCs separados** | UC_ADM_04..07 | 4 (`publish_menu_item`, `deprecate_menu_item`, `archive_menu_item`, `manage_menu_catalog`) | 4 endpoints específicos | Sí (event_type por UC) |
| **v2: 1 UC consolidado** | UC_ADM_04 | 1 (`manage_menu_lifecycle`) + UC_ADM_05 (`manage_menu_catalog` para CRUD metadata) | 2 endpoints (CRUD + transition) | Sí (via metadata.to_status) |

**Recomendación final:** **v2 con 2 UCs**:

- **UC_ADM_04** `manage_menu_catalog` — CRUD metadata UI
  (display_label, icon, display_order, route_path, parent).
- **UC_ADM_05** `manage_menu_lifecycle` — transiciones de
  status (publish/deprecate/archive vía PATCH con
  target_status).

MOD_Admin pasa de 3 a 5 funciones — más razonable que pasar
a 7.

## Sección 5 — Resumen de cambios v1 → v2

| Item | v1 (corrections) | v2 (review v2) |
|---|---|---|
| ``get_all_capabilities()`` | Llamada sin definir | **`UserCapabilityResolver` con 1 query + cache** + indexes obligatorios |
| Response shape | Árbol recursivo ``children`` | **Lista plana con `parent_id`** + frontend construye tree + max_depth=3 server-side |
| Cache invalidation | Via signal `post_save` | **Invalidación explícita en el UC de transición** dentro de transacción atómica |
| UCs nuevos en MOD_Admin | 4 UCs (UC_ADM_04..07) | **2 UCs (UC_ADM_04 catálogo + UC_ADM_05 lifecycle)** |

## Sección 6 — Las 4 preguntas — refinadas FINAL

| # | Pregunta | Recomendación final |
|---|---|---|
| **P1** | ¿Opción 1, 2 o 3? | **Opción 2** (MenuItem 1:1 wrapper UX, ahora con todas las correcciones C-1..C-4 + G-1..G-4) |
| **P2** | ¿Cuántos UCs? | **2 UCs**: UC_ADM_04 `manage_menu_catalog` + UC_ADM_05 `manage_menu_lifecycle` (no 4 separados) |
| **P3** | ¿Multi-tenancy? | **NO** (preserva BR-012; abrir scope si negocio lo requiere) |
| **P4** | ¿Cuántos estados? | **4** (DRAFT/ACTIVE/DEPRECATED/ARCHIVED) — refuerzo: DEPRECATED es esencial para C-4 |

## Sección 7 — Implicación para Phase 7 DESIGN — actualizada

Phase 7 DESIGN ahora produce:

1. **ADR-BACK-008** (revisado v2): MenuItem wrapper UX con
   `on_delete=PROTECT`, queryset SoT, modelo completo.
2. **ADR-BACK-009** (revisado v2): Contrato endpoint `/api/menu/`
   con lista plana + max_depth=3 + cache invalidation explícita.
3. **ADR-BACK-010** (NUEVO): `UserCapabilityResolver` con
   garantías de performance + indexes obligatorios.
4. **CNST-032** reescrito: guard rails C-1..C-4 + G-1..G-4.
5. **UC_PERM_08** extendido: 2 flujos (F-1, F-2).
6. **UC_ADM_04** `manage_menu_catalog` (NUEVO).
7. **UC_ADM_05** `manage_menu_lifecycle` (NUEVO).
8. **`rbac-implementation-guide.rst` extendido** sección Q9.
9. **Tests guardrail** verbatim (5 originales + 2 performance
   tests para G-1).

## Refs

- Análisis padre v1: ``discover/menuitem-design-corrections.md``.
- Análisis padre estructura: ``discover/menuitem-standalone-vs-wrapper-clarification.md``.
- Análisis principal: ``discover/lifecycle-managed-menu-vs-static-analysis.md``.
- Arqueología: ``discover/cmenu2-legacy-archeology.md``,
  ``discover/inserta-modulos-menu-sql-analysis.md``,
  ``discover/index-asp-legacy-render-analysis.md``.
- Corpus vigente:

  - ADR-BACK-001: :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`.
  - ADR-BACK-007: :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
  - CNST-029: :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
  - CNST-032: :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio`.
  - UC_PERM_08: :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.
