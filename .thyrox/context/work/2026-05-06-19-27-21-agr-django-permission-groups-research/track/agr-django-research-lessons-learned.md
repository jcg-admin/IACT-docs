```yml
created_at: 2026-05-06 21:08:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 11 — TRACK/EVALUATE (lessons learned)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Lessons Learned — AGR Django Permission Groups Research

## Contexto

WP de research puro (Q1..Q8) con priorización Tier 1 (oficial) > Tier 2 (paquetes maduros) > Tier 3 (comunidad). Output: `analyze/django-rbac-idiomatic-analysis.md` + `strategy/agr-django-research-solution-strategy.md`.

## Lecciones de proceso

### LP-01 — Estrategia de búsqueda explícita reduce sesgo de respuesta

**Observación:** Definir la estrategia (8 queries planificados, idioma inglés, allowed_domains por Tier) **antes** de empezar las búsquedas eliminó el sesgo de "buscar hasta confirmar lo que pensaba".

**Aplicación:** Para futuros research WPs, escribir el plan de queries en `wp-state.md` antes de ejecutar la primera `WebSearch`. El plan se commitea junto al bootstrap del WP.

### LP-02 — Verbatim quotes preserva auditabilidad

**Observación:** Cada finding en `research/raw/Q{N}-*.md` cita verbatim con URL — facilita auditar el razonamiento y reproducir conclusiones meses después. Sin verbatim, claims se vuelven SPECULATIVE.

**Aplicación:** En cualquier research que vaya a fundamentar gates (Stage 5 STRATEGY), exigir verbatim + source URL en cada hallazgo. Codificar en convenciones del WP de research.

### LP-03 — Investigación interna del corpus debe preceder al research externo

**Observación:** Antes de lanzar WebSearch, debí leer ADR-BACK-001/005/006 + grupos-funciones.rst + catalogo-funciones.rst para entender el estado IACT actual. Hacerlo después generó re-trabajo (algunas queries volvieron datos que ya conocía del corpus).

**Aplicación:** Stage 1 DISCOVER de research WPs incluye **dos pasos**: (a) leer corpus interno relacionado; (b) listar gaps que necesitan research externo. Solo después se ejecuta WebSearch.

### LP-04 — No usar Monitor para WebSearch / Write (R-2.0 directo)

**Observación:** WP-5 no necesitó Monitor en absoluto. WebSearch + WebFetch + Write generan output text directo en chat — no hay proceso largo que observar.

**Aplicación:** Internalizado en R-2.0 actualizada. Research WPs futuros no deberían tocar Monitor a menos que necesiten observar un build de docs largo (>5 min) — caso raro en research.

## Lecciones de contenido

### LC-01 — Django Forum + ticket tracker > Stack Overflow

**Observación:** Para preguntas de "patrón idiomatic", Django Forum (`forum.djangoproject.com`) y el ticket tracker (`code.djangoproject.com`) tuvieron answers más autoritativos que Stack Overflow. SO tiene buenas respuestas para "cómo hacer X" pero no para "por qué Y vs Z".

**Aplicación:** Tier 1 priority orden: docs.djangoproject.com → forum.djangoproject.com → code.djangoproject.com → SO solo si los anteriores no cubren.

### LC-02 — "No idiomatic" ≠ "incorrecto"

**Observación:** El research mostró que el modelo IACT no es Django idiomatic, pero **es defendible** dado el contexto del proyecto. La conclusión "Recomendación A: mantener" no es resignación, es trade-off explícito.

**Aplicación:** El framing "idiomatic vs custom" no debe forzar elegir uno; un ADR formal puede justificar custom con sources oficiales y evidencia de costo/beneficio. Aplicar este framing a futuros debates "¿conviene migrar a X?".

### LC-03 — `auth.Group` tiene una limitación documentada (ticket #29748)

**Observación:** El ticket "Add AUTH_GROUP_MODEL setting" sigue abierto desde 2018. Esto significa que muchos proyectos enfrentan el mismo trade-off — IACT no está en posición exótica.

**Aplicación:** Este hallazgo es citable en cualquier futura discusión sobre el tema. Documentado en ADR-BACK-007 como referencia perenne.

## Lecciones de timing

### LT-01 — Research-only WPs cierran rápido

**Observación:** WP-5 (research-only, 8 queries) tomó ~25 minutos del bootstrap al commit final. Comparado con WPs de execute (3-5 horas), es 10× más rápido por unidad de valor entregado.

**Aplicación:** Cuando se enfrenta una decisión arquitectónica con costo > $0, abrir un research-only WP es **siempre rentable** vs decidir sin evidencia. La inversión es baja, el value de "decisión documentada" es alto.

### LT-02 — STRATEGY artifact post-research debe ser su propio artefacto

**Observación:** El research entrega `analyze/django-rbac-idiomatic-analysis.md` con la recomendación, pero el formal `solution-strategy.md` necesita más estructura: alternativas, justificación, evidencia clasificada, traceability. **Son artefactos distintos**.

**Aplicación:** Phase 5 STRATEGY siempre produce su artefacto formal aunque el análisis ya esté hecho. Este WP no lo hizo originalmente; se corrigió en sesión 2026-05-06 21:00 al aplicar formalmente el thyrox skill.

## Riesgos identificados (no realizados)

- **R-01:** Que el research caiga en blogs sin sustancia técnica → **Mitigado** vía allowed_domains Tier 1.
- **R-02:** Que docs antiguos (Django 2.x) confundan análisis → **Mitigado** revisando fechas y prefiriendo Django 5.x/6.0.
- **R-03:** Que IACT-docs ya tenga ADRs que invaliden el WP → **Verificado**: ADR-BACK-001/005/006 son compatibles, no contradicen.

## Métricas

- Queries ejecutadas: 8 (Q1..Q8).
- Sources Tier 1 capturados: 24+ URLs oficiales.
- Sources Tier 2: 8 URLs (Django Forum, GitHub repos).
- Hallazgos verbatim preservados: 100%.
- Tiempo wall-clock: ~25 minutos (bootstrap → commit final WP-5).
- Decisiones derivadas con evidencia: 3 (Decision 1, 2, 3 en solution-strategy).
- TDs derivadas: 2 (TD-RBAC-01 backend, TD-RBAC-02 wrapper).

## Refs

- WP: `2026-05-06-19-27-21-agr-django-permission-groups-research`.
- Research raw: `research/raw/Q1..Q8.md`.
- Análisis: `analyze/django-rbac-idiomatic-analysis.md`.
- Strategy: `strategy/agr-django-research-solution-strategy.md` (formalización 2026-05-06 21:05).
- ADR derivado: `source/backend/adr-back-007-rbac-custom-vs-auth-group.rst` (WP-6).
- WP de aplicación: `2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr` (A.1 + A.2).
