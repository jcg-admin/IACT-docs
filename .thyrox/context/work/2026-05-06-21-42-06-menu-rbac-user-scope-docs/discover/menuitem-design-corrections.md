```yml
created_at: 2026-05-06 23:50:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/menuitem-standalone-vs-wrapper-clarification.md
```

# Correcciones al diseño de `MenuItem` — review crítico

## Trigger

Tras la propuesta de wrapper UX `MenuItem`, el ejecutor
identificó **4 cuestionamientos válidos** + **1 gap** que
revelan decisiones implícitas no defendibles. Este documento
revierte/refina esas decisiones y hace explícito el contrato
del endpoint que faltaba.

## Sección 1 — Las 4 correcciones aceptadas

### Corrección C-1: ``on_delete=CASCADE`` → ``on_delete=PROTECT``

**Cuestionamiento del ejecutor:**

> *"CASCADE en este contexto tiene una consecuencia grave: si
> alguien borra una Function por error o por proceso de
> deprecación, el MenuItem desaparece silenciosamente sin audit
> trail propio. (...) El CASCADE asume que borrar Function es
> una operación válida y frecuente. Dado que el modelo tiene
> estados y soft-delete, probablemente no debería serlo."*

**Aceptado.** Mi propuesta original era inconsistente con la
decisión de 4 estados de lifecycle.

**Análisis de consistencia:**

Si el lifecycle correcto es:

```
DRAFT → ACTIVE → DEPRECATED → ARCHIVED
```

Entonces `DELETE` directo de `Function` **no es operación
válida** en flujo normal. El admin debe:

1. Marcar el `MenuItem.status = ARCHIVED` (UC_ADM_07).
2. Marcar la `Function.is_active = False` (UC_ADM_02).
3. **Eventualmente** borrar — pero esto es operación
   excepcional, no rutinaria.

`CASCADE` permite saltar todo este flujo silenciosamente.
`PROTECT` lo bloquea.

**Decisión correcta: `on_delete=PROTECT`.**

```python
class MenuItem(models.Model):
    function = models.OneToOneField(
        Function,
        on_delete=models.PROTECT,        # ← cambio
        related_name="menu_item",
    )
    # ...
```

**Implicación operativa:**

- Borrar una `Function` con `MenuItem` asociado lanza
  ``ProtectedError``.
- El admin debe archivar el `MenuItem` primero.
- Audit trail intacto: el `MenuItem.status = ARCHIVED`
  preserva el evento.

### Corrección C-2: Signal NO es source of truth de visibilidad

**Cuestionamiento del ejecutor:**

> *"La signal post_save para ocultar MenuItem cuando
> Function.is_active = False es frágil. (...) Si alguien hace
> Function.objects.filter(module='RPT').update(is_active=False),
> ninguna signal se dispara y los MenuItems quedan en estado
> inconsistente visualmente. La solución correcta es que el
> endpoint que sirve el menu siempre filtre por
> function__is_active=True en el queryset, sin depender de
> signals."*

**Aceptado.** Mi diseño original confundió "trigger" con
"source of truth".

**Análisis del problema:**

Django `post_save` signal **NO se dispara en bulk operations**:

```python
# NO triggers signal:
Function.objects.filter(module="RPT").update(is_active=False)

# SÍ triggers signal:
fn = Function.objects.get(pk=X)
fn.is_active = False
fn.save()
```

Si la visibilidad del `MenuItem` depende de un campo
sincronizado por signal, un bulk update deja el estado
inconsistente: `Function.is_active=False` pero algún flag
duplicado en `MenuItem` queda `True`.

**Decisión correcta: el queryset filter es la única fuente
de verdad de visibilidad.**

```python
# apps/access/managers.py
class MenuItemQuerySet(models.QuerySet):
    def renderable(self):
        """Items que el endpoint debe devolver al frontend.

        Source of truth de visibilidad — sin depender de signals.
        Funciona correctamente con bulk updates.
        """
        return self.filter(
            status__in=["ACTIVE", "DEPRECATED"],   # ← C-3 abajo
            function__is_active=True,
        )

    def for_user(self, user):
        """Items visibles para un user específico."""
        codenames = user.get_all_capabilities()
        return self.renderable().filter(
            function__codename__in=codenames,
        ).select_related("function").order_by("display_order")
```

