```yml
created_at: 2026-05-06 21:10:00
project: IACT-docs
work_package: 2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr
phase: Phase 12 — STANDARDIZE (patterns)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Patterns — RBAC Bootstrap + ADR (reusable patterns extraidos)

## Propósito

Extraer patrones reutilizables del par WP-5 (research) + WP-6 (apply A.1+A.2). Estos patrones aplican a cualquier futura decisión arquitectónica de IACT-docs (o proyectos similares) que necesite:

- Investigación oficial respaldando una decisión.
- Trade-off entre "idiomatic framework" y "custom existente".
- Bootstrap inicial de data del sistema.

---

## Pattern P-01: Research-driven Architectural Decision

**Cuándo aplicar:** Hay una pregunta arquitectónica donde el costo de elegir mal es no-trivial, y la respuesta no es obvia desde el conocimiento del equipo.

**Estructura:**

```
WP-A (research-only):
├── wp-state.md con estrategia de búsqueda explícita
│   ├── Queries planificados (Q1..QN)
│   ├── Priorización por Tier (oficial > paquetes > comunidad)
│   ├── Idioma definido (típicamente inglés para docs oficiales)
│   └── allowed_domains por query
├── research/raw/Q{N}-{slug}.md
│   ├── Query exacto ejecutado
│   ├── URLs capturadas con título
│   ├── Quotes verbatim (NO parafrasear)
│   └── Veredicto preliminar de la query
├── analyze/{wp-name}-analysis.md
│   └── Síntesis comparativa con el estado actual del proyecto
└── strategy/{wp-name}-solution-strategy.md
    ├── Key Ideas
    ├── Fundamental Decisions con alternatives + justification
    ├── Evidencia clasificada (PROVEN/INFERRED/SPECULATIVE)
    └── Plan de aplicación (mapping a TDs)

WP-B (apply):
├── Ejecuta las recomendaciones del WP-A
├── Crea ADR formal con quotes verbatim del WP-A
└── Actualiza docs del proyecto que apliquen
```

**Beneficios:**

- Decisión auditable con evidencia de fuentes oficiales.
- Reduce probabilidad de re-debate (ADR responde al "¿por qué no X?").
- Inversión baja (~25 min por research típico) vs costo de decisión incorrecta.

**Anti-patrón:** decidir basado en "lo que el equipo recuerda haber leído" sin sources verificables. Genera cycles de re-discusión.

---

## Pattern P-02: Custom Model Defendido por ADR

**Cuándo aplicar:** El proyecto usa un modelo custom donde el framework provee algo nativo, y esa decisión no está documentada formalmente.

**Estructura del ADR:**

```
ADR-NNN: {Custom Model} vs {Native Framework Equivalent}

§1 Contexto y Problema
   - Qué provee el framework nativo (con quote verbatim de docs).
   - Qué requiere el proyecto que el nativo no cubre.

§2 Factores de Decisión
   - Idiomática | Compatibilidad tooling tercero | Capacidad extender
   - Costo refactor | Riesgo regresión | Auditabilidad

§3 Decisión
   §3.1 Por qué NO el nativo (con quotes verbatim de issues/forum oficiales)
   §3.2 Patrón canónico que SÍ se adopta (ej: bootstrap via RunPython)

§4 Consecuencias (positivas, negativas aceptadas, neutrales)

§5 Alternativas Consideradas (B, C, ...)
   - Cada alternativa con justificación de descarte
   - Si una alternativa queda como "TD-X" deferred, citarla explícitamente

§6 Implementación
   - Ejemplo de código canónico
   - Cross-link a docs del proyecto que ilustran el patrón

§7 Trazabilidad
   - ADRs relacionados
   - WPs de research que respaldan
   - TDs derivadas

§8 Referencias verbatim oficiales
```

**Aplicado en:** `source/backend/adr-back-007-rbac-custom-vs-auth-group.rst`.

**Beneficio clave:** cualquier futuro contribuyente que cuestione "¿por qué AccessGroup en lugar de auth.Group?" encuentra respuesta en 5 min sin necesidad de re-research.

---

## Pattern P-03: Bootstrap Canónico Django via RunPython data migration

**Cuándo aplicar:** Necesitás cargar datos seed del sistema (grupos predefinidos, configuración inicial, catálogos) en una app Django.

**Patrón canónico:**

```python
# apps/{app}/migrations/00NN_create_default_{thing}.py
from django.db import migrations

PREDEFINED_DATA = [
    # ... constantes del seed
]

def create_default_{thing}(apps, schema_editor):
    Model = apps.get_model('{app}', '{Model}')
    for entry in PREDEFINED_DATA:
        Model.objects.get_or_create(
            unique_field=entry['key'],
            defaults={...},
        )

