```yml
created_at: 2026-05-06 22:25:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/inserta-modulos-menu-sql-analysis.md
artifact_origin: index.asp (legacy IACT — Reportes Automáticos)
```

# Arqueología ASP: `index.asp` legacy — render real del menú

## Contexto

Tras analizar:

1. La tabla legacy ``C_MENU2`` (``cmenu2-legacy-archeology.md``).
2. El script de inserción ``Inserta_modulos_menu.sql``.

El ejecutor compartió ahora un ``index.asp`` legacy real — la
**página que renderiza el menú al usuario**. Cierra el ciclo:
de cómo se creaba (script SQL), cómo se almacenaba (`C_MENU2`),
y ahora cómo se mostraba al usuario (este artefacto).

## Anatomía del archivo `index.asp`

### 1. Includes (directivas ``<!--#include file=...-->``)

```asp
<!--#include file="../../../connections/Session.asp"-->
<!--#include file="../../../connections/constants.asp"-->
<!--#include file="../../../connections/cConnection.asp"-->
<!--#include file="../../../DAO/TabControl.asp"-->
<!--#include file="../../../DAO/BitacoraVisitas.asp"-->
```

**Decodificación:**

| Include | Rol |
|---|---|
| `Session.asp` | Gestión de sesión ASP (popula ``Session("ID_CONVENIO")``, ``ID_USUARIO``, etc.) |
| `constants.asp` | Constantes globales (``DB_INI``, ``TabTypeFrames``, etc.) |
| `cConnection.asp` | Clase wrapper de conexión a BD (``con.startConnection``, ``con.executeQuery``, ``con.endConnection``) |
| `TabControl.asp` | Componente UI server-side de pestañas |
| `BitacoraVisitas.asp` | Audit log de navegación del usuario (``Call Bitacora_Visitas(...)``) |

**Observación crítica:** las rutas son relativas con
``../../../`` lo que sugiere una estructura de directorios
jerárquica donde este archivo está 3 niveles abajo de
``connections/``, ``DAO/``, etc. — **acoplamiento físico** al
filesystem del servidor.

### 2. Audit log de navegación (línea inicial)

```asp
Call Bitacora_Visitas ("REPORTES", "GENERADOR->REPORTES AUTOMATICOS")
```

**Significado:** cada vez que el usuario abre esta página, se
registra una entrada en el audit log con:

- Categoría: ``REPORTES``.
- Path lógico: ``"GENERADOR->REPORTES AUTOMATICOS"``.

**Implicación arqueológica:** el sistema legacy registraba
**cada vista de menú** en bitácora, no solo las acciones
funcionales. Esto es **audit overhead** comparado con el
patrón actual donde solo eventos de negocio (CNST-025) se
auditan.

### 3. Inicialización de sesión y default tab

```asp
DefaultTab = Request.QueryString("Tab")
if DefaultTab = "" then
    DefaultTab = 1
else
    DefaultTab = cint(DefaultTab)
end if
```

**Patrón:** el tab visible se controla via query string
(``index.asp?Tab=3``). Default = 1 (primer tab).

**Comparación con SPA moderna:** este patrón es equivalente
a React Router con ``useSearchParams`` — la diferencia es que
ASP renderiza server-side y SPA renderiza client-side.

### 4. Configuración del TabControl (componente UI)

```asp
Set MyTabControl = New TabControl
MyTabControl.TabSelected = DefaultTab
MyTabControl.ControlImagePath = "../../../IMAGES/TABS/"
MyTabControl.ControlScriptPath = "../../../JS/"
MyTabControl.TabType = TabTypeFrames
MyTabControl.TabHome = False
MyTabControl.Width = "99%"
```

**Decodificación crítica:**

| Property | Valor | Implicación |
|---|---|---|
| `TabSelected` | `DefaultTab` (int) | tab inicial visible |
| `ControlImagePath` | `"../../../IMAGES/TABS/"` | path a sprites de tabs (acoplado al filesystem) |
| `ControlScriptPath` | `"../../../JS/"` | path a scripts JS del componente |
| `TabType` | **`TabTypeFrames`** | usa HTML ``<frame>`` legacy |
| `TabHome` | `False` | sin tab "home" especial |
| `Width` | `"99%"` | ancho fluido |

