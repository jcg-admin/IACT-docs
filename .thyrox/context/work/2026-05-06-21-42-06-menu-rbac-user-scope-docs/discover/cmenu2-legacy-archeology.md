```yml
created_at: 2026-05-06 21:55:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/menu-rbac-user-scope-docs-analysis.md
```

# Arqueología: tabla `C_MENU2` legacy — origen del sistema de menús IACT

## Trigger

Ejecutor solicitó: *"buscar en `temp-holding/` el nacimiento de
lo anterior, fue un ejemplo que se usaba una tabla cmenu2.
Analizar y documentar los hallazgos."*

## Búsqueda ejecutada

Variantes consultadas (case-insensitive) en `temp-holding/`:

```
cmenu2     → 0 archivos
cmenu      → 0 archivos
c_menu     → 3 archivos
menu_2     → 1 archivo
menu2      → 3 archivos
MENU2      → 3 archivos
v_menu     → 2 archivos (UC_PERM_08 SQL function variable)
```

**Conclusión de búsqueda:** la referencia exacta en el código
legacy es **`C_MENU2`** (no `cmenu2`). Aparece en:

- `temp-holding/Modules/call_center_privilege_models.py`
- `temp-holding/Modules/department_privilege_system.py`
- `temp-holding/Modules/privilege_flow_diagram.py`

## Hallazgo principal: el sistema legacy ASP/ASP.NET

La tabla `C_MENU2` es de un sistema **legacy ASP** (campos
`HREF: 'menu.asp'`, `'index.asp'`, `'dashboard-agente.asp'` lo
delatan), reescrito a Django manteniendo compatibilidad de
nombres de columnas (UPPERCASE, prefijos `ID_`, `DES_`).

## Esquema legacy reconstruido

### Tabla 1 — `C_MENU2`: catálogo de menús/módulos

```python
class CallCenterModule(models.Model):
    """
    Módulos específicos del Call Center
    Extiende C_MENU2 con campos relevantes al dominio
    """
    # Campos legacy compatibles
    ID_MENU = models.AutoField(primary_key=True)
    NIVEL = models.IntegerField(default=1)
    ID_PARENT = models.IntegerField(null=True, blank=True)
    DES_MENU = models.CharField(max_length=100, unique=True)
    DES_NAME = models.CharField(max_length=200)
    STATUS = models.CharField(
        max_length=10,
        choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')],
        default='ACTIVO',
    )
    TARGET = models.CharField(max_length=20, default='main')
    IMAGE = models.CharField(max_length=100, null=True, blank=True)
    HREF = models.CharField(max_length=200, default='index.asp')
    ORDEN = models.IntegerField(default=1)
    # ... campos Call Center extendidos
```

**Semántica de los campos legacy:**

| Campo | Tipo | Rol | Ejemplo |
|---|---|---|---|
| `ID_MENU` | PK autoincrement | identidad del nodo | `42` |
| `NIVEL` | int | profundidad jerárquica | `1` (raíz), `2` (hijo), ... |
| `ID_PARENT` | FK self | padre en el árbol | `null` raíz; `5` hijo de menú #5 |
| `DES_MENU` | CHAR(100) UNIQUE | codename interno | `'OPERACIONES'`, `'DASHBOARD_AGENTE'` |
| `DES_NAME` | CHAR(200) | display name (UX) | `'Operaciones'`, `'Mi Dashboard'` |
| `STATUS` | CHAR(10) | activo/inactivo | `'ACTIVO'` |
| `TARGET` | CHAR(20) | frame target legacy ASP | `'main'` (frameset) |
| `IMAGE` | CHAR(100) | icono | path a `.gif`/`.png` |
| `HREF` | CHAR(200) | URL | `'menu.asp'`, `'reportes.asp?id=5'` |
| `ORDEN` | int | orden visual | `1`, `2`, `3` ... |

### Tabla 2 — `BD_MENU2`: M2M user ↔ menú con privilegios