class Migration(migrations.Migration):
    dependencies = [('{app}', '00NN-1_previous')]
    operations = [
        migrations.RunPython(
            create_default_{thing},
            migrations.RunPython.noop,  # reverse opcional
        ),
    ]
```

**Por qué:**

Quote verbatim de docs.djangoproject.com:

> "RunPython is generally the operation you would use to create data migrations, run custom data updates and alterations."

> "Since Django 1.7, automatic loading of fixtures is deprecated when applications use migrations, and if you want to load initial data for an app, consider doing it in a migration."

**Beneficios:**

- Idempotente (`get_or_create`).
- Se ejecuta automáticamente con `python manage.py migrate`.
- Se carga en setup de test database.
- `apps.get_model()` retorna versión histórica del modelo (robusto a refactors).

**Anti-patrones evitados:**

- Fixtures (`loaddata`) — destructivo, deprecado para apps con migrations.
- Management command como **fuente** del seed — requiere paso manual; OK como convenience wrapper que delegue en la data migration.
- Hardcoded data en `models.py` — viola separation of concerns.

**Aplicado en:** `source/arquitectura-tecnica/rbac/modelo-rbac-iact/implementacion.rst` §9.5.

---

## Pattern P-04: Recommendation A/B/C — Trade-off Framework

**Cuándo aplicar:** Hay 2-3 alternativas viables para una decisión arquitectónica y necesitás justificar cuál elegir.

**Estructura:**

```
Recommendation A — Mantener custom + fixes idiomáticos
  Pros: bajo costo, riesgo bajo, alinea con estado actual
  Contras: pierde compatibilidad con tooling X
  Aplicar: si el proyecto está estabilizado

Recommendation B — Migrar a framework nativo
  Pros: máxima compatibilidad, simplicidad
  Contras: refactor masivo, riesgo regresión alto
  Aplicar: si el proyecto está temprano o el costo de mantenimiento custom es alto

Recommendation C — Hibrido
  Pros: balance, preserva compatibilidad parcial
  Contras: más complejidad conceptual
  Aplicar: si necesitás algunos pero no todos los features de A o B
```

Cada Recommendation se evalúa contra:

| Criterio | A | B | C |
|---|---|---|---|
| Esfuerzo refactor | Bajo | Alto | Medio |
| Compatibilidad tooling tercero | Baja | Alta | Alta |
| Riesgo regresión | Bajo | Alto | Medio |
| Idiomatic con el framework | Bajo | Alto | Medio |

**Decisión final** documentada en ADR + cross-link al WP de research.

**Aplicado en:** `analyze/django-rbac-idiomatic-analysis.md` § "Recomendaciones".

---

## Pattern P-05: Cross-WP Pipeline (Research → Apply)

**Cuándo aplicar:** El WP de research no debería ejecutar las recomendaciones — separar concerns.

**Estructura:**

```
WP-A (Research) → cierra con strategy/ + recomendaciones explícitas
  ↓ (handoff documentado en track/changelog y wp-state.md predecessor)
WP-B (Apply) → bootstrap referencia explícita a WP-A
  ↓ Aplica las recomendaciones priorizadas
  ↓ Marca diferidas como TDs con criterios de cierre
WP-C (Standardize) → patrones extraidos del par WP-A + WP-B (este artefacto)
```

**Beneficios:**

- Research permanece auditable y no se contamina con código de aplicación.
- Apply tiene scope claro: ejecutar lo decidido.
- Standardize permite reusar el aprendizaje en futuros casos similares.

---

## Tabla resumen de patterns

| ID | Nombre | Cuándo aplicar |
|---|---|---|
| P-01 | Research-driven Architectural Decision | Pregunta arquitectónica con costo no-trivial |
| P-02 | Custom Model Defendido por ADR | Modelo custom donde framework provee nativo |
| P-03 | Bootstrap Canónico Django via RunPython | Seed data del sistema en Django app |
| P-04 | Recommendation A/B/C Trade-off Framework | Múltiples alternativas viables |
| P-05 | Cross-WP Pipeline (Research → Apply) | Separar research de aplicación |

---

## Refs

- WP origen del patrón: `2026-05-06-19-27-21-agr-django-permission-groups-research` (P-01, P-04).
- WP origen del patrón: `2026-05-06-20-11-32-rbac-bootstrap-data-migration-adr` (P-02, P-03, P-05).
- ADR aplicado: `source/backend/adr-back-007-rbac-custom-vs-auth-group.rst`.
- Docs Django referenciadas: ver §8 del ADR-BACK-007.