**Hallazgo crítico:** ``TabType = TabTypeFrames`` significa
que **el sistema usaba HTML frames** — deprecado desde HTML5
(2014) por razones de UX, accesibilidad y SEO. Cada tab
abría un ``<frame src="...">``.

### 5. Código comentado (vestigios del pasado)

El bloque comentado revela una **versión anterior del código**:

```asp
'	sql = "SELECT *"
'	sql = sql + " FROM C_REPORTES_AUTO"
'	sql = sql + " WHERE C_REPORTES_AUTO.STATUS = 'ACTIVO'"
'	sql = sql + " ORDER BY C_REPORTES_AUTO.ID_REPORTE_AUTO"
```

**Tabla pre-`C_MENU2`: `C_REPORTES_AUTO`**

Antes de migrar al modelo `C_MENU2`, este módulo tenía una
tabla **dedicada** ``C_REPORTES_AUTO`` con su propio set de
filas (``ID_REPORTE_AUTO``, ``DESC_REPORTE_AUTO``).

Lógica complementaria comentada:

```asp
'	sql_temp = " SELECT ID_CONVENIO "&_
'				" FROM BD_CONVENIO_PRODUCTO "&_
'				" WHERE ID_PRODUCTO = 3 "
'
'	if cint(ID_CONVENIO) = temp then
'		if rs.fields("ID_REPORTE_AUTO") <> 12 then
'			MyTabControl.AddTab ...
'		end if
'	else
'		if rs.fields("ID_REPORTE_AUTO") <> 13 then
'			MyTabControl.AddTab ...
'		end if
'	end if
```

**Hallazgo crítico:** el código viejo **excluía pestañas
hardcoded** (``ID_REPORTE_AUTO <> 12`` y ``<> 13``) según el
``ID_CONVENIO`` del usuario. Es decir:

- Si el convenio del user matcheaba con `ID_PRODUCTO=3` →
  ocultar la pestaña ID=12.
- Si no → ocultar la pestaña ID=13.

**Anti-patrón legacy directo:** lógica de visibilidad de menú
**embebida en código ASP con números mágicos**. Para cambiar
qué pestaña ocultar, había que editar este archivo y
desplegar.

**Por qué se comentó:** se migró a ``C_MENU2 + BD_MENU2`` que
externaliza la decisión de visibilidad a la BD (vía join). El
nuevo modelo es más limpio pero el código viejo se conservó
comentado — **deuda histórica visible**.

### 6. Query activo: el corazón del sistema

```sql
SELECT M.ID_MENU
       ,M.DES_MENU
       ,M.DES_NAME
       ,M.HREF
FROM C_MENU2 M
INNER JOIN BD_MENU2 B
    ON B.ID_MENU0 = M.ID_PARENT
    AND B.ID_MENU1 = M.ID_MENU
WHERE M.ID_PARENT = 131
AND M.STATUS = 'ACTIVO'
AND B.ID_USUARIO = <ID_USUARIO>
AND B.ID_CONVENIO = <Session("ID_CONVENIO")>
ORDER BY M.ORDEN
```

**Decodificación detallada:**

| Cláusula | Significado |
|---|---|
| `FROM C_MENU2 M` | catálogo de menús (analizado en arqueología previa) |
| `INNER JOIN BD_MENU2 B` | fuerza que solo aparezcan menús con privilegio asignado |
| `B.ID_MENU0 = M.ID_PARENT AND B.ID_MENU1 = M.ID_MENU` | **clave compuesta** padre+hijo (sin FK formal a `ID_MENU`) |
| `M.ID_PARENT = 131` | **número mágico** — los hijos del nodo `ID_MENU=131` (probablemente "Reportes Automáticos") |
| `M.STATUS = 'ACTIVO'` | excluye los soft-deleted |
| `B.ID_USUARIO = <session>` | filtro per-user |
| `B.ID_CONVENIO = <session>` | filtro per-campaign (multi-tenant) |
| `ORDER BY M.ORDEN` | orden visual definido en `C_MENU2.ORDEN` |

**Hallazgos críticos:**

#### F-01 — JOIN compuesto sin FK formal

