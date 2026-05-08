```yml
created_at: 2026-05-06 21:05:00
project: IACT-docs
work_package: 2026-05-06-19-27-21-agr-django-permission-groups-research
phase: Phase 5 — STRATEGY (formalización post-research)
architecture_version: 1.0
architect: NestorMonroy
stack_version: Python 3.11, Django 5.x, Django REST Framework 3.x
validated_by: NestorMonroy + WP-5 research/raw/Q1..Q8
status: Aprobado
```

# Solution Strategy: AGR-NNN RBAC Custom vs Django auth.Group

## Propósito

Formalizar la decisión arquitectónica derivada del research del WP-5 (AGR Django Permission Groups Research). El research entregó hallazgos verbatim con sources oficiales; este artefacto sintetiza las decisiones operativas y traza el plan de implementación.

> Objetivo: Cerrar formalmente la pregunta arquitectónica "¿AccessGroup custom o `auth.Group`?" con evidencia, alternativas evaluadas y plan de aplicación.

---

## Key Ideas

### Idea 1: Mantener modelo custom RBAC con fixes idiomáticos

**Descripción:** Preservar `AccessGroup`, `Function`, `FunctionSeparationRule` como modelos custom independientes de `django.contrib.auth.Group/Permission`, **pero adoptar el patrón canónico Django para bootstrap** (data migration con `RunPython`).

**Impacto:** Ningún refactor masivo del modelo. Reduce setup manual al automatizar el bootstrap. Mantiene compatibilidad con la documentación ya estabilizada (~180 archivos del corpus tocados en sesiones 2026-05-06).

**Justificación:** La pregunta no es "¿es Django idiomatic?" sino "¿qué decisión maximiza valor con costo mínimo dado el estado actual?". Mantener custom + fixes mínimos gana en costo/beneficio sobre refactor mayor.

### Idea 2: Documentar formalmente el porqué — ADR

**Descripción:** Producir un ADR que explique por qué la decisión custom es legítima, qué alternativas se descartaron, y bajo qué circunstancias se reabriría el debate.

**Impacto:** Reduce probabilidad de re-debate futuro. Cualquier desarrollador que cuestione el modelo encuentra respuesta documentada con sources oficiales.

### Idea 3: Bootstrap canónico via data migration

**Descripción:** Reemplazar el management command `manage.py initialize_permissions` (no canónico) como **fuente** del estado inicial — pasa a ser convenience wrapper. La fuente es una data migration con `RunPython`.

**Impacto:** El RBAC se carga automáticamente con `python manage.py migrate` (incluyendo en setup de test database). El equipo no necesita recordar correr el management command tras cada migración.

---

## Fundamental Decisions

### Decision 1: Mantener AccessGroup / Function custom (NO migrar a auth.Group)

**Alternatives Considered:**

- **Alternativa A — Mantener custom + fixes idiomáticos:** preservar modelo, adoptar bootstrap canónico, documentar ADR.
- **Alternativa B — Migrar a `auth.Group` + custom Permission codenames:** alineación máxima con Django, pero requiere refactor masivo del backend Y del corpus IACT-docs.
- **Alternativa C — Wrapper `OneToOneField` (Role → Group):** punto medio que preserva compatibilidad con `django-guardian` y admin nativo.

**Justification:**

- El modelo ya está implementado y documentado en ~80 archivos del corpus (RBAC v5.6.0 estabilizado en sesiones 2026-05-06).
- Migrar a `auth.Group` (B) implica refactor masivo con riesgo de regresión alto, por un beneficio (compatibilidad con `django-guardian`) que no se necesita en el roadmap actual.
- El wrapper (C) introduce dos capas (Role + Group) que complejizan el modelo conceptual sin beneficios visibles dado que IACT no usa `django-guardian` ni admin Group UI extensivamente.
- Django Forum y ticket #29748 documentan que `auth.Group` no es customizable sin workarounds; modelos RBAC más complejos típicamente lo reemplazan.
- El research (Q5) confirma que el patrón "custom Group independiente" es comunidad-documentado aunque no oficial.

**Implications:**

- Pérdida de compatibilidad con tooling tercero que asume `auth.Group` (`django-guardian`). Aceptado: si en el futuro se adopta `django-guardian`, se construye adapter.
- DRF `DjangoModelPermissions` no funciona out-of-the-box: requiere custom permission classes (ya documentadas en ADR-BACK-005).
- Mantener mayor responsabilidad de mantenimiento (lógica que en `auth.Group` viene "free").

### Decision 2: Bootstrap canónico via `RunPython` data migration

**Alternatives Considered:**

- Management command (`python manage.py initialize_permissions`) — no canónico Django, requiere paso manual.
- Fixtures (`loaddata`) — deprecado per docs.djangoproject.com cuando hay migrations.
- Data migration con `RunPython` — patrón canónico oficial.

**Justification:**

