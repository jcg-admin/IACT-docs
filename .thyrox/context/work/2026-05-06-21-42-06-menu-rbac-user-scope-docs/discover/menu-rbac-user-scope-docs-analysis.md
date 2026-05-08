```yml
created_at: 2026-05-06 21:48:00
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Borrador
```

# DISCOVER — Menu RBAC User Scope (qué se espera + hallazgos temp-holding)

## Propósito

Análisis de qué se debe documentar en IACT-docs para soportar el WP frontend ``menu-rbac-user-scope``, incorporando:

- Lo que ya existe en el corpus IACT-docs (vigente).
- Lo que existe en ``temp-holding/`` (artefactos pre-corpus, no migrados).
- Gaps detectados.
- Decisiones pendientes.

## Sección 1 — Estado actual en el corpus IACT-docs vigente

### 1.1 UC_PERM_08: Generar Menú Dinámico (Vigente)

`source/requisitos/casos-uso/permissions/uc-perm-08/`:

- 12 partes completas (anatomía estándar).
- Ya documenta concepto general "estructura jerárquica del menu basada en effective_set del User".
- Función RBAC implícita: ``view_own_navigation``.
- Categoría: UX support / personalization.
- Criticidad: Importante (UX) — NO crítica (seguridad real está en UC_PERM_07 enforcement de endpoints).

### 1.2 CNST-032: Menu Dinámico Obligatorio (Vigente)

`source/normativa/restricciones/cnst-032-menu-dinamico-obligatorio.rst`:

- Tipo: Técnica · Criticidad: Crítico · Negociable: No.
- Enunciado verbatim:

   *"El frontend del sistema IACT DEBE invocar la función SQL nativa
   ``obtener_menu_usuario(user_id)`` para construir la estructura de
   navegación del usuario en cada inicio de sesión y al cambiar
   permisos. Está prohibido renderizar menu estático, hardcoded o
   calculado en frontend basado en roles enumerados."*

### 1.3 Patrón documentado en UC_PERM_08 §10 (patrones de diseño)

Verbatim:

> *"Regla: TODO endpoint debe verificar permiso via UC_PERM_07. El
> menu **complementa** la UX (oculta lo no autorizado) pero NO es la
> barrera. Si pasa el menu pero no esta protegido en endpoint → bug
> critico de seguridad."*

## Sección 2 — Hallazgos en `temp-holding/` (pre-corpus)

`temp-holding/` es zona de artefactos legacy no migrados al corpus. Encontré contenido relevante para menú-RBAC en 4 archivos clave:

### 2.1 `FASE 01/docs/backend/UC-PERM-008_generar_menu_dinamico.md`

Documento backend pre-corpus con detalle técnico que NO está en la versión vigente del UC_PERM_08:

**Algoritmo declarado (verbatim):**

```
1. Obtener todas las capacidades del usuario (grupos + excepcionales)
2. Para cada capacidad con formato "dominio.subdominio.funcion.accion":
   - Agrupar por dominio → subdominio → funcion → [acciones]
3. Construir estructura jerárquica tipo árbol
4. Retornar JSON con estructura navegable
```

**SQL function declarada (verbatim):**

```sql
CREATE OR REPLACE FUNCTION obtener_menu_usuario(
    p_usuario_id INTEGER
) RETURNS JSONB AS $$
DECLARE
    v_menu JSONB;
BEGIN
    SELECT jsonb_object_agg(dominio, funciones) INTO v_menu
    FROM (
        SELECT
            split_part(capacidad_codigo, '.', 2) AS dominio,
            jsonb_object_agg(
                split_part(capacidad_codigo, '.', 3),
                array_agg(split_part(capacidad_codigo, '.', 4))
            ) AS funciones
        FROM vista_capacidades_usuario
        WHERE usuario_id = p_usuario_id
        GROUP BY dominio
    ) AS menu_data;
    RETURN COALESCE(v_menu, '{}'::jsonb);
END;
$$ LANGUAGE plpgsql STABLE;
```

**API endpoint canónico (verbatim):**

