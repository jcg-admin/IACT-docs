```yml
created_at: 2026-05-06 23:00:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/menu-v560-design-and-id-convenio-equivalent.md
```

# Lifecycle managed menu vs static ALL_NAV_LINKS — replanteo arquitectónico

## Trigger

Ejecutor desafió la propuesta anterior de ``ALL_NAV_LINKS``
constante:

> *"¿no consideras que está mejor que se tengan una función con
> los estados correspondientes a la asignación, desasignacion,
> creación, altas, bajas de menus?"*

El planteamiento es válido. Mi propuesta anterior priorizó
"alejarse del legacy `C_MENU2`" pero descartó beneficios
legítimos del modelo lifecycle-managed. Replanteo aquí.

## Sección 1 — Reconocimiento de los problemas reales del approach static

### 1.1 ¿Qué problemas tiene `ALL_NAV_LINKS` estática?

| Problema | Severidad | Detalle |
|---|---|---|
| **Sin audit del lifecycle del menu** | ALTA | ¿Quién decidió agregar "Reportes" al menú? ¿Cuándo? Git blame del archivo no es audit formal. |
| **Sin soft-delete** | ALTA | Si elimino una entry, refs históricas se pierden. No hay "DEPRECADO" como estado intermedio. |
| **Sin estados explícitos** | MEDIA | Solo "está" o "no está". No hay BORRADOR, INACTIVO, DEPRECADO. |
| **Sin granularidad de rollout** | MEDIA | Para activar un menú nuevo solo a algunos AGRs durante feature flag → requiere lógica adicional en código. |
| **Acopla menu a release frontend** | MEDIA | Cambios al menú = release del SPA. Para org grandes con CI/CD lento puede ser fricción. |
| **Sin trazabilidad de cambios al catálogo** | MEDIA | Imposible reconstruir "estado del menú al 15 de marzo de 2026" sin git archeology. |

### 1.2 ¿Qué propone el ejecutor?

Una **función con estados** que cubra:

- **Creación** de menus (alta de un nuevo item).
- **Altas / Bajas** (activar / desactivar).
- **Asignación / Desasignación** (rollout granular por AGR).
- **Estados** (ACTIVO / INACTIVO / DEPRECADO / BORRADOR).

Esto es **management runtime** del catálogo del menú, no
hardcoded en código.

## Sección 2 — Verificación: ¿v5.6.0 YA tiene esto?

**Sí, en gran parte.** El catálogo de Functions v5.6.0 ya
implementa lifecycle managed:

### 2.1 Lifecycle states existentes a nivel `Function`

```python
class Function(models.Model):
    codename = models.CharField(...)
    name = models.CharField(...)
    module = models.CharField(...)
    description = models.TextField(...)
    is_active = models.BooleanField(default=True)  # ← estado
    # implícito: created_at, updated_at via auto-fields
```

| Operación | UC | Implementación |
|---|---|---|
| **Creación** de Function | UC_ADM_02 ``manage_function_catalog`` | CRUD sobre catálogo |
| **Alta/Baja** (activar/desactivar) | UC_ADM_02 (toggle ``is_active``) | Update field, idempotente |
| **Asignación** a AGR | UC_PERM_06 ``assign_functions_to_group`` | M2M ``FunctionGroupMembership.objects.create`` |
| **Desasignación** | UC_PERM_02 ``revoke_function_group`` | Delete del row M2M |
| **Estados implícitos** | ``is_active`` boolean | Function existe + activa = visible; existe + inactiva = oculta; no existe = nunca creada |
| **Audit del lifecycle** | MOD_Audit (P-44) + ``BR_010 auditoria_inmutable`` | Cada CRUD de Function genera evento de alta criticidad (CNST-029) |

### 2.2 ¿Qué falta? — Solo metadata UI

Lo que v5.6.0 NO tiene a nivel Function:

| Campo UI faltante | Para qué sirve |
|---|---|
| `display_label` | Texto humano del item (vs codename técnico) — ej. "Mis Reportes" vs `view_reports` |
| `icon` | Identificador del icono UI |
| `display_order` | Orden visual entre hermanos |
| `parent_menu_item` | Padre en la jerarquía visual (separado del `module` lógico) |
| `is_visible_in_menu` | Una Function puede ser capability sin ser entry de menú (ej. `read_own_mailbox` no necesita item dedicado) |
| `route_path` | Ruta SPA del item (`/reports`, `/users`, etc.) |