El JOIN usa **dos columnas** (``ID_MENU0 = ID_PARENT`` y
``ID_MENU1 = ID_MENU``). Esto sugiere que `BD_MENU2` no tiene
foreign key formal a `C_MENU2.ID_MENU` — la integridad
referencial es por convención, no enforced por la BD.

Esto hace posible **filas huérfanas** en `BD_MENU2`
(privilegios sobre menús que ya no existen).

#### F-02 — `ID_PARENT = 131` hardcoded en el view

El parent ID está **hardcoded en el archivo ASP**. Si el
admin reorganizara la jerarquía (renombrar/mover el padre),
**este archivo deja de funcionar**. Es acoplamiento entre
identidades de DB y código.

#### F-03 — Multi-tenant via `ID_CONVENIO` en sesión

El filtro `B.ID_CONVENIO = Session("ID_CONVENIO")` muestra
que el menú **depende del convenio activo del usuario en su
sesión actual**. Si el user trabaja en múltiples convenios,
**cambiar de convenio cambia el menú** — no es solo per-user,
es per-user-per-current-context.

#### F-04 — La visibilidad NO usa codename, usa identity

El JOIN `B.ID_MENU1 = M.ID_MENU` filtra por **ID numérico**,
no por `DES_MENU` (codename). Esto significa:

- Re-crear un menú en otro ambiente con el mismo `DES_MENU`
  pero distinto `ID_MENU` rompe los privilegios existentes.
- No hay "función abstracta" reusable entre ambientes.

#### F-05 — SQL injection vulnerability

```asp
"AND B.ID_USUARIO = " & ID_USUARIO & ""
"AND B.ID_CONVENIO = " & Session("ID_CONVENIO") & ""
```

**Concatenación directa de strings** sin parametrización.
Aunque ``ID_USUARIO`` y ``Session("ID_CONVENIO")`` vengan de
sesión (no de input directo), el patrón es **vulnerable a
SQL injection** si alguna de esas variables se expone en
otra ruta (o si el sistema de sesión es comprometido).

### 7. Manejo de "sin permisos"

```asp
If Not rs.EOF Then
    Do Until rs.EOF
        MyTabControl.AddTab rs.fields("DES_NAME"),"",rs.fields("HREF")
    rs.MoveNext
    Loop
Else
    Response.Write("No tiene privilegios para poder ver las pesta&ntilde;as.")
End If
```

**Patrón:**

- Si hay filas → agrega cada una como pestaña.
- Si no hay filas → escribe un mensaje en HTML.

**No 403, no redirect, no escalation.** Solo un texto plano.
Esto es **UX flat** sin distinguir "no tienes permiso" de
"no hay nada configurado".

### 8. Cleanup y close

```asp
rs.close
set rs = nothing
con.endConnection
```

**Patrón ASP Classic:** liberación manual de recursos. Si una
exception ocurre antes, los recursos quedan colgados (ASP
Classic no tiene `try/finally` robusto). Posible leak.

### 9. HTML mínimo

```html
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Siempre Creciendo</title>
</head>

<body style="margin-top:2px;margin-bottom:0px;margin-right:0px;margin-left:5px;">
    <%
    MyTabControl.Draw
    %>
</body>
</html>
```

**Hallazgos:**

- `<title>Siempre Creciendo</title>` — branding del proyecto
  o de la organización (preservar en docs).
- `<body style="...">` — **inline styles** (anti-patrón
  moderno; CSS debe ir en hojas separadas).
- `MyTabControl.Draw` — render server-side del componente.
  Genera el HTML completo de tabs en este punto.

## Comparación operativa: legacy ASP vs SPA moderna