```
GET /api/permisos/verificar/{usuario_id}/menu/
Authorization: Bearer <token>

Response: 200 OK
{
  "vistas": {
    "dashboards": ["ver", "editar"],
    "reportes": ["ver", "crear", "exportar"],
    "calidad": ["ver", "evaluar"]
  },
  "administracion": {
    "usuarios": ["ver", "crear", "editar"],
    "grupos": ["ver", "crear"]
  }
}
```

### 2.2 Diagrama PUML completo (`temp-holding/.../UC-PERM-008_menu_dinamico_seq.puml`)

Diagrama de secuencia con **6 fases** documentadas:

| Fase | Descripción |
|------|-------------|
| 1 | First load (cache MISS) → SQL function → DB |
| 2 | Cache write + HTTP 200 |
| 3 | Renderizado React (parseo JSON, construcción navbar) |
| 4 | User navigation (action-level visibility — botones ocultos por capability) |
| 5 | Cache HIT en navegación posterior |
| 6 | Invalidación por cambio de permisos (admin asigna grupo → cache DEL) |

**Métricas de performance declaradas (verbatim):**

```
┌────────────────────────┬──────────┐
│ Escenario              │ Latencia │
├────────────────────────┼──────────┤
│ Cache HIT              │ < 5ms    │
│ Cache MISS (SQL func)  │ 20-40ms  │
│ Renderizado React      │ 10-20ms  │
│ Total (cache HIT)      │ < 30ms   │
│ Total (cache MISS)     │ 40-80ms  │
└────────────────────────┴──────────┘
```

**Cache TTL:** 5 minutos (300s) declarado en el diagrama.

**Estructura capacidad declarada en temp-holding:**

```
sistema . vistas . dashboards . ver
└──┬──┘ └──┬──┘ └────┬────┘ └─┬┘
dominio  sub      función   acción
```

### 2.3 `FASE 01/docs/gobernanza/sesiones/.../GAP_ANALYSIS_SISTEMA_PERMISOS.md`

Documenta el set completo de endpoints permisos:

```
GET /api/permisos/verificar/:id/capacidades/
GET /api/permisos/verificar/:id/tiene-permiso/?capacidad=X
GET /api/permisos/verificar/:id/menu/
GET /api/permisos/verificar/:id/grupos/
```

Y la sección "4. Menú Dinámico" verbatim:

> *"Endpoint: GET /api/permisos/verificar/:id/menu/ — Construcción automática de navbar."*

### 2.4 `FASE 01/docs/backend/diseno/arquitectura/permisos_granular.md`

Documenta el modelo de datos backend pre-corpus:

- Modelo ``Funcion`` con campos ``icono: str`` y ``orden_menu: int`` para UI.
- M2M con ``Capacidad`` via ``FuncionCapacidad``.
- Vistas SQL: ``vista_capacidades_usuario``, ``vista_grupos_usuario``.
- Funciones SQL: ``usuario_tiene_permiso()``, ``obtener_menu()``, etc.

## Sección 3 — Gap analysis: corpus actual vs temp-holding vs frontend

| Tema | Corpus IACT-docs (vigente) | temp-holding (pre-corpus) | Frontend WP | Gap |
|------|---------------------------|--------------------------|-------------|-----|
| UC declarado | UC_PERM_08 12 partes | UC-PERM-008 detalle técnico | Implementa filtrado | Ninguno (UC existe) |
| SQL function `obtener_menu_usuario` | CNST-032 menciona obligatorio | Implementación verbatim | NO usa SQL — usa codenames | **GAP: el frontend NO invoca la SQL function como lo manda CNST-032** |
| Formato capacidad | v5.6.0 codenames 1-nivel (``view_reports``) | 4-niveles (``dominio.sub.fn.accion``) | 1-nivel (consistente con v5.6.0) | **GAP CRÍTICO: temp-holding y frontend usan formatos distintos; el corpus actual decidió 1-nivel pero CNST-032 referencia el formato 4-niveles legacy** |
| Endpoint `/api/permisos/verificar/{id}/menu/` | UC_PERM_08 lo menciona | Verbatim implementado | NO documentado en frontend WP | **GAP: el frontend no usa este endpoint** |
| Endpoint `/api/permisos/verificar/{id}/capacidades/` | NO documentado en corpus | Mencionado en GAP_ANALYSIS | Frontend lo mockea (SP-01) | **GAP: endpoint canónico no documentado en IACT-docs vigente** |
| Cache TTL 5 min | NO documentado | Verbatim 300s + invalidación | NO mencionado | **GAP: estrategia de cache no documentada** |
| Performance targets | NO documentado | <30ms HIT / 40-80ms MISS | NO mencionado | **GAP: NFR de menu no especificado** |
| Action-level visibility (Fase 4 del PUML) | NO documentado explícito | Verbatim ("botón Eliminar OCULTO") | UI design out-of-scope | **GAP: política de action-level no documentada** |
| Sub-menús | NO documentado | Implícito en jerarquía 4-niveles | OUT-OF-SCOPE explícito | OK (consistente con scope frontend) |