**Conclusión:** la lifecycle YA EXISTE. El gap es **metadata
UI** específica del item de menú.

## Sección 3 — Tres opciones de diseño

### Opción 1 — Enriquecer ``Function`` con campos UI

Agregar columnas UI directamente al modelo ``Function``:

```python
class Function(models.Model):
    # campos canonicos v5.6.0:
    codename = models.CharField(unique=True)
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # NUEVOS — UI metadata:
    display_label = models.CharField(max_length=100, blank=True)  # vs codename
    icon = models.CharField(max_length=100, blank=True)
    display_order = models.IntegerField(default=0)
    is_visible_in_menu = models.BooleanField(default=True)
    route_path = models.URLField(max_length=200, blank=True)
    parent_function = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
```

**Ventajas:**

- Un solo modelo, un solo CRUD.
- El admin gestiona el catálogo entero desde una UI.
- Cualquier cambio (agregar capability + entry menu) = un solo INSERT.
- Audit unificado.

**Desventajas:**

- Mezcla concerns: una `Function` es un permiso atómico (lógica) Y un nodo de menú (UI). No es ortogonal.
- El concepto "Function" se contamina con UI metadata que no debería preocupar al permission backend.
- Capabilities que NO son menu items (ej. `manage_own_agent_state` que es una acción dentro de una página, no un item) deben llevar `is_visible_in_menu=False` — flag que no aplica naturalmente al concepto.

### Opción 2 — Entidad `MenuItem` 1:1 con `Function`

Modelo separado que envuelve Function con metadata UI:

```python
class MenuItem(models.Model):
    """Entry visual del menu — wrapper UI sobre Function.

    Una Function puede tener 0 o 1 MenuItem (relación opcional).
    Un MenuItem siempre apunta a una Function (que define su
    capability requirement).
    """

    function = models.OneToOneField(
        Function,
        on_delete=models.CASCADE,
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
    is_visible = models.BooleanField(default=True)
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
        indexes = [models.Index(fields=("status", "is_visible"))]
```

**Ventajas:**

- **Separation of concerns**: `Function` = permission lógico,
  `MenuItem` = UI wrapper.
- **Functions sin MenuItem son legítimas**: capabilities que no
  necesitan entry visual no tienen MenuItem.
- **Lifecycle independiente**: `Function.is_active` (capability)
  vs `MenuItem.status` (visibilidad UI). Pueden moverse en
  rangos distintos.
- **Audit independiente** sobre cada plano.
- **Soft-delete real**: `MenuItem.status = ARCHIVED` preserva
  la entry para refs históricas.

**Desventajas:**

- Dos modelos a sincronizar (FK 1:1 garantiza integridad pero
  agrega complejidad operativa).
- CRUD doble: crear capability + crear menu item (con UC_ADM_02
  + UC_ADM_04 nuevo, por ejemplo).
- Aún acopla algo de UI al backend (display_label, icon,
  route_path) — el frontend debe respetar estos valores.

### Opción 3 — Híbrida: lifecycle managed pero metadata UI en frontend

```python
class Function(models.Model):
    # campos canonicos v5.6.0 + lifecycle ya existente

    # Solo agregamos:
    is_visible_in_menu = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    # NO agregamos label/icon/route_path — eso vive en frontend
```

Frontend tiene constante mínima:

```typescript
// MENU_METADATA: solo lo que NO se gestiona en backend
const MENU_METADATA: Record<string, MenuMetadata> = {
  'view_reports': {
    label: 'Mis Reportes',
    icon: 'BarChartIcon',
    route: '/reports',
  },
  'view_users': {
    label: 'Usuarios',
    icon: 'UsersIcon',
    route: '/users',
  },
  // ...una entry por Function que tenga is_visible_in_menu=true
};
```

**Y el render**:

```typescript
const visibleMenuItems = userCapabilities
  .filter(codename => MENU_METADATA[codename])
  .filter(codename => functionsFromBackend
    .find(f => f.codename === codename)?.is_visible_in_menu)
  .map(codename => ({
    ...MENU_METADATA[codename],
    codename,
    order: functionsFromBackend
      .find(f => f.codename === codename)?.display_order ?? 0,
  }))
  .sort((a, b) => a.order - b.order);
```

**Ventajas:**