| Aspecto | Legacy ASP (este archivo) | React/SPA moderna v5.6.0 |
|---|---|---|
| **Lenguaje** | ASP Classic (VBScript server-side) | TypeScript/React (client-side) |
| **Render** | Server-side (string concat) | Client-side (Virtual DOM) |
| **Paginación de tabs** | HTML `<frame>` (TabTypeFrames) | React Router `<Outlet>` o tabs UI |
| **Visibilidad por permiso** | INNER JOIN BD_MENU2 a nivel SQL | Filtrado JS sobre `ALL_NAV_LINKS` por capabilities del user |
| **Identidad del menú** | `ID_MENU` numérico (ad-hoc) | Codename de Function v5.6.0 (semántico) |
| **Multi-tenant** | `Session("ID_CONVENIO")` per request | `user.segment_id` (BR-012) |
| **Cambio de orden** | UPDATE C_MENU2.ORDEN | Reorder en config React |
| **Cambio de URL** | UPDATE C_MENU2.HREF | Cambio en React Router |
| **Audit del visit** | `Bitacora_Visitas("REPORTES",...)` server-side | Frontend puede emitir telemetría a backend si se requiere (P-51) |
| **Manejo de "sin perms"** | `Response.Write` texto plano | UI consistente: lista vacía o redirect informativo |
| **SQL injection** | Vulnerable (string concat) | Django ORM parametriza automáticamente |
| **Resource cleanup** | Manual (`rs.close`, `con.endConnection`) | Context managers/auto-cleanup en Django |

## Hallazgos consolidados

### F-A — Múltiples generaciones de UI conviviendo

El archivo muestra **dos generaciones** del rendering de menú:

1. **Generación 0** (comentada): query a tabla dedicada
   ``C_REPORTES_AUTO`` con lógica de exclusión hardcoded.
2. **Generación 1** (activa): query a ``C_MENU2 + BD_MENU2``
   con join compuesto.

La **Generación 2** (canónica IACT v5.6.0) **deprecaría
ambas** y movería todo el rendering a frontend con
``ALL_NAV_LINKS`` filtrado por capabilities.

### F-B — La tabla ``C_REPORTES_AUTO`` reveló otro modelo legacy

Antes de ``C_MENU2``, había **tablas dedicadas por dominio**
(`C_REPORTES_AUTO`, presumiblemente `C_USUARIOS_FUNC`,
`C_REPORTES_MANUAL`, etc.). El equipo consolidó en ``C_MENU2``
como tabla genérica de menús — **paso intermedio antes de
function-centric v5.6.0**.

### F-C — Audit log de navegación = audit overhead

`Bitacora_Visitas("REPORTES", "GENERADOR->REPORTES
AUTOMATICOS")` ejecuta en cada GET. Esto produce **alto
volumen de eventos** (cada user navegando genera audit row).

P-51 (read-no-audit) en el corpus actual evita exactamente
este overhead — solo se auditan **acciones**, no
**visualizaciones** (excepto cuando el dominio lo exige
explícitamente, ej. UC_AUD_03 tiene audit propio).

### F-D — Acoplamiento físico al filesystem

Las rutas ``../../../`` indican estructura jerárquica fija.
Mover este archivo rompe los includes. Esto se evita en SPA
moderno via imports relativos al package o aliases (e.g.
``@/components/TabControl``).

### F-E — Frame-based UI = deprecated

`TabType = TabTypeFrames` usa HTML frames, deprecado.
Implicaciones para migración:

- Frame `src` mapea a una ruta SPA.
- Cada tab en SPA = ruta independiente con `<Outlet>` o
  componente lazy-loaded.
- No hay "frame switching" — hay React state.

### F-F — Lógica de visibilidad embebida en archivo (Generación 0)

El bloque comentado mostraba lógica `ID_REPORTE_AUTO <> 12`
condicionada a ``ID_CONVENIO`` — **business rule en código
ASP**, no en BD ni en RBAC.

Migración correcta v5.6.0:

- Si "no mostrar reporte X cuando convenio = Y" es regla de
  negocio → modelar como permission codename + asignación
  AGR.
- NO embedir condicionales en archivos de view.

## Implicaciones para el WP `menu-rbac-user-scope-docs`

### Implicación 1 — El modelo legacy era SQL JOIN, NO SQL function

Curiosamente, `index.asp` ejecuta el query INLINE en la página,
**no usa una SQL function** como ``obtener_menu_usuario`` que
CNST-032 obliga.

Esto significa:

- El sistema legacy **no tenía** ``obtener_menu_usuario`` —
  cada página construía su propio query con join hardcoded.
- ``obtener_menu_usuario`` es **innovación posterior** (de
  temp-holding ``UC-PERM-008_generar_menu_dinamico.md``)
  que centralizaba la lógica.