Quote verbatim de docs Django (Q2):

> "RunPython is generally the operation you would use to create data migrations, run custom data updates and alterations, and anything else you need access to an ORM and/or Python code for."

> "Since Django 1.7, automatic loading of fixtures is deprecated when applications use migrations, and if you want to load initial data for an app, consider doing it in a migration."

**Implications:**

- El RBAC se bootstrap automáticamente con `migrate`, incluyendo test database setup.
- Idempotente vía `get_or_create`.
- `apps.get_model()` retorna versión histórica del modelo (no la actual) — robusto a refactors futuros.
- Management command `initialize_permissions` se preserva como convenience wrapper, **NO fuente canónica**.

### Decision 3: SoD permanece custom (no hay alternativa nativa)

**Alternatives Considered:**

- `django-rbac` (PyPI) — provee delegation patterns pero no enforcement SoD.
- `django-prbac` (Dimagi) — RBAC parametrizado más complejo.
- Custom `FunctionSeparationRule` (lo que IACT ya hace).

**Justification:**

Django no provee SoD nativo. `FunctionSeparationRule` con 3 reglas declarativas (SOD-001/002/003) está bien fundamentado teóricamente (paper Purdue, NIST RBAC) y resuelve el requerimiento BR-007.

**Implications:**

Mantener el modelo. El backend debe implementar enforcement custom (signal o validation en assignment).

---

## Technology Stack

```
Language & Runtime:     Python 3.11+
Web Framework:          Django 5.x
API Framework:          Django REST Framework 3.x
RBAC modelos:           AccessGroup + Function + FunctionSeparationRule (custom)
Bootstrap RBAC:         Data migration con RunPython (canónico)
Convenience wrapper:    manage.py initialize_permissions (no canónico)
Permission backend:     Custom (delega user.has_perm con codenames de Function)
Object-level perms:     No usado en v5.6.0 (modelo + segment-bound queries cubren scope)
```

**Justification para cada:**

- Python/Django/DRF: ya son el stack del proyecto, no se cambia.
- AccessGroup custom: justificado en Decision 1.
- Data migration: justificado en Decision 2.
- Custom permission backend: documentado en ADR-BACK-005.
- No django-guardian: verificado en Q8 — IACT no requiere object-level permissions.

---

## Architecture Patterns

### Structural Patterns

- **Repository Pattern (acceso a datos):** `AccessGroupRepo`, `FunctionRepo` ya documentados en `arquitectura-tecnica/domain-model/`.
- **Permission Backend (Django built-in extension point):** custom backend que implementa `get_all_permissions()` retornando codes de `Function` vía `AccessGroup`.

### Behavioral Patterns

- **Strategy Pattern:** distintos enforcement paths según tipo de operación (model-level, segment-bound, temporal).
- **Observer / Signal:** SoD enforcement vía `pre_save` signal en `UserFunctionGroupAssignment`.

### Architectural Styles

- **Flat RBAC + SoD layer:** sin herencia de roles (ADR-BACK-001), 12 grupos predefinidos + custom dinámicos, 3 reglas SoD declarativas.

---

## Adherence to Constraints

### Technical Constraint: Django + DRF stack

**How we respect it:** Toda la solución usa exclusivamente Django 5.x + DRF 3.x; no introduce paquetes terceros que cambien el modelo (no `django-guardian`, no `django-rules`).

### Platform Constraint: Custom permission backend ya documentado

**How we respect it:** Decision 1 mantiene compatibilidad con ADR-BACK-005 (middleware/decoradores custom); no requiere cambios en esa capa.

### Organizational Constraint: Corpus IACT-docs estabilizado

**How we respect it:** Decision 1 evita refactor masivo. ~180 archivos del corpus tocados en 2026-05-06 permanecen consistentes.

---

## Traceability to Analysis

### Satisfying Requirements

- **R-1: 12 grupos predefinidos** → AccessGroup custom con `is_system=True` (Decision 1).
- **R-2: SoD entre conjuntos de funciones** → `FunctionSeparationRule` custom (Decision 3).
- **R-3: Bootstrap automatizado** → Data migration con `RunPython` (Decision 2).
- **R-4: Permisos temporales (CNST-031)** → preservado en modelo custom.
- **R-5: Compatibilidad con DRF** → custom permission classes (ADR-BACK-005).

### Satisfying Quality Goals

- **QG-1: Maintainability** → ADR documenta el porqué; reduce probabilidad de re-debate.
- **QG-2: Idiomaticity Django** → Bootstrap canónico via RunPython resuelve el único gap mayor.
- **QG-3: Auditability** → AccessGroup custom permite metadata de audit (`is_system`, código AGR, descripción) que `auth.Group` no soporta nativamente.

### Satisfying Stakeholder Needs