- Backend gestiona **lifecycle + visibilidad + orden** (datos que cambian).
- Frontend gestiona **label/icon/route** (datos que no cambian sin redespliegue de UI).
- Audit completo del lifecycle (lo que el ejecutor pidió) sin contaminar `Function`.
- Multi-tenancy: un MenuMetadata diferente per client/theme se controla en frontend (release).
- Compatible con la decisión Lectura B (jerarquía derivable
  del codename).

**Desventajas:**

- Para agregar un menu nuevo: requiere release frontend
  (agregar entry a `MENU_METADATA`) + activar Function en
  backend.
- Si label/icon necesitan ser i18n dinámicos, el frontend
  necesita un sistema separado.

## Sección 4 — Comparación de opciones

| Criterio | Opción 1 (Function enriquecida) | Opción 2 (MenuItem 1:1) | Opción 3 (Híbrida) |
|---|---|---|---|
| Lifecycle managed | ✅ | ✅ | ✅ |
| Audit del menu | ✅ | ✅ (independiente) | ✅ |
| Estados explícitos (DRAFT/ACTIVE/DEPRECATED) | parcial (solo `is_active`) | ✅ (4+ estados) | parcial |
| Separation of concerns | ❌ (mezcla) | ✅ | ✅ (parcial) |
| Functions sin menu item | con flag (feo) | naturalmente | con flag |
| Cambio de label/icon | requiere INSERT + redeploy frontend | requiere PATCH MenuItem (no redeploy) | requiere redeploy frontend |
| Cambio de orden | UPDATE Function | PATCH MenuItem | UPDATE Function |
| Activar/desactivar item | UPDATE Function.is_active | PATCH MenuItem.status | UPDATE Function.is_visible_in_menu |
| Multi-tenant (menus diferentes per client) | Difícil | ✅ (un MenuItem per tenant via segment_id) | ❌ (frontend constante global) |
| Complejidad del modelo | Bajo | Alto (2 modelos) | Bajo |
| Riesgo de regresión a `C_MENU2` legacy | Bajo (Function es semántica, no ASP-like) | Medio (MenuItem se parece a `C_MENU2` si se le agrega `HREF`) | Bajo |
| Esfuerzo migración | Bajo (agregar campos a Function existente) | Alto (modelo nuevo + UCs nuevos) | Bajo (agregar 2 campos) |

## Sección 5 — Recomendación

**Recomendación: Opción 2 (MenuItem 1:1 con Function), con
guard explícito contra el anti-patrón legacy.**

Razonamiento:

1. **El ejecutor tiene razón** en que el lifecycle managed
   tiene ventajas reales (audit, estados, granularidad,
   separation of concerns).
2. **Opción 1 mezcla concerns** — agregar UI fields a Function
   es contaminación.
3. **Opción 3 retiene fragilidad del approach static** para
   label/icon/route.
4. **Opción 2 es separation of concerns limpia + lifecycle
   completo + estados explícitos**, sin riesgo si se respeta
   el guard rail.

### Guard rails contra regresión a `C_MENU2` legacy

Si se elige Opción 2, el ADR debe incluir explícitamente:

- ❌ `MenuItem.route_path` NO almacena URLs ASP-like (`'index.asp'`, `'menu.asp'`). Solo paths SPA modernos (`/reports`, `/users/{id}`).
- ❌ `MenuItem` NO tiene flags `can_read/can_write/can_delete`. Eso lo hace `Function` via codename.
- ❌ `MenuItem.parent` referencia otro `MenuItem` (semántica UI), NO un node arbitrario. La jerarquía sigue siendo derivable del codename para el caso default; `parent` es override solo cuando el agrupamiento UI difiere del agrupamiento por module.
- ❌ NO BD multi-tenant via `id_convenio` o `segment_id` en MenuItem (decisión BR-012 + scope).
- ✅ `MenuItem` SOLO existe como wrapper de UX sobre `Function`. Si una Function se desactiva (`is_active=False`), su MenuItem también se oculta automáticamente vía signal.
- ✅ Audit de cambios via Django admin log + MOD_Audit events (P-44 audit reforzado).

### Lifecycle completo con Opción 2

