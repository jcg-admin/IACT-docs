```yml
created_at: 2026-05-06 23:30:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/lifecycle-managed-menu-vs-static-analysis.md
```

# Aclaración formal: MenuItem standalone vs wrapper UX sobre Function

## Trigger

Ejecutor preguntó: *"¿qué se refiere con MenuItem como entidad standalone?"*

El guard rail mencionado en el análisis previo
(``lifecycle-managed-menu-vs-static-analysis.md`` §5) es
crítico para evitar regresión al legacy ``C_MENU2``. Esta
aclaración lo formaliza con código y ejemplos.

## Sección 1 — Definición precisa de los dos diseños

### Diseño A — Standalone (❌ NO usar)

``MenuItem`` existe como entidad independiente en el modelo
de datos, sin relación obligatoria con ``Function``:

```python
class MenuItem(models.Model):
    label = models.CharField(...)
    icon = models.CharField(...)
    route_path = models.URLField(...)
    status = models.CharField(...)
    # NO hay FK a Function — el menu es independiente
```

Posible (e indeseado) crear:

```python
MenuItem.objects.create(
    label="Mis Reportes",
    route_path="/reports",
    status="ACTIVE",
)
# No hay Function que respalde la capability.
# El menu aparece pero el endpoint no tiene permission backend
# que lo proteja.
```

### Diseño B — Wrapper UX (✅ canónico v5.6.x)

``MenuItem`` REQUIERE una ``Function`` asociada como fuente
de la capability:

```python
class MenuItem(models.Model):
    function = models.OneToOneField(
        Function,
        on_delete=models.CASCADE,        # cascada: borra Function → borra MenuItem
        related_name="menu_item",
        # null=False, blank=False (default) — relación OBLIGATORIA
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
        User, on_delete=models.PROTECT,
        related_name="menu_items_created",
    )

    class Meta:
        db_table = "menu_items"
        ordering = ("display_order",)
        indexes = [models.Index(fields=("status",))]
```

Crear un ``MenuItem`` requiere que la ``Function`` exista
primero:

```python
# Paso 1 (obligatorio): crear la Function
function = Function.objects.create(
    codename="view_reports",
    module="RPT",
    name="Ver Reportes",
    is_active=True,
)

# Paso 2 (obligatorio): asignar a AGR via UC_PERM_06
agr_002 = AccessGroup.objects.get(agr_code="AGR-002")
FunctionGroupMembership.objects.create(
    group=agr_002, function=function,
)

# Paso 3 (opcional): crear MenuItem
MenuItem.objects.create(
    function=function,           # ← FK obligatoria
    display_label="Mis Reportes",
    icon="BarChartIcon",
    route_path="/reports",
    status="DRAFT",
    created_by=request.user,
)
```

## Sección 2 — Los 4 invariantes del Diseño B

| # | Invariante | Cómo se garantiza |
|---|---|---|
| I-1 | Todo MenuItem tiene exactamente una Function asociada | ``OneToOneField(null=False, blank=False)`` + DB unique constraint |
| I-2 | Borrar Function borra su MenuItem | ``on_delete=CASCADE`` |
| I-3 | Function puede existir sin MenuItem | OneToOne **opcional desde el lado Function** (``related_name="menu_item"`` es accesible vía ``function.menu_item`` con DoesNotExist si no existe) |
| I-4 | Desactivar Function (``is_active=False``) oculta MenuItem en runtime | Signal ``post_save`` o property en QuerySet manager |

### Implementación del invariante I-4 (signal)

```python
# apps/access/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Function, MenuItem


@receiver(post_save, sender=Function)
def sync_menu_item_visibility(sender, instance, **kwargs):
    """Si Function se desactiva, el MenuItem se considera oculto.

    No se cambia status — el MenuItem sigue existiendo y
    permanece editable. Solo el render lo filtra.
    """
    # No hay cambio de schema; el filter del queryset abajo
    # garantiza la coherencia.


# apps/access/managers.py
class MenuItemQuerySet(models.QuerySet):
    def visible(self):
        """MenuItems renderizables — Function activa + status ACTIVE."""
        return self.filter(
            status="ACTIVE",
            function__is_active=True,
        )

    def for_user(self, user):
        """MenuItems que el user puede ver según sus capabilities."""
        codenames = user.get_all_capabilities()  # via custom backend
        return self.visible().filter(
            function__codename__in=codenames,
        )
```

## Sección 3 — Tabla de visibilidad efectiva

Combinaciones de estados y resultado para el user:

| `Function.is_active` | `MenuItem.status` | User tiene capability | ¿Ve menú? | ¿Puede acceder a endpoint? |
|---|---|---|---|---|
| `True` | `ACTIVE` | ✅ | ✅ Sí | ✅ Sí |
| `True` | `ACTIVE` | ❌ | ❌ | ❌ |
| `True` | `DRAFT` | ✅ | ❌ (preview admin) | ✅ Sí (capability existe) |
| `True` | `DEPRECATED` | ✅ | ⚠️ Con etiqueta "(legacy)" | ✅ Sí |
| `True` | `ARCHIVED` | ✅ | ❌ | ✅ Sí (capability accesible por URL directa) |
| `True` | (sin MenuItem) | ✅ | ❌ (no hay item) | ✅ Sí (URL directa funciona) |
| `False` | (cualquiera) | (irrelevante) | ❌ | ❌ |

**Regla mnemotécnica:**