- CNST-032 obliga la SQL function como **mejora** sobre el
  patrón legacy (que es lo que muestra `index.asp`).

**Para el WP:** la migración correcta es **NO replicar** ni
``obtener_menu_usuario`` ni el query inline. El frontend
v5.6.0 hace su propio filtrado en el cliente sobre
``ALL_NAV_LINKS`` consultando capabilities por separado
(endpoint ``/api/permisos/verificar/{id}/capacidades/``).

CNST-032 puede necesitar **deprecación o reescritura** en
Phase 7 DESIGN del WP.

### Implicación 2 — La visibilidad por convenio es un gap real

`Session("ID_CONVENIO")` es **filtro real** del modelo legacy.
v5.6.0 maneja esto via ``user.segment_id`` (BR-012, "Usuario
Segmento Único") pero la **lógica de "convenio activo"** no
es lo mismo que "segmento del user":

- Convenio = contexto de trabajo cambiable (multi-tenant).
- Segmento = atributo permanente del user.

**Pregunta abierta:** ¿IACT v5.6.0 soporta múltiples convenios
por user con switching dinámico? Si sí, se necesita
``current_convenio`` adicional al ``segment_id``. Si no, los
multi-tenant scenarios del legacy no migran 1:1.

**Recomendación para Phase 7:** documentar explícitamente
si v5.6.0 mantiene/deprecia el concepto de "convenio
multi-contexto" del legacy.

### Implicación 3 — Audit overhead heredado

El patrón ``Bitacora_Visitas`` legacy auditaba navegación. P-51
en v5.6.0 prohíbe esto.

**Para el WP:** documentar como anti-patrón en Phase 7:
"NO replicar audit log de navegación por defecto. P-51
limita audit a acciones de negocio, no a visualizaciones."

### Implicación 4 — SQL injection guardrails

El patrón ``"WHERE x = " & var & ""`` legacy es vulnerable.
Migración a Django ORM resuelve esto pero **debe ser test
guardrail**:

- Test integración: verificar que el endpoint ``capacidades``
  no es vulnerable a ``user_id = '1; DROP TABLE'``.

## Consolidación: 3 generaciones de menú IACT

| Generación | Tecnología | Tablas | Lógica de visibilidad |
|---|---|---|---|
| **G0** (más antigua) | ASP Classic + tabla dedicada | `C_REPORTES_AUTO` + condicionales hardcoded en `.asp` | Embebida en código del view (`<> 12`, `<> 13` por convenio) |
| **G1** (mid) | ASP Classic + tabla genérica | `C_MENU2` + `BD_MENU2` con join | SQL JOIN inline en cada `.asp` |
| **G2** (transición temp-holding) | Django + SQL function | `obtener_menu_usuario(user_id)` retorna JSONB | Centralizada en SQL function |
| **G3** (canónica v5.6.0 IACT) | React SPA + custom permission backend | `Function` + `AccessGroup` + `UserAccessGroupAssignment` | Frontend filtra `ALL_NAV_LINKS` con capabilities del user |

Cada generación corrige defectos de la anterior:

- G0 → G1: extrae lógica de visibility a BD (deja de estar en cada `.asp`).
- G1 → G2: centraliza en SQL function (un solo lugar de query).
- G2 → G3: mueve a frontend (SPA), backend solo entrega capabilities.

## Refs

- Archivo analizado: ``index.asp`` (legacy IACT — Reportes
  Automáticos), provisto por ejecutor 2026-05-06.
- Análisis previos:

  - ``cmenu2-legacy-archeology.md``.
  - ``inserta-modulos-menu-sql-analysis.md``.

- Análisis principal: ``menu-rbac-user-scope-docs-analysis.md``.
- Corpus vigente afectado:

  - UC_PERM_08: :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.
  - CNST-032: :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio` (revisar para Phase 7).
  - P-51 (read-no-audit): patrón documentado en UC_RPT_01 y otros.
  - BR-012 (Usuario Segmento Único): :doc:`/requisitos/reglas-negocio/br-012-usuario-segmento-unico`.

- Backend pre-corpus relacionado:
  ``temp-holding/Modules/call_center_privilege_models.py``,
  ``temp-holding/FASE 01/docs/backend/UC-PERM-008_generar_menu_dinamico.md``.
