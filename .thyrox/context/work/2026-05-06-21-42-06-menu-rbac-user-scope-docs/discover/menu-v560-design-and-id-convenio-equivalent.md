```yml
created_at: 2026-05-06 22:45:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
parent_analysis: discover/index-asp-legacy-render-analysis.md
```

# Cómo manejaríamos el menú en v5.6.0 + análisis del equivalente de `ID_CONVENIO`

## Trigger

Ejecutor planteó dos preguntas:

1. *"¿cuál sería nuestro identificador equivalente al ``ID_CONVENIO`` del legacy?"*
2. *"mencionas ``user.segment_id`` pero habíamos dicho que estaba fuera del scope, revisa los WP sobre esas decisiones antes de continuar."*

Antes de responder, revisé los WPs y el corpus. Documento aquí
**lo que canónicamente se decidió** + **propuesta v5.6.0 para
manejar el menú**.

## Sección 1 — Verificación de decisiones de scope (corpus + WPs)

### 1.1 ¿Está `segment_id` fuera de scope?

**NO.** `segment_id` está **dentro de scope** y es **canónico
v5.6.0**. Verificado en:

- **BR-012** "Usuario Segmento Único"
  (`source/requisitos/reglas-negocio/br-012-usuario-segmento-unico.rst`)
  estado **Aprobado**, criticidad **Alta**:

  > *"Cada usuario operativo del sistema IACT DEBE estar
  > asociado a **exactamente un segmento de datos**
  > (DataSegment) que delimita el alcance de los datos que
  > puede consultar (centro, campaña, servicio, o región). El
  > segmento es asignado por un administrador con la función
  > ``manage_segments``. Un usuario sin segmento NO puede
  > consultar reportes operativos."*

- **TD-ACC-05** resuelto (WP `corpus-tech-debt-cleanup`):

  > *"NO requiere endpoint separado. Per BR-012 (Usuario
  > Segmento Único), el segmento es atributo del User.
  > Operación canónica: ``PATCH /users/{userId}/`` con
  > ``{segment_id}`` (mismo endpoint de UC_USR_03)."*
  > — STD-013 §"TD-ACC-05".

- **UC_INC_RPT_01** "Resolver Segmento del Usuario" — UC de
  inclusión (``<<include>>``) usado por TODOS los UC_RPT_*.
  Define que el usuario puede tener acceso a **uno, varios o
  todos** los segmentos IVR (``nacional_A``, ``nacional_B``,
  ``Puebla``). Estado: Vigente.

### 1.2 ¿Qué SÍ está fuera de scope en v5.6.0?

Verificado en `wp-state.md` de `2026-05-06-09-02-26-rbac-v5-6-0-corpus-alignment`:

| Elemento | Status | Razón |
|---|---|---|
| MOD_Operator (10 funciones) | RESERVADO open-closed | Extension point, no implementable v5.6.0 |
| MOD_Supervision (3 funciones) | RESERVADO open-closed | Extension point |
| MOD_Caller | Out-of-scope | Por diseño (design-view-buildout) |
| **Multi-tenant convenio dinámico** (switching de convenio en sesión) | **NO modelado en v5.6.0** | BR-012 fija 1 segmento por user (no switchable) |

### 1.3 Resolución de la posible confusión

El ejecutor probablemente refería al concepto **"convenio
multi-tenant dinámico"** del legacy (``Session("ID_CONVENIO")``
cambiable per request) — eso **SÍ está fuera de scope**.

Pero **`segment_id` per BR-012 está in-scope**: es un atributo
permanente del User, no un selector de contexto cambiable.

**Aclaración para el WP:** mi análisis previo de `index.asp`
mencionaba ``user.segment_id`` como equivalente del
``ID_CONVENIO`` — eso era **incorrecto semánticamente**. El
``ID_CONVENIO`` legacy es contexto cambiable; ``segment_id``
v5.6.0 es atributo permanente. **No son equivalentes 1:1.**

## Sección 2 — ¿Cuál es nuestro equivalente de `ID_CONVENIO`?

### Respuesta directa

**v5.6.0 NO tiene equivalente directo de ``ID_CONVENIO``** —
y esa es una decisión arquitectónica deliberada, no un gap.

### Por qué no hay equivalente directo

| Aspecto | `ID_CONVENIO` (legacy) | v5.6.0 |
|---|---|---|
| Concepto | Contexto activo del user en su sesión | Atributo permanente del User |
| Cardinalidad | User puede pertenecer a múltiples convenios y cambiar | User pertenece a exactamente 1 segmento (BR-012) |
| Persistencia | Por session (`Session("ID_CONVENIO")`) | En el modelo User (DB) |
| Cambio dinámico | Sí (UI tipo dropdown convenio) | No (admin asigna segmento; no switchable) |
| Filtra menú | Sí (`BD_MENU2.ID_CONVENIO = Session(...)`) | No (menú no depende de segmento) |
| Filtra datos | Sí (cada query filtraba por `ID_CONVENIO`) | Sí (UC_INC_RPT_01 filtra reports queryset por `segment_id`) |