> *"La fuente de verdad de **'puede acceder'** es siempre
> ``Function`` (via AGR). ``MenuItem`` solo controla
> **'¿lo muestro en el sidebar?'**."*

## Sección 4 — Por qué Diseño A es regresión a `C_MENU2`

| Aspecto | Diseño A (standalone) | Legacy `C_MENU2` |
|---|---|---|
| Fuente de la capability | El menú | El menú (`BD_MENU2.ID_MENU1`) |
| Defense-in-depth | Roto | Roto |
| Crear menu sin permiso subyacente | Posible | Posible |
| Modelo flat sin jerarquía (CNST-029) | Violado | N/A (predates the constraint) |
| ADR-BACK-001 (sin jerarquía) | Violado | N/A |

Conclusión: **Diseño A reproduce 1:1 el anti-patrón del legacy
analizado en arqueología C_MENU2** (``cmenu2-legacy-archeology.md``).

## Sección 5 — Por qué Diseño B preserva v5.6.0 idiomatic

| Aspecto | Diseño B (wrapper UX) | Compatibilidad |
|---|---|---|
| Fuente de la capability | ``Function`` | CNST-029 ✅ |
| Modelo flat sin jerarquía | Sí (parent es UI override, no permission hierarchy) | ADR-BACK-001 ✅ |
| Defense-in-depth | Endpoint siempre protegido por Function | UC_PERM_08 §10 ✅ |
| RBAC custom vs auth.Group | Mantenido | ADR-BACK-007 ✅ |
| Lifecycle states | Granulares (DRAFT/ACTIVE/DEPRECATED/ARCHIVED) | Audit BR-010 ✅ |
| Naming | snake_case codename + display_label separado | STD-008 ✅ |

## Sección 6 — Referencia cruzada para Phase 7 DESIGN

Si el ejecutor aprueba **Opción 2** (la recomendación del
análisis padre), Phase 7 DESIGN debe documentar el modelo
``MenuItem`` siguiendo **Diseño B exclusivamente** y prohibir
explícitamente el Diseño A en:

- ADR-BACK-008 (nuevo): "MenuItem como wrapper UX sobre
  Function".
- CNST-032 reescrito: clausula explícita prohibiendo
  ``MenuItem`` standalone.
- ``rbac-implementation-guide.rst`` §"Q9 — MenuItem UI
  metadata layer" (extensión).

## Sección 7 — Test guardrail propuesto

```python
# apps/access/tests/test_menu_item.py
import pytest
from django.db import IntegrityError

from apps.access.models import MenuItem, Function


@pytest.mark.django_db
def test_cannot_create_menu_item_without_function():
    """Diseño B garantiza I-1: Function requerida."""
    with pytest.raises(IntegrityError):
        MenuItem.objects.create(
            display_label="Test",
            route_path="/test",
            status="ACTIVE",
            # SIN function= → debe fallar
        )


@pytest.mark.django_db
def test_deleting_function_cascades_to_menu_item():
    """Diseño B garantiza I-2: cascade on_delete."""
    fn = Function.objects.create(codename="test_fn", module="TST")
    mi = MenuItem.objects.create(
        function=fn, display_label="X", route_path="/x",
    )
    fn.delete()
    assert not MenuItem.objects.filter(pk=mi.pk).exists()


@pytest.mark.django_db
def test_function_can_exist_without_menu_item():
    """Diseño B garantiza I-3: capability sin item visual."""
    fn = Function.objects.create(codename="manage_own_state", module="OPR")
    # Sin MenuItem asociado
    assert not hasattr(fn, "menu_item") or fn.menu_item is None


@pytest.mark.django_db
def test_inactive_function_hides_menu_item():
    """Diseño B garantiza I-4: visibility cascade."""
    fn = Function.objects.create(codename="x", module="TST", is_active=True)
    MenuItem.objects.create(function=fn, display_label="X", route_path="/x", status="ACTIVE")

    assert MenuItem.objects.visible().filter(function=fn).exists()

    fn.is_active = False
    fn.save()

    assert not MenuItem.objects.visible().filter(function=fn).exists()
```

## Sección 8 — Resumen ejecutivo en una frase

> **"Standalone"** = ``MenuItem`` puede existir sin
> ``Function`` → el menú **es** la regla de acceso (legacy
> ``C_MENU2``).
>
> **"Wrapper UX"** = ``MenuItem`` requiere ``Function`` → el
> menú **solo presenta** la regla, que vive en ``Function``
> (v5.6.x idiomatic).

## Refs

- Análisis padre: ``discover/lifecycle-managed-menu-vs-static-analysis.md``.
- Arqueología legacy: ``discover/cmenu2-legacy-archeology.md``.
- Análisis SQL: ``discover/inserta-modulos-menu-sql-analysis.md``.
- Render legacy ASP: ``discover/index-asp-legacy-render-analysis.md``.
- ID_CONVENIO equivalente: ``discover/menu-v560-design-and-id-convenio-equivalent.md``.
- Análisis principal: ``discover/menu-rbac-user-scope-docs-analysis.md``.
- ADR-BACK-001 (modelo flat): :doc:`/backend/adr-back-001-grupos-funcionales-sin-jerarquia`.
- ADR-BACK-007 (custom RBAC): :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
- CNST-029 (RBAC modelo plano): :doc:`/normativa/restricciones/cnst-029-rbac-modelo-plano`.
- UC_PERM_08 (Generar Menu Dinámico): :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.
- Catálogo de Function: :doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones`.