**Implicación:** la signal `post_save` puede usarse para
**invalidación de cache** opcional, pero **no para
sincronizar estado**. El queryset siempre re-evalúa
`function__is_active`.

### Corrección C-3: Flujo "Function sin MenuItem" es válido y debe documentarse

**Cuestionamiento del ejecutor:**

> *"El flujo de 3 pasos asume que siempre se crea MenuItem
> después de Function. (...) No contempla el caso inverso
> válido: una Function que existe y tiene usuarios asignados
> pero intencionalmente no tiene MenuItem porque la capability
> es accesible solo por URL directa (API, integración, acceso
> técnico)."*

**Aceptado.** El invariante I-3 lo permitía técnicamente, pero
el flujo operativo no lo documentaba como caso primer-class.

**Casos de uso valídos para `Function` SIN `MenuItem`:**

| Función | Por qué no necesita MenuItem |
|---|---|
| `read_own_mailbox` | Acción interna del header (no item de sidebar) |
| `manage_own_agent_state` | Botón rápido en toolbar (no menú) |
| `acknowledge_alert` | Acción contextual sobre una alerta (en su detalle) |
| `export_csv` | Acción dentro del reporte (no entry de sidebar) |
| `view_user_menu_simulation` | Capacidad técnica de admin/auditor (URL directa) |
| `view_audit_log` (para integraciones) | Endpoint API consumido por sistema externo |

**Documentación operativa correcta — 2 flujos válidos:**

#### Flujo F-1: Function CON MenuItem (capability con entry visual en sidebar)

```
1. UC_ADM_02 manage_function_catalog → crear Function
2. UC_PERM_06 assign_functions_to_group → asignar a AGR
3. UC_ADM_04 manage_menu_catalog → crear MenuItem (opcional)
4. UC_ADM_05 publish_menu_item → status=ACTIVE
```

#### Flujo F-2: Function SIN MenuItem (capability sin entry visual)

```
1. UC_ADM_02 manage_function_catalog → crear Function
2. UC_PERM_06 assign_functions_to_group → asignar a AGR
3. (FIN — la capability se accede por URL directa o acción contextual)
```

**Implicación de UX:** los admins **no deben sentir que "falta
algo"** cuando una `Function` no tiene `MenuItem`. La UI de
admin debe mostrar explícitamente:

- Functions con MenuItem (lista 1).
- Functions sin MenuItem (lista 2 — "Capabilities sin entry
  de menú", con botón opcional "Crear MenuItem").

### Corrección C-4: DEPRECATED debe estar en el contrato del endpoint

**Cuestionamiento del ejecutor:**

> *"El estado DEPRECATED con etiqueta visual es una decisión de
> UX no resuelta. La tabla dice que DEPRECATED muestra el item
> 'con etiqueta (legacy)'. Eso implica que el frontend tiene
> que saber interpretar ese estado y renderizar algo diferente.
> (...) El endpoint de menu no puede devolver solo los items
> ACTIVE, sino que tiene que devolver también los DEPRECATED
> con un campo que el frontend use para diferenciar la
> presentación."*

**Aceptado.** La sutileza de DEPRECATED requiere contrato
explícito del endpoint.

**Implicación contractual:**

El endpoint NO puede:

- Filtrar `status="ACTIVE"` (deja fuera DEPRECATED → frontend
  no los ve).

El endpoint SÍ debe:

- Filtrar `status IN ("ACTIVE", "DEPRECATED")` —
  **DRAFT y ARCHIVED quedan fuera**.
- Devolver `status` como campo del payload — frontend lo lee
  y decide la presentación.

**Tabla de comportamiento del frontend según `status`:**

| status del payload | Comportamiento UI |
|---|---|
| `ACTIVE` | Render normal |
| `DEPRECATED` | Render con etiqueta "(legacy)" + tooltip "Esta opción será removida en futuras versiones" |
| (no recibido — `DRAFT`/`ARCHIVED`) | No aparece en sidebar |

## Sección 2 — Gap detectado: contrato del endpoint `/api/menu/`

**Observación del ejecutor:**

> *"El documento habla de visibilidad pero no define qué
> devuelve el endpoint /api/menu/ ni su estructura. Si ese
> contrato no se define antes de implementar, el frontend y
> el backend van a hacer suposiciones distintas."*

**Aceptado.** El contrato debe ser explícito antes de Phase 7
DESIGN. Documento el contrato canónico aquí.

### Endpoint canónico

```
GET /api/menu/
Authorization: Bearer <jwt>
```

### Filtros aplicados (todos AND)

1. ``MenuItem.status IN ("ACTIVE", "DEPRECATED")``.
2. ``MenuItem.function__is_active = True``.
3. ``MenuItem.function__codename IN <user.capabilities>``.

### Order

1. Por ``display_order ASC`` dentro de cada nivel de
   jerarquía.
2. Resolución de árbol via ``parent`` (recursive serializer
   o vista anidada).

### Response shape (200 OK)

```json
{
  "user_id": 42,
  "generated_at": "2026-05-06T23:55:00Z",
  "items": [
    {
      "id": "menuitem-uuid-1",
      "codename": "view_reports",
      "display_label": "Mis Reportes",
      "icon": "BarChartIcon",
      "route_path": "/reports",
      "display_order": 10,
      "status": "ACTIVE",
      "parent_id": null,
      "children": [
        {
          "id": "menuitem-uuid-2",
          "codename": "export_csv",
          "display_label": "Exportar CSV",
          "icon": "DownloadIcon",
          "route_path": "/reports/export-csv",
          "display_order": 1,
          "status": "ACTIVE",
          "parent_id": "menuitem-uuid-1",
          "children": []
        }
      ]
    },
    {
      "id": "menuitem-uuid-3",
      "codename": "view_legacy_dashboard",
      "display_label": "Dashboard antiguo",
      "icon": "DashboardIcon",
      "route_path": "/dashboard-legacy",
      "display_order": 99,
      "status": "DEPRECATED",
      "parent_id": null,
      "children": []
    }
  ]
}
```

### Campos del item — definición precisa

| Campo | Tipo | Obligatorio | Significado |
|---|---|---|---|
| `id` | UUID | Sí | PK del MenuItem (no expone autoincrement) |
| `codename` | string | Sí | Codename de la Function asociada (el frontend cruza con sus rutas) |
| `display_label` | string | Sí | Texto humano del item (i18n responsibility del frontend si aplica) |
| `icon` | string | No (default `""`) | Identificador del icono — frontend lo mapea a su componente |
| `route_path` | string | Sí | Ruta SPA (NO URLs ASP-like — guard rail anti-legacy) |
| `display_order` | int | Sí | Orden visual entre hermanos del mismo `parent` |
| `status` | string | Sí | `"ACTIVE"` o `"DEPRECATED"` (DRAFT/ARCHIVED nunca aparecen aquí) |
| `parent_id` | UUID o null | Sí | Padre en el árbol; `null` si es nivel raíz |
| `children` | array | Sí (puede ser `[]`) | Subárbol pre-resuelto por el backend |

### Cache strategy

- TTL: 5 minutos.
- Cache key: ``menu:user:{user_id}``.
- Invalidación: signal `post_save` en `UserAccessGroupAssignment`,
  `Function`, `MenuItem` → DEL del cache key.
- **NOTA:** la invalidación de cache via signal **es OK aquí**
  porque cache es derivado, no source of truth. Si la signal
  no se dispara (bulk update), el peor caso es: TTL de 5 min
  hasta refrescar. No hay inconsistencia permanente.

### Errores

| Status | Body code | Razón |
|---|---|---|
| 401 | `UNAUTHORIZED` | Sin JWT válido |
| 403 | `FORBIDDEN` | JWT válido pero user inactivo |
| 503 | `MENU_SERVICE_UNAVAILABLE` | DB timeout o cache failure |

### Performance targets

- Cache HIT: P50 ≤ 5 ms, P95 ≤ 30 ms.
- Cache MISS: P50 ≤ 50 ms, P95 ≤ 200 ms.
- Coverage de tests: 100% de las 4 ramas (4 estados de status).

## Sección 3 — Diseño corregido del modelo `MenuItem`

```python
class MenuItem(models.Model):
    """Wrapper UX sobre Function — provee metadata visual.

    Invariantes (I-1..I-4):
    - Toda fila tiene una Function asociada.
    - PROTECT impide borrar Function con MenuItem (admin debe archivar).
    - Function puede existir sin MenuItem (capability sin item visual).
    - Visibilidad efectiva derivada de queryset, no de signals.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    function = models.OneToOneField(
        Function,
        on_delete=models.PROTECT,    # ← C-1: ya no CASCADE
        related_name="menu_item",
    )
    display_label = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, default="")
    display_order = models.IntegerField(default=0)
    route_path = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("DRAFT",      "Borrador"),
            ("ACTIVE",     "Activo"),
            ("DEPRECATED", "Deprecado"),
            ("ARCHIVED",   "Archivado"),
        ],
        default="DRAFT",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="menu_items_created",
    )

    objects = MenuItemQuerySet.as_manager()    # ← C-2

    class Meta:
        db_table = "menu_items"
        ordering = ("display_order",)
        indexes = [
            models.Index(fields=("status",)),
            models.Index(fields=("parent", "display_order")),
        ]
```

## Sección 4 — Tests guardrail revisados

```python
# apps/access/tests/test_menu_item.py
from django.db.models import ProtectedError


@pytest.mark.django_db
def test_protect_blocks_function_delete_when_menu_item_exists():
    """C-1: PROTECT impide borrar Function con MenuItem.

    Admin DEBE archivar MenuItem primero.
    """
    fn = Function.objects.create(codename="test", module="TST")
    MenuItem.objects.create(
        function=fn, display_label="X", route_path="/x",
        created_by=admin_user,
    )

    with pytest.raises(ProtectedError):
        fn.delete()    # bloqueado correctamente


@pytest.mark.django_db
def test_archived_menu_item_allows_function_delete():
    """Tras archivar el MenuItem, borrar Function sigue requiriendo
    eliminación explícita del MenuItem (no auto-cascade)."""
    fn = Function.objects.create(codename="test", module="TST")
    mi = MenuItem.objects.create(
        function=fn, display_label="X", route_path="/x",
        status="ARCHIVED",
        created_by=admin_user,
    )

    with pytest.raises(ProtectedError):
        fn.delete()    # PROTECT sigue activo aún con ARCHIVED

    # Flujo correcto: borrar MenuItem primero, luego Function
    mi.delete()
    fn.delete()    # ahora sí
    assert not Function.objects.filter(pk=fn.pk).exists()


@pytest.mark.django_db
def test_bulk_function_deactivation_hides_menu_items_via_queryset():
    """C-2: visibilidad funciona con bulk updates (sin signals)."""
    fns = [
        Function.objects.create(codename=f"fn_{i}", module="TST", is_active=True)
        for i in range(3)
    ]
    for fn in fns:
        MenuItem.objects.create(
            function=fn, display_label=fn.codename, route_path=f"/{fn.codename}",
            status="ACTIVE",
            created_by=admin_user,
        )

    assert MenuItem.objects.renderable().count() == 3

    # Bulk update — no dispara signals
    Function.objects.filter(module="TST").update(is_active=False)

    # El queryset filter sigue siendo source of truth
    assert MenuItem.objects.renderable().count() == 0


@pytest.mark.django_db
def test_function_without_menu_item_is_valid_first_class():
    """C-3: Function sin MenuItem es flujo válido."""
    fn = Function.objects.create(codename="api_only_capability", module="API")
    # Asignar a AGR
    agr = AccessGroup.objects.get(agr_code="AGR-002")
    FunctionGroupMembership.objects.create(group=agr, function=fn)

    # Sin MenuItem — esto es válido
    with pytest.raises(MenuItem.DoesNotExist):
        fn.menu_item

    # User con la capability puede usar el endpoint pero NO ve item en menu
    user = make_user_with_agr("AGR-002")
    assert user.has_perm("api_only_capability")
    assert MenuItem.objects.for_user(user).count() == 0


@pytest.mark.django_db
def test_endpoint_returns_active_and_deprecated_not_draft_or_archived():
    """C-4: contrato del endpoint incluye DEPRECATED, excluye DRAFT/ARCHIVED."""
    fn1 = Function.objects.create(codename="x1", module="TST")
    fn2 = Function.objects.create(codename="x2", module="TST")
    fn3 = Function.objects.create(codename="x3", module="TST")
    fn4 = Function.objects.create(codename="x4", module="TST")

    MenuItem.objects.create(function=fn1, display_label="A", route_path="/x1",
                            status="DRAFT", created_by=admin_user)
    MenuItem.objects.create(function=fn2, display_label="B", route_path="/x2",
                            status="ACTIVE", created_by=admin_user)
    MenuItem.objects.create(function=fn3, display_label="C", route_path="/x3",
                            status="DEPRECATED", created_by=admin_user)
    MenuItem.objects.create(function=fn4, display_label="D", route_path="/x4",
                            status="ARCHIVED", created_by=admin_user)

    visible = list(MenuItem.objects.renderable().values_list("status", flat=True))
    assert "ACTIVE" in visible
    assert "DEPRECATED" in visible
    assert "DRAFT" not in visible
    assert "ARCHIVED" not in visible
```

## Sección 5 — Resumen de cambios al diseño

| Decisión original | Decisión corregida | Razón |
|---|---|---|
| ``on_delete=CASCADE`` | ``on_delete=PROTECT`` | C-1: consistencia con lifecycle de 4 estados; admin debe archivar antes |
| Signal `post_save` como mecanismo de visibilidad | Queryset filter como source of truth | C-2: bulk updates no disparan signals |
| Flujo único "Function → MenuItem" | Dos flujos válidos: F-1 con MenuItem, F-2 sin MenuItem | C-3: capabilities API/integración no necesitan item visual |
| Endpoint filtra solo ACTIVE | Endpoint devuelve ACTIVE + DEPRECATED con campo `status` | C-4: frontend diferencia visualmente |
| (Sin contrato definido) | Contrato canónico documentado: filtros, response shape, cache, errores, performance | Gap: previene divergencia frontend/backend |

## Sección 6 — Implicación para Phase 7 DESIGN

Phase 7 DESIGN debe producir:

1. **ADR-BACK-008** (revisado): MenuItem como wrapper UX,
   ``on_delete=PROTECT``, queryset como source of truth.
2. **ADR-BACK-009** (nuevo): contrato del endpoint
   ``/api/menu/`` con response shape canónico, cache strategy,
   y guardrails frontend (campo `status` obligatorio).
3. **CNST-032 reescrito**: clausulas explícitas sobre los 4
   guard rails C-1..C-4 + contrato del endpoint.
4. **UC_PERM_08 extendido**: documentar los 2 flujos (F-1 con
   MenuItem, F-2 sin MenuItem) como casos válidos primer-class.
5. **rbac-implementation-guide.rst extendido** con sección
   "Q9 — MenuItem y endpoint /api/menu/".
6. **Tests guardrail** verbatim incluidos en la guía.

## Refs

- Análisis padre: ``discover/menuitem-standalone-vs-wrapper-clarification.md``.
- Análisis principal: ``discover/lifecycle-managed-menu-vs-static-analysis.md``.
- ADR-BACK-001 (modelo flat): :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`.
- ADR-BACK-007 (custom RBAC): :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
- CNST-029 (RBAC modelo plano): :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
- UC_PERM_08: :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.