```
┌─────────────────────────────────────────────────────────────┐
│  CICLO DE VIDA — Function                                   │
│                                                             │
│  CREATE Function (UC_ADM_02 manage_function_catalog)        │
│    └─ is_active=True                                        │
│         │                                                   │
│         ├─ ASSIGN to AGR (UC_PERM_06)                       │
│         ├─ REVOKE from AGR (UC_PERM_02)                     │
│         │                                                   │
│         └─ DEACTIVATE (UC_ADM_02)                           │
│              └─ is_active=False                             │
│                   └─ DELETE (raro; preferir is_active=False)│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CICLO DE VIDA — MenuItem (NUEVO en v5.6.x — Opción 2)      │
│                                                             │
│  CREATE MenuItem(function=F)  status=DRAFT                  │
│    └─ admin lo prueba                                       │
│         │                                                   │
│         └─ status=ACTIVE   (publicado al menu)              │
│              │                                              │
│              ├─ UPDATE label/icon/order   (PATCH MenuItem)  │
│              │                                              │
│              ├─ status=DEPRECATED  (marca de deprecación)   │
│              │   └─ frontend muestra con etiqueta "(legacy)"│
│              │                                              │
│              └─ status=ARCHIVED   (oculto pero preservado)  │
│                   └─ refs históricas válidas                │
└─────────────────────────────────────────────────────────────┘
```

### UCs nuevos derivados (Opción 2)

| UC | Capability | Acción |
|---|---|---|
| UC_ADM_04 | `manage_menu_catalog` | CRUD sobre `MenuItem` (admin) |
| UC_ADM_05 | `publish_menu_item` | Cambiar status DRAFT → ACTIVE |
| UC_ADM_06 | `deprecate_menu_item` | ACTIVE → DEPRECATED |
| UC_ADM_07 | `archive_menu_item` | DEPRECATED → ARCHIVED |

Todos asignados a AGR-010 (`system_admin_group`), siguiendo
patrón MOD_Admin.

## Sección 6 — Implicación para el WP `menu-rbac-user-scope-docs`

### 6.1 Replanteo del scope IN/OUT

**Phase 7 DESIGN debería ahora considerar:**

| Item | Status |
|---|---|
| Documentar UC_PERM_08 (Generar Menu Dinámico) | IN — extender con detalle de filtrado en frontend |
| Documentar `MenuItem` model como nueva entidad | IN si se elige Opción 2 |
| Documentar 4 UCs nuevos (UC_ADM_04..07) | IN si se elige Opción 2 |
| Endpoint `/api/menu-items/` para CRUD admin | IN si se elige Opción 2 |
| Endpoint `/api/permisos/verificar/{userId}/capacidades/` | IN |
| Reescribir CNST-032 | IN |
| Migración de C_MENU2 legacy a MenuItem v5.6.x | OUT (es trabajo backend, otro WP) |

### 6.2 Pregunta para el ejecutor antes de Phase 7

**Preguntas de cierre antes de avanzar:**

1. **¿Aprobar Opción 2 (MenuItem 1:1 con Function)?** O ¿prefiere Opción 1, 3, u otra?
2. **¿UC_ADM_04..07 nuevos UCs?** ¿O considerar que UC_ADM_02 absorbe la gestión de MenuItem también?
3. **¿Multi-tenancy en MenuItem (per segment)?** Mantener BR-012 estricto significa no, pero si el negocio lo requiere, abrir scope.
4. **¿Estados del MenuItem son 4 (DRAFT/ACTIVE/DEPRECATED/ARCHIVED)?** ¿O sets más simple (ACTIVE/INACTIVE)?

## Sección 7 — Auto-corrección

En el análisis previo (`menu-v560-design-and-id-convenio-equivalent.md`)
recomendé **Opción 3 (frontend ALL_NAV_LINKS estático +
backend solo capabilities)**. Eso era **incompleto** — no
abordaba lifecycle managed que el ejecutor planteó.

Este artefacto **complementa y refina** la recomendación
anterior. La decisión final de scope debe ser del ejecutor
en Phase 6 SCOPE.

## Refs

- Análisis previos:

  - ``menu-rbac-user-scope-docs-analysis.md``
  - ``cmenu2-legacy-archeology.md``
  - ``inserta-modulos-menu-sql-analysis.md``
  - ``index-asp-legacy-render-analysis.md``
  - ``menu-v560-design-and-id-convenio-equivalent.md``

- Catálogo Function v5.6.0:
  :doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones`.
- MOD_Admin (UC_ADM_01..03):
  :doc:`/requisitos/casos-uso/admin/index`.
- BR-012:
  :doc:`/requisitos/reglas-negocio/br-012-usuario-segmento-unico`.
- ADR-BACK-007:
  :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`.
- CNST-032 (a reescribir).