### Si v5.6.0 alguna vez necesita el concepto

Si en el futuro IACT requiere multi-tenancy dinámica (un user
en múltiples campañas con switching), las opciones son:

- **Opción A** — Modificar BR-012 para permitir N segmentos
  por user. Agregar al modelo User un campo
  `current_segment_id` (foreign key a uno de los segmentos
  del user, modificable per session).
- **Opción B** — Modelar **Campaign** como entidad propia
  separada de DataSegment (similar a `Campaign` en
  `temp-holding/Modules/call_center_privilege_models.py`).
  Cada user tiene M2M con Campaigns + un Campaign activo.
- **Opción C** — JWT claim de "scope activo" que el user
  selecciona al login.

**Estado actual:** ninguna de las 3 opciones está modelada en
v5.6.0. Sería expansión de scope que requiere ADR + nuevo WP.

### Para el menú v5.6.0 específicamente

**El menú v5.6.0 NO debe depender de un equivalente de
`ID_CONVENIO`.** Razones:

1. El menú es **derivado de capabilities** (Function codenames
   asignados al user via AGRs).
2. Las capabilities son **globales** — no varían por contexto
   de campaña.
3. El **filtrado de datos** (que sí depende del segmento) ocurre
   en los reports/endpoints, NO en el menú.

Implicación: si un user tiene la capability `view_reports`,
**el ítem de menú "Reportes" se muestra** independientemente
de su segmento. Cuando el user entra al reporte, el reporte
filtra los datos por su segmento — pero el menú se mostró igual.

## Sección 3 — Diseño v5.6.0 del menú: cómo lo manejaríamos

### 3.1 Arquitectura conceptual

```
┌───────────────────────────────────────────────────────────────┐
│  FRONTEND (React SPA)                                         │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ ALL_NAV_LINKS  (constante en código React)              │  │
│  │                                                         │  │
│  │  [                                                      │  │
│  │    { path: '/reports',  required: ['view_reports'] },   │  │
│  │    { path: '/users',    required: ['view_users'] },     │  │
│  │    { path: '/audit',    required: ['view_audit_log'] }, │  │
│  │    ...                                                  │  │
│  │  ]                                                      │  │
│  └─────────────────────────────────────────────────────────┘  │
│                            │                                  │
│                            ▼ filter()                         │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Sidebar = ALL_NAV_LINKS                                │  │
│  │            .filter(link =>                              │  │
│  │              link.required.every(c =>                   │  │
│  │                userCapabilities.includes(c))            │  │
│  │            )                                            │  │
│  └─────────────────────────────────────────────────────────┘  │
│                            ▲                                  │
└────────────────────────────│──────────────────────────────────┘
                             │ GET /api/permisos/verificar/{userId}/capacidades/
                             │ → { capabilities: ['view_reports', 'export_csv', ...] }
                             ▼
┌───────────────────────────────────────────────────────────────┐
│  BACKEND (Django + DRF)                                       │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  GET /api/permisos/verificar/{userId}/capacidades/      │  │
│  │                                                         │  │
│  │  → custom permission backend                            │  │
│  │  → user.access_groups.functions.codename                │  │
│  │  → Set[str]  (codenames del user)                       │  │
│  └─────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

### 3.2 Decisiones de diseño aplicadas

| Decisión | Valor v5.6.0 | Justificación |
|---|---|---|
| **Fuente de verdad del set de menús** | `ALL_NAV_LINKS` (constante en código React) | F-01 del análisis SQL: legacy tenía menús en BD = release SQL por cada cambio. v5.6.0 mueve a código → versionado, testeable. |
| **Fuente de verdad de capabilities del user** | Backend endpoint `/api/permisos/verificar/{userId}/capacidades/` | Single source of truth. Frontend cachea pero no calcula. |
| **Resolución del filtrado** | Cliente (React filter sobre ALL_NAV_LINKS) | La UX del menú es responsabilidad del frontend; el backend solo entrega capabilities. |
| **Identidad del nodo** | Codename de Function (`view_reports`) + path React (`/reports`) | F-04: codename semántico + ruta SPA. Sin acoplamiento autoincrement. |
| **Jerarquía** | Derivable del codename (`module` field + verbo + sustantivo) | Decisión Lectura B reforzada por arqueología. Sin tabla `Menu` con `parent_id`. |
| **Orden visual** | Configuración en componente React (no en BD) | F-05: legacy tenía `ORDEN` con espaciamiento manual → renumeración masiva. Frontend ordena por agrupación lógica. |
| **Multi-tenant dinámico** | NO modelado en v5.6.0 | Scope decision documentada en BR-012 (1 segmento permanente). |
| **Audit del visit** | NO (P-51) | F-C del index.asp: legacy auditaba navegación = overhead. v5.6.0 audita solo acciones. |
| **Cache** | Frontend cachea capabilities en memoria/localStorage; invalida al login y al cambio de permisos vía signal | Replace de `obtener_menu_usuario` SQL function (que era G2 transición, no v5.6.0). |
| **Defense-in-depth** | Endpoint protegido SIEMPRE (custom permission backend) + menú solo es UX | UC_PERM_08 patrones-diseño + CNST-032. |

### 3.3 Endpoints canónicos del backend

```
GET /api/permisos/verificar/{userId}/capacidades/
    → 200 OK
    {
      "user_id": 42,
      "access_groups": ["AGR-002", "AGR-005"],
      "capabilities": [
        "view_reports", "view_alerts", "view_kpis",
        "export_csv", "configure_alerts", ...
      ],
      "expires_at": null  // null si ninguno tiene expiración
    }