- **Backend developers:** ADR documentado evita cuestionamientos futuros sobre por qué no `auth.Group`.
- **Equipo de seguridad/auditoría:** SoD enforcement formalizado.
- **Operadores:** bootstrap automático con `migrate` (sin paso manual obligatorio).

---

## Plan de Aplicación (mapping a TDs)

| Item | Status | Aplicación |
|---|---|---|
| **A.1** Migrar bootstrap a data migration | ✅ Documentado | `implementacion.rst` §9.5 + ADR-BACK-007 §3.2/§6.1 (WP-6) |
| **A.2** ADR formal | ✅ Creado | `adr-back-007-rbac-custom-vs-auth-group.rst` (WP-6) |
| **A.3** Re-evaluar wrapper OneToOneField | ⏳ Diferido — TD-RBAC-02 | Sólo si se adopta `django-guardian` u otro paquete dependiente de `auth.Group` |
| **A.4** Verificar custom permission backend en código real | ⏳ Out-of-scope IACT-docs — TD-RBAC-01 | Repositorio backend (no IACT-docs) |

---

## Si el WP es un sistema agentic: checklist obligatorio

> No aplica — este WP es de research + decisión arquitectónica documental sobre RBAC, no construye un sistema agentic.

---

## Evidencia de respaldo

| Claim | Tipo | Fuente | Confianza | Origen |
|-------|------|--------|-----------|--------|
| Django provee `auth.Group` y `auth.Permission` nativos con M2M user/groups/permissions | PROVEN | `research/raw/Q1` quote verbatim de [django.contrib.auth docs](https://docs.djangoproject.com/en/6.0/ref/contrib/auth/) | alta | nuevo |
| `RunPython` es el patrón canónico Django para data migrations | PROVEN | `research/raw/Q2` quote verbatim de [Migration Operations docs](https://docs.djangoproject.com/en/5.0/ref/migration-operations/) | alta | nuevo |
| `auth.Group` no es customizable nativamente | PROVEN | `research/raw/Q5` quote verbatim de [Django Forum — Custom Group model](https://forum.djangoproject.com/t/custom-group-model/30070) | alta | nuevo |
| Ticket #29748 (AUTH_GROUP_MODEL) sigue abierto desde 2018 | PROVEN | `research/raw/Q5` cita directa al [ticket](https://code.djangoproject.com/ticket/29748) | alta | nuevo |
| Django no provee SoD nativo; requiere custom o paquete tercero | INFERRED | `research/raw/Q7` — no encontrada implementación nativa en docs; paquetes tercero (django-rbac, django-prbac) ofrecen scaffolding parcial | media | nuevo |
| El corpus IACT-docs ya implementa AccessGroup custom en ~80 archivos | PROVEN | `grep -rn "AccessGroup" source/` ejecutado en sesiones 2026-05-06 | alta | nuevo |
| Refactor a auth.Group implicaría riesgo alto de regresión | INFERRED | Tamaño del corpus (~180 archivos tocados sesión 2026-05-06) + estado estabilizado | media | nuevo |

**Criterios de Confianza:** alta = OBSERVABLE con tool/source citado; media = INFERRED con razonamiento explícito.

**Criterios de Origen:** todos los claims son nuevos (generados en este WP con evidencia directa).

---

## Validation Checklist

- [x] Key ideas clearly articulated (3 ideas)
- [x] Fundamental decisions documented (3 decisiones)
- [x] Alternatives considered for each decision (B y C evaluadas, descartadas con justificación)
- [x] Clear justifications (con quotes verbatim a sources oficiales)
- [x] Technology stack complete (Python/Django/DRF + custom RBAC)
- [x] All patterns explained (Repository, Permission Backend, Strategy, Signal, Flat RBAC + SoD)
- [x] Quality goals addressed (Maintainability, Idiomaticity, Auditability)
- [x] Constraints respected (stack, ADR-BACK-005, corpus estabilizado)
- [x] Traceable to PHASE 1 DISCOVER (`research/raw/Q1..Q8`) y PHASE 3 ANALYZE (`analyze/django-rbac-idiomatic-analysis.md`)
- [x] Clear guidance for PHASE 6 PLAN / PHASE 10 EXECUTE (TDs derivadas)
- [x] Sección "Evidencia de respaldo" con ≥3 claims clasificados (7 claims; 5 PROVEN, 2 INFERRED, 0 SPECULATIVE)

---

## Siguiente Paso

PHASE 6 PLAN no requiere artefacto separado: el plan es **mantener status quo + 2 fixes ya aplicados (A.1 + A.2 en WP-6)**. Las TDs derivadas (TD-RBAC-01 al backend repo, TD-RBAC-02 deferido) tienen owners y criterios de cierre documentados.

PHASE 11 TRACK del WP-5 ya cerrada (`track/agr-django-research-changelog.md`). PHASE 12 STANDARDIZE se documenta en WP-6 (`standardize/patterns.md`) — ver siguiente artefacto.