```python
class BD_MENU2(models.Model):
    """
    Privilegios de usuario sobre menús
    El ID_CONVENIO ahora puede representar diferentes contextos
    """
    ID_MENU0 = models.IntegerField(default=0)
    ID_MENU1 = models.ForeignKey(
        C_MENU2, on_delete=models.CASCADE,
        db_column='ID_MENU1',
        related_name='user_privileges',
    )
    ID_USUARIO = models.ForeignKey(
        CallCenterUser, on_delete=models.CASCADE,
        db_column='ID_USUARIO',
        related_name='menu_privileges',
    )
    ID_CONVENIO = models.IntegerField(
        default=1,
        help_text="Contexto/campaña",
    )
    can_read = models.BooleanField(default=True)
    can_write = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_export = models.BooleanField(default=False)
```

**Semántica:** una fila de `BD_MENU2` = "user `X` puede acceder
al menú `Y` en el contexto del convenio `Z` con permisos
{read, write, delete, export}".

### Tabla 3 — `BD_MENU_CONVENIO`: contexto por campaña

Mencionada en el código (línea 6 de `department_privilege_system.py`):

> *"Similar a BD_MENU_CONVENIO pero a nivel departamento"*

No tengo el esquema explícito pero se infiere: M2M entre
`Convenio` (campaña) y `C_MENU2` (qué menús están disponibles
para qué campaña, antes de asignar a usuarios).

## Estructura jerárquica del menú legacy (extraída del seed)

`privilege_flow_diagram.py` líneas 17-260 declara el seed con
3+ niveles de profundidad. Ejemplo verbatim:

```python
# MÓDULOS DE OPERACIONES
{
    'DES_MENU': 'OPERACIONES',
    'DES_NAME': 'Operaciones',
    'NIVEL': 1,
    'ID_PARENT': None,
    'owner': 'OPERACIONES',
    'departments': ['OPERACIONES'],
    'children': [
        {'DES_MENU': 'DASHBOARD_AGENTE',
         'DES_NAME': 'Mi Dashboard',
         'HREF': 'dashboard-agente.asp'},
        {'DES_MENU': 'MIS_METRICAS',
         'DES_NAME': 'Mis Métricas',
         'HREF': 'metricas-personales.asp'},
        {'DES_MENU': 'BASE_CONOCIMIENTO',
         'DES_NAME': 'Base de Conocimiento',
         'HREF': 'knowledge-base.asp'},
    ],
},
```

## Modelo de privilegios legacy: comparación con RBAC v5.6.0

| Aspecto | Sistema legacy (C_MENU2 + BD_MENU2) | RBAC v5.6.0 (corpus actual) |
|---|---|---|
| **Unidad de permiso** | Fila en tabla menú (`C_MENU2`) | Codename atómico (`Function`) |
| **Quién define los permisos** | El menú: si está en C_MENU2, es asignable | El catálogo `Function`: 64 codenames in-scope |
| **Granularidad** | 4 flags por fila: read/write/delete/export | 1 codename atómico (verbo + sustantivo) |
| **Asignación a user** | `BD_MENU2(user, menu, convenio, perms)` | `UserAccessGroupAssignment(user, AGR)` |
| **Contexto multi-tenant** | `ID_CONVENIO` (campaña) | `segment_id` en User (BR-012) |
| **Rendering del menú** | Query directo a `C_MENU2 JOIN BD_MENU2 WHERE ID_USUARIO=X` | SQL function `obtener_menu_usuario(user_id)` deriva desde codenames |
| **Naming** | UPPERCASE legacy ASP (`DES_MENU`, `HREF`) | snake_case Django (`codename`, `module`) |
| **Identidad del nodo** | `ID_MENU` autoincrement | `agr_code` natural key (AGR-001..012) |
| **Jerarquía** | Self-FK explícita (`ID_PARENT`) | Derivable del codename (module + verbo + sustantivo) |
| **Status** | `STATUS = 'ACTIVO'/'INACTIVO'` | `is_active` + `is_system` |

## Análisis del cambio de paradigma

### Paradigma legacy: **menu-centric**

> "El menú define el permiso. Si el menú existe en `C_MENU2` y
> el user tiene fila en `BD_MENU2`, puede acceder."

Consecuencias:

- Cualquier nueva función UI requiere INSERT en `C_MENU2`.
- Permission grants son por menu-row, no por capability lógica.
- Difícil reutilizar el mismo permiso desde múltiples lugares.
- HREF acoplado al permiso (cambio de URL = cambio de schema).