```

**No se necesita endpoint `/menu/` separado.** El frontend
cruza este set con `ALL_NAV_LINKS` localmente. Esto difiere
de:

- **G2 (temp-holding) `obtener_menu_usuario`**: backend
  retornaba JSONB jerárquico ya parseado. v5.6.0 NO necesita
  esto: la jerarquía es responsabilidad del frontend.
- **Legacy G1 `index.asp`**: backend renderizaba HTML
  directamente. v5.6.0 separa render (frontend) de datos
  (backend).

### 3.4 Comparación con el SP-01 del frontend WP

El frontend WP `menu-rbac-user-scope` planteó:

> *"El endpoint ``/api/permisos/verificar/{userId}/capacidades/``
> no tiene handler en mockInterceptor.js. El sistema usePermisos
> carga del permissions.json directamente."*

**Resolución v5.6.0:** **el endpoint debe ser explícito**. El
mock interceptor debe responder a este URL con el set de
capabilities correspondiente al user. No bypass.

Justificación reforzada por esta arqueología:

- Legacy también consultaba "qué puede ver el user" desde la
  base — el mecanismo cambió pero el contrato de "API de
  capabilities" permanece.
- Bypassear el contrato implica que cuando llegue el backend
  real, hay refactor.

### 3.5 ¿Y para los reportes que SÍ dependen del segmento?

El segmento del user (per BR-012) afecta los **datos** que ve,
no los **menús**. Implementación:

```
GET /api/reports/centros-xsegmento/?period=today
   ↓
Custom permission backend verifica view_reports
   ↓ (permite)
ReportingService llama callproc(sp_rpt_centros_xsegmento, [period, user.segment_id])
   ↓
SP retorna solo datos del segmento del user (UC_INC_RPT_01)
   ↓
