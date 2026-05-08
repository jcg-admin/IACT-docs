```yml
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
created_at: 2026-05-06 19:27:21
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeño-mediano (Stages 1, 5, 11 — investigación + recomendación)
target: Validar si el modelo AGR-NNN (12 grupos predefinidos del catalogo IACT) es la forma idiomatica de modelar grupos de permisos en Django + Django REST Framework. Recopilar evidencia de la documentacion oficial Django/DRF y proyectos de referencia. Producir recomendacion con respaldo bibliografico verificable.
predecessor_wp: 2026-05-06-10-19-34-corpus-tech-debt-cleanup (cerrado, B-1..B-11)
trigger: directiva del ejecutor "vamos a revisar si lo que tenemos de AGR-NNN es la forma correcta... Django y DRF son los frameworks del backend, prioridad oficial, busqueda en ingles, guardar todo en el WP".
```

# WP — AGR Django Permission Groups Research

## Trigger

El corpus IACT-docs declara 12 grupos predefinidos (AGR-001..012)
con `is_system=True` (inmutables) en `grupos-funciones.rst`. El
modelo se diseñó conceptualmente sin verificar si Django y DRF
soportan **grupos predefinidos del sistema** como concepto
nativo, o si requiere implementación custom (e.g. data migrations,
fixtures, custom permission backends).

El ejecutor ordena investigar la forma idiomatica en Django/DRF
y respaldar con documentación oficial.

## Pregunta de investigación

> "¿Cuál es la forma idiomática en Django + DRF de modelar
> **grupos de permisos predefinidos del sistema** (system groups,
> inmutables, creados al bootstrap, distintos de grupos custom
> creables por administradores en runtime)?"

## Estado actual del corpus IACT (lo que vamos a validar)

Per `grupos-funciones.rst` y `catalogo-funciones.rst`:

- **Modelo:** `AccessGroup` con campo `is_system: BOOLEAN`
  - `is_system=True` → grupos predefinidos AGR-001..012, inmutables.
  - `is_system=False` → grupos custom (UC_PERM_05).
- **64 funciones activas** asignadas a 9 modulos in-scope + 13
  reservadas (v5.6.0).
- **Asignación:** muchos-a-muchos `function_group_membership`.
- **Reglas SoD:** 3 (SOD-001/002/003) que restringen pares de
  grupos.

Preguntas específicas a validar:

1. ¿Django tiene `auth.Group` nativo o requiere modelo custom?
2. ¿`auth.Permission` cubre el concepto de "función atómica" del
   IACT, o el corpus debe usar un modelo distinto (p. ej.
   `permissions.Permission` custom)?
3. ¿La distinción `is_system` vs custom es un patrón documentado
   o una invención del proyecto?
4. ¿Cómo se bootstrap los grupos predefinidos (data migrations,
   fixtures, signals, management commands)?
5. ¿DRF provee algo encima de auth.Group para APIs REST, o
   reusa `django.contrib.auth`?
6. ¿Hay paquetes oficiales/maduros (p. ej. `django-guardian`,
   `django-rules`) que cambian este panorama?

## Estrategia de búsqueda

**Idioma:** inglés (per directiva del ejecutor — los docs
oficiales son en inglés).

**Priorización de sitios:**

1. **Tier 1 — Oficial:** docs.djangoproject.com, www.django-rest-
   framework.org, github.com/django/django, github.com/encode/
   django-rest-framework.
2. **Tier 2 — Mantenedores establecidos:** django-guardian,
   django-rules, django-permissions, real-python.com (autores
   notables como Vitor Freitas, William Vincent, Adam Johnson).
3. **Tier 3 — Comunitario verificado:** stackoverflow.com con
   respuestas aceptadas y bien votadas, blogs con autoridad
   (testdriven.io, simpleisbetterthancomplex.com).
4. **Excluir o citar con cautela:** medium.com/dev.to artículos
   sin verificación, posts de hace >5 años sin update.

**Queries planeados (búsqueda secuencial, una por temática):**

| # | Query | Foco |
|---|-------|------|
| Q1 | `Django auth Group Permission model documentation` | Nativos: `Group`, `Permission` |
| Q2 | `Django predefined permission groups system groups bootstrap` | System groups inmutables |
| Q3 | `Django data migration create permission groups` | Bootstrap por migración |
| Q4 | `Django REST Framework custom permissions vs auth groups` | Capa DRF |
| Q5 | `Django Group is_system custom group flag pattern` | Patrón is_system específico |
| Q6 | `Django RBAC role-based access control best practices` | Idiomática RBAC |
| Q7 | `Django auth.Permission codename naming convention` | Naming `view_reports`-style |
| Q8 | `django-guardian django-rules object-level permissions comparison` | Paquetes oficiales |

**Para cada query:**

1. `WebSearch` con `allowed_domains` priorizando Tier 1.
2. Si el resultado es valioso, `WebFetch` para extraer detalle.
3. Guardar resultados en `research/raw/Q{N}-{slug}.md` con:
   - Query exacto.
   - URLs visitadas + título.
   - Quotes verbatim (no parafrasear).
   - Clasificación: Tier 1/2/3.

**Output del Stage 5 STRATEGY:**

`analyze/django-rbac-idiomatic-analysis.md` — síntesis con:

- Tabla "Patrón nativo Django ↔ Concepto IACT" (mapping).
- Veredicto: ¿AGR-NNN es idiomático? ¿qué cambiar?
- Recomendaciones con cita verbatim a doc oficial.
- Migration path si requiere refactor.

## Restricciones

- NO modificar el modelo IACT en este WP — solo investigación y
  recomendación.
- NO confundir Django `auth.Group` con DRF permission classes
  (son capas distintas).
- Citar verbatim con URL y fecha de acceso de cada fuente.
- Build strict (sphinx -W) NO requerido para este WP (no toca
  código RST publicado, solo `research/raw/`).

## Riesgos

| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Resultados confusos por terminología (Group vs Role vs Permission Class) | Diccionario terminológico al inicio del análisis |
| R-02 | Docs antiguos (Django 2.x) que ya no apliquen | Filtrar por fecha; preferir Django 4.x/5.x |
| R-03 | Búsqueda devuelve solo blogs sin oficial | Ajustar query; usar `allowed_domains` con docs.djangoproject.com |
| R-04 | El proyecto IACT-docs ya tiene precedentes (ADR-back-001..006) que podrían contradecir o validar | Leer ADRs backend antes de buscar — referencia interna primero |

## Stopping points

- **SP-01** (gate humano): el ejecutor declaro "ya no necesitas el
  gate humano".
- **SP-02** (autovalidación): verificar que cada Q1..Q8 tiene
  archivo en `research/raw/` antes de pasar a análisis.
- **SP-03** (cierre): pendiente del ejecutor o cuando WP cierre
  ciclo.