## Sección 4 — Decisión arquitectónica pendiente: formato capacidad

El gap más crítico es **el formato de capability**:

- **temp-holding (legacy):** ``dominio.subdominio.funcion.accion`` (4 niveles, parseable por SQL ``split_part``).
- **IACT-docs vigente v5.6.0:** ``snake_case_codename`` 1-nivel (``view_reports``, ``export_csv``).

Esto tiene 2 lecturas:

### Lectura A — temp-holding está obsoleta

El formato 4-niveles fue v4.0/v5.0 legacy. v5.2.1 → v5.6.0 cambió a codenames 1-nivel snake_case (per Q6 del WP-5 research). CNST-032 cita la SQL function legacy pero la SQL real debe migrarse al nuevo formato. **Decisión:** actualizar CNST-032 + UC_PERM_08 para reflejar el formato actual.

### Lectura B — el formato 4-niveles sigue siendo el contrato del menú

Los codenames 1-nivel del catálogo se **mapean** a 4-niveles para construir el menú jerárquico. Ej:

```
view_reports          → vistas.reportes.ver
export_csv            → vistas.reportes.exportar
manage_function_catalog → administracion.catalogo.gestionar
```

El mapping vive en una metadata adicional de cada ``Function`` (``module``, ``submodule``, ``action`` columns). **Decisión:** documentar el mapping explícitamente como parte de la spec del menú.

**Recomendación de este análisis: Lectura B.** Razones:

- El menú **necesita estructura jerárquica** para UX coherente — un sidebar plano de 64 ítems es inusable.
- Los codenames v5.6.0 ya tienen el ``module`` (AUTH, USR, ACC, RPT, ALR, AUD, LOG, ADM) que cubre el primer nivel.
- El verbo del codename (``view_``, ``create_``, ``export_``) cubre la "acción".
- El sustantivo (``reports``, ``users``, ``audit_log``) cubre el "subdomain/función".
- Esto significa que **la jerarquía es derivable del codename sin metadata extra**, evitando deuda técnica de "tabla de mapping menu".

## Sección 5 — Stakeholders

| Stakeholder | Rol | Interés |
|---|---|---|
| Frontend dev team | Implementación React | Spec clara de endpoint y formato |
| Backend dev team | Implementación SQL/Django | Spec de function obtener_menu_usuario actualizada |
| Operadores finales | Usuarios | Sidebar coherente + sin opciones inaccesibles |
| Equipo seguridad | Auditoría | Garantía de que menu NO es la barrera (defense-in-depth) |
| Arquitecto | Gobernanza | Coherencia con CNST-032 + ADR-BACK-007 |

## Sección 6 — Requisitos esperados (a documentar en Phase 7)

### 6.1 Funcionales (FR)

- **FR-MENU-01:** Frontend invoca endpoint canónico al login y al cambiar permisos.
- **FR-MENU-02:** Backend retorna estructura jerárquica derivada de codenames del User.
- **FR-MENU-03:** Frontend renderiza únicamente ítems para los que el User tiene capability.
- **FR-MENU-04:** Cache TTL configurable (default 5 min).
- **FR-MENU-05:** Invalidación de cache al asignar/revocar grupo o función excepcional al user (signal post_save).

### 6.2 No funcionales (NFR)