### Paradigma actual v5.6.0: **function-centric**

> "La función atómica define el permiso. El menú es solo
> rendering UX derivado del set de funciones del user."

Consecuencias:

- 64 funciones in-scope son contrato estable.
- Una función (ej. `view_reports`) puede aparecer en múltiples
  rutas UI sin duplicar permisos.
- HREF/UI puede cambiar sin tocar el modelo de permisos.
- Defense-in-depth: enforcement en endpoint + opcionalmente
  filtrado en menu (no al revés).

## Origen real de UC_PERM_08 + CNST-032

Con esta arqueología queda claro el origen:

1. **Existía** un sistema legacy donde el menú = la fuente de
   permisos (`C_MENU2` + `BD_MENU2`).
2. El equipo migró a un **modelo RBAC plano** (ADR-BACK-001) +
   funciones atómicas (Q6: snake_case verb-noun).
3. Pero **el frontend ya estaba acostumbrado** a renderizar
   menús estáticos a partir del query a `C_MENU2`. Ese es el
   anti-patrón que CNST-032 prohíbe explícitamente:

   *"Está prohibido renderizar menu estático, hardcoded o
   calculado en frontend basado en roles enumerados."*

4. UC_PERM_08 **preserva la API mental** del menú dinámico
   (frontend pide menú, backend lo entrega) **sin** mantener
   la deuda técnica del modelo `C_MENU2`. La SQL function
   `obtener_menu_usuario(user_id)` es el nuevo punto de
   indirección que permite que el menú sea **derivado** del
   `effective_set` del user.

## Implicación para el WP `menu-rbac-user-scope-docs`

### Decisión arquitectónica reforzada

Esta arqueología **valida la Lectura B** del análisis principal
(jerarquía derivable del codename sin metadata extra):

- Mantener metadata legacy (`HREF`, `IMAGE`, `ORDEN`) en una
  tabla `MenuMetadata` separada **NO** es necesario.
- El frontend conoce sus propias rutas (React Router) y sus
  propios iconos (componentes); no necesita que el backend
  le diga `'dashboard-agente.asp'`.
- El backend solo debe responder: "para este user, ¿qué set
  de codenames tiene?". El frontend agrupa, ordena y enruta.

### Anti-patrón a evitar explícitamente

Reintroducir un equivalente moderno de `C_MENU2` (tabla con
`HREF`, `ORDEN`, `IMAGE`) en el modelo Django sería **regresión
arquitectónica**. El frontend WP `menu-rbac-user-scope` ya está
correctamente alineado: filtra `ALL_NAV_LINKS` (constante en
código React) por capabilities del user — **NO consulta tabla
de menús del backend**.

### Documentación recomendada para Phase 7 DESIGN

1. **Sección histórica en UC_PERM_08** o nuevo documento de
   contexto: "Origen del menú dinámico — del paradigma
   menu-centric (C_MENU2) al function-centric (RBAC v5.6.0)".
2. **NFR explícito de no-regresión**:
   "El backend no expone una tabla de menús con HREF/ORDEN.
   El menú es derivado funcionalmente desde
   `effective_set` del user."
3. **Diagrama de transición** legacy → actual para que cualquier
   dev que llegue después entienda por qué la spec actual NO
   modela `HREF` en backend.

## Refs

- Archivos legacy analizados:
  - `temp-holding/Modules/call_center_privilege_models.py`
  - `temp-holding/Modules/department_privilege_system.py`
  - `temp-holding/Modules/privilege_flow_diagram.py`
- Análisis principal: `discover/menu-rbac-user-scope-docs-analysis.md`.
- Corpus vigente afectado:
  - UC_PERM_08 (`source/requisitos/casos-uso/permissions/uc-perm-08/`)
  - CNST-032 (`source/normativa/restricciones/cnst-032-menu-dinamico-obligatorio.rst`)
  - ADR-BACK-001 (modelo flat sin jerarquía — refuerza el cambio de paradigma)
  - ADR-BACK-007 (custom RBAC vs auth.Group)
- Research previo:
  WP-5 ``2026-05-06-19-27-21-agr-django-permission-groups-research``.