Backend retorna response con ese subset
```

Es decir:

- Menú: muestra "Reportes" (basado en `view_reports` capability).
- Click en "Reportes": navega a `/reports`.
- `/reports` ejecuta query con filtro `segment_id = user.segment_id` (UC_INC_RPT_01).
- User ve datos filtrados por su segmento.

**El menú NUNCA filtra por segmento.** Eso siempre ocurre en
el endpoint de datos.

### 3.6 Si un user no tiene segmento

Per BR-012: *"Un usuario sin segmento NO puede consultar
reportes operativos."*

Implementación:

- Si `user.segment_id is None` y user tiene `view_reports`:
  - El menú **igual muestra "Reportes"** (la capability existe).
  - Al click, el endpoint retorna **400 USER_WITHOUT_SEGMENT**
    o redirige a página informativa.
  - Es responsabilidad del UX informar el problema, NO del menú.

Esto es **defense-in-depth correcto**: separa menú (UX) de
enforcement (datos).

## Sección 4 — Recomendaciones para Phase 7 DESIGN del WP

### 4.1 Documentar respuestas a las dos preguntas del ejecutor

1. **`segment_id` está in-scope** (BR-012). NO es equivalente
   directo de `ID_CONVENIO`.
2. **`ID_CONVENIO` legacy NO tiene equivalente directo** en
   v5.6.0. Es decisión deliberada (multi-tenant dinámico
   fuera de scope).
3. **El menú v5.6.0 NO depende de segmento ni de convenio.**
   Solo depende de capabilities.

### 4.2 Documentar la separación menú vs datos

Crear sección explícita en UC_PERM_08 (o nuevo doc):

- "Capabilities determinan **qué menús el user ve**."
- "`segment_id` determina **qué datos el user ve dentro de
  cada menú**."
- "Son dos planos ortogonales — confundirlos = regresión al
  paradigma legacy."

### 4.3 Deprecar/reescribir CNST-032

CNST-032 dice verbatim:

> *"El frontend del sistema IACT DEBE invocar la función SQL
> nativa ``obtener_menu_usuario(user_id)`` para construir la
> estructura de navegación..."*

**Problema:** esto se basaba en G2 (`obtener_menu_usuario`)
de temp-holding. v5.6.0 (G3) no usa esa SQL function — el
frontend filtra `ALL_NAV_LINKS` con capabilities.

**Acción Phase 7:** reescribir CNST-032 a:

> *"El frontend del sistema IACT DEBE construir el menú de
> navegación filtrando una constante de rutas conocidas
> (``ALL_NAV_LINKS``) por el set de capabilities del usuario
> autenticado, obtenido vía endpoint canónico
> ``/api/permisos/verificar/{userId}/capacidades/``. Está
> prohibido renderizar menú estático sin filtrado, hardcoded
> por roles enumerados, o construido en backend con tablas de
> menús (anti-patrón legacy ``C_MENU2``)."*

### 4.4 Documentar formalmente que "convenio" no es scope

Agregar al WP `menu-rbac-user-scope-docs` un anti-patrón
explícito:

> *"NO modelar 'convenio activo' del user. v5.6.0 fija un
> segmento permanente per BR-012. Si el negocio requiere
> multi-tenant dinámico, abrir nuevo WP que modifique BR-012
> o introduzca Campaign entity (ver sección 'Si v5.6.0 alguna
> vez necesita el concepto')."*

## Sección 5 — Auto-corrección de mi análisis previo

En `index-asp-legacy-render-analysis.md` § "Implicación 2"
escribí:

> *"v5.6.0 maneja esto via ``user.segment_id`` (BR-012,
> 'Usuario Segmento Único') pero la **lógica de 'convenio
> activo'** no es lo mismo que 'segmento del user': Convenio
> = contexto de trabajo cambiable (multi-tenant). Segmento =
> atributo permanente del user."*

Esa frase es **correcta semánticamente** pero **insuficiente
en su conclusión**. Concluía con:

> *"Pregunta abierta: ¿IACT v5.6.0 soporta múltiples convenios
> por user con switching dinámico?"*

**Respuesta canónica (resuelta en este análisis):** NO, v5.6.0
no soporta switching dinámico. BR-012 fija 1 segmento per
user. La pregunta queda **cerrada**, no abierta.

## Sección 6 — Resumen ejecutivo

| Pregunta del ejecutor | Respuesta |
|---|---|
| ¿`segment_id` está fuera de scope? | **NO**, está in-scope per BR-012 (Aprobado, Alta criticidad) |
| ¿Cuál es nuestro `ID_CONVENIO`? | **No tenemos uno**. v5.6.0 NO modela multi-tenant dinámico (decisión deliberada). |
| ¿Cómo manejamos el menú? | Frontend filtra `ALL_NAV_LINKS` (constante React) por capabilities del user obtenidas via endpoint canónico. Sin tabla de menús en backend, sin SQL function `obtener_menu_usuario`, sin dependencia de segmento. |
| ¿El menú depende del segmento del user? | **NO**. El menú depende solo de capabilities. El segmento filtra **datos** dentro de cada endpoint, no menús. |
| ¿Qué pasa si user no tiene segmento? | Menú aparece igual (capability existe). Al ejecutar reporte, endpoint retorna `400 USER_WITHOUT_SEGMENT`. Defense-in-depth correcta. |
| ¿CNST-032 sigue válido? | **No tal cual está**. Refiere a la SQL function `obtener_menu_usuario` de G2 (temp-holding). v5.6.0 (G3) no la usa. **Reescribir CNST-032** en Phase 7 DESIGN. |

## Refs

- BR-012: :doc:`/requisitos/reglas-negocio/br-012-usuario-segmento-unico`.
- TD-ACC-05 (resuelto): WP ``2026-05-06-10-19-34-corpus-tech-debt-cleanup``.
- STD-013 §"TD-ACC-05" en :doc:`/normativa/estandares/std-013-rest-api-conventions`.
- UC_INC_RPT_01: :doc:`/requisitos/casos-uso/reports/uc-inc-rpt-01/index`.
- UC_PERM_08: :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`.
- CNST-032: :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio` (revisar Phase 7).
- Análisis arqueológico previo:

  - ``cmenu2-legacy-archeology.md``.
  - ``inserta-modulos-menu-sql-analysis.md``.
  - ``index-asp-legacy-render-analysis.md``.

- WPs de scope decisions:

  - ``2026-05-06-09-02-26-rbac-v5-6-0-corpus-alignment``.
  - ``2026-05-06-09-17-55-uc-opr-sup-reserved-open-closed``.
  - ``2026-05-06-10-19-34-corpus-tech-debt-cleanup``.