- **NFR-MENU-01:** Cache HIT < 30ms total (objetivo).
- **NFR-MENU-02:** Cache MISS < 80ms total (objetivo).
- **NFR-MENU-03:** Defense-in-depth: menu jamás reemplaza enforcement de endpoints (CNST-032 + UC_PERM_07).
- **NFR-MENU-04:** Idempotencia: 2 requests al endpoint con cache hit retornan exactamente el mismo payload.

### 6.3 Reglas a actualizar/agregar

- **CNST-032:** actualizar para reflejar formato codename v5.6.0 (no formato 4-niveles legacy). El mecanismo (``obtener_menu_usuario`` SQL function) puede mantenerse, pero el parsing debe operar sobre codenames v5.6.0.
- **(Opcional) BR-MENU-01:** "Defense-in-depth" como BR formal — aunque CNST-032 ya lo implica.

## Sección 7 — Riesgos identificados

| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Confundir "menu como UI" con "menu como autorización" | NFR-MENU-03 explícita; tests guardrail (endpoint protegido independientemente del menú) |
| R-02 | El formato 4-niveles legacy de temp-holding genera scope creep si se interpreta como "current spec" | Decisión Lectura B documentada en Phase 5 STRATEGY |
| R-03 | Sub-menús se cuelan al WP frontend a pesar de estar OUT-OF-SCOPE | SP-03 ya respondida; reforzar en Phase 7 design |
| R-04 | Cache stale tras cambio de permisos no invalidado | FR-MENU-05 obligatorio + test de integración |
| R-05 | UC_PERM_08 actual está incompleto vs temp-holding | Phase 7 DESIGN incorpora SQL function + API endpoint + diagrama PUML migrados desde temp-holding |

## Sección 8 — Recomendación de scope (input para Phase 6)

**Scope IN:**

1. Actualizar UC_PERM_08 (12 partes) con detalle técnico que está en temp-holding pero NO en el corpus vigente.
2. Migrar el diagrama PUML de secuencia (6 fases) desde temp-holding al corpus.
3. Crear NFR-MENU-01..04 nuevos (no existen explícitos en NFRs actuales).
4. Bump CNST-032 con clarificación del formato codename v5.6.0 + deprecación del formato 4-niveles legacy.
5. Cross-link UC_PERM_08 + CNST-032 + ADR-BACK-007 + STD-013.

**Scope OUT:**

1. Implementación real (frontend + backend) — está en repos separados.
2. Sub-menús (UX) — WP separado si aplica.
3. Action-level visibility detallada — Phase 9 PILOT si se necesita PoC.
4. Migración de toda `temp-holding/` — solo lo relevante a menú.

## Sección 9 — Próximos pasos

1. **Phase 5 STRATEGY** — formalizar la decisión Lectura A vs B (recomendación: B).
2. **Phase 6 SCOPE** — confirmar la lista de scope IN/OUT con el ejecutor.
3. **Phase 7 DESIGN** — actualizar UC_PERM_08, CNST-032 + crear NFRs.
4. **Phase 10 EXECUTE** — aplicar cambios + strict build.
5. **Phase 11 TRACK** — changelog + lessons learned.
6. **Phase 12 STANDARDIZE** — patterns reutilizables (qué aprender para futuras especificaciones de UI driven by RBAC).

## Refs

- WP frontend (target): ``menu-rbac-user-scope`` (repo separado).
- UC vigente: :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index` (en source/).
- CNST: :doc:`/normativa/restricciones/cnst-032-menu-dinamico-obligatorio` (en source/).
- ADR-BACK-007: :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group` (en source/).
- STD-013 REST API: :doc:`/normativa/estandares/std-013-rest-api-conventions` (en source/).
- temp-holding archivos:

  - ``temp-holding/FASE 01/docs/backend/UC-PERM-008_generar_menu_dinamico.md``
  - ``temp-holding/FASE 01/docs/backend/diseno/detallado/diagramas/casos_de_uso/UC-PERM-008_menu_dinamico_seq.puml``
  - ``temp-holding/FASE 01/docs/gobernanza/sesiones/analisis_nov_2025/GAP_ANALYSIS_SISTEMA_PERMISOS.md``
  - ``temp-holding/FASE 01/docs/backend/diseno/arquitectura/permisos_granular.md``

- WP-5 research: ``2026-05-06-19-27-21-agr-django-permission-groups-research`` (Q1-Q8).
