```yml
created_at: 2026-04-30 09:06:01
project: IACT-docs
work_package: 2026-04-30-09-06-01-requisitos-update
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Análisis — colocación de docs UML/OOP/casos-uso aplicados a IACT

## Premisa

Durante este WP se generaron 7 documentos derivados de las
"GUÍAS-*" internas (Schmuller Hora 1..6 + Plan + ejemplos
aplicados al dominio). Inicialmente fueron colocados en
`source/gestion/pm/`. El ejecutor cuestionó si esa ubicación
es correcta, pidiendo revisar los `.claude/skills/*` para
mejor orientación.

## Hallazgos

### F-1 — Mismatch PMBOK vs BABOK

Los 7 docs son artefactos **BABOK**, no **PMBOK**.

| Doc | Skill correcto | Por qué |
|-----|----------------|---------|
| `plan-documentacion-uc-con-uml.rst` | `ba-planning` | Es un BA Plan (planificar elicitación + análisis), no un PM Plan |
| `ejemplos-uml-aplicados-iact.rst` | `ba-requirements-analysis` | Modelado de requisitos con UML — descripción literal del skill |
| `ejemplos-oop-aplicados-iact.rst` | `ba-requirements-analysis` | Análisis OOP de UCs |
| `ejemplos-analisis-dominio-aplicados-iact.rst` | `ba-elicitation` + `ba-requirements-analysis` | Sustantivos→clases es elicitación + análisis |
| `ejemplos-relaciones-uml-aplicados-iact.rst` | `ba-requirements-analysis` | Modelado de relaciones |
| `ejemplos-agregacion-interfaces-aplicados-iact.rst` | `ba-requirements-analysis` | Modelado de aggregation/composition/interfaces |
| `ejemplos-casos-uso-aplicados-iact.rst` | `ba-requirements-analysis` | Especificación de UCs |

PMBOK no incluye UML / OOP / casos de uso — son herramientas
BABOK. El descriptor literal de `ba-requirements-analysis`
dice: *"model requirements with use cases and user stories"*.

### F-2 — Naturaleza dual de los docs

Los 7 docs **no son del mismo tipo**:

- **Plan operativo** (1 doc) — qué hacer (13 docs × 97 UCs).
- **Ejemplos aplicados al dominio** (6 docs) — cómo lucen las
  técnicas en IACT (precedente visual + explicación).

Tratarlos como un solo bloque homogéneo es incorrecto.

### F-3 — Cajones existentes en `source/`

| Cajón | Propósito |
|-------|-----------|
| `gestion/pm/` | Project management (PMBOK) |
| `gestion/evidencia/` | Evidencias / archives |
| `normativa/estandares/` | Reglas + metodologías + plantillas |
| `base-cognitiva/_uml/` | Lecciones UML genéricas (Schmuller) |
| `base-cognitiva/_ejemplos-pedagogicos/` | **Sagas end-to-end** del SDLC |
| `base-cognitiva/_taxonomias-y-metamodelos/` | Metamodelos formales |

El cajón `_ejemplos-pedagogicos/` es para **sagas end-to-end de
un feature** (ya tiene `ejemplo-dark-mode`). No es para guías
de aplicación de UNA técnica al dominio. Es otra dimensión.

### F-4 — Cross-links existentes que se rompen

Si se mueven los archivos, hay que actualizar refs en:

- `normativa/estandares/metodologia-oop-para-ucs.rst` →
  apunta a `ejemplos-oop-aplicados-iact`
- `normativa/estandares/metodologia-analisis-dominio-ucs.rst`
  → apunta a `ejemplos-analisis-dominio-aplicados-iact`
- `base-cognitiva/_uml/cuando-usar-cada-diagrama.rst` →
  apunta a `ejemplos-uml-aplicados-iact`
- Plan → apunta a los 6 ejemplos
- Cada ejemplo → apunta al plan + a los demás ejemplos
- `gestion/pm/index.rst` toctree
- `gestion/index.rst` (si se crea `ba/`)

## Tres opciones evaluadas

### Opción 1 — SPLIT por naturaleza (recomendada)

```
gestion/ba/                                  ← NUEVO (paralelo a pm/)
├── index.rst
└── plan-documentacion-uc-con-uml.rst        ← BA Plan operativo

base-cognitiva/_aplicaciones-iact/           ← NUEVO
├── index.rst
├── diagramas-uml.rst
├── orientacion-objetos.rst
├── analisis-dominio.rst
├── relaciones-uml.rst
├── agregacion-interfaces.rst
└── casos-uso-especificacion.rst
```

| Pros | Cons |
|------|------|
| Cada doc en su lugar semánticamente correcto | Plan y ejemplos en cajones distintos |
| `gestion/ba/` cumple el descriptor BABOK exactamente | 2 cajones nuevos |
| Ejemplos = conocimiento cognitivo aplicado, no gestión | Hay que actualizar varios cross-links |
| Nombres simplificados (sin `-aplicados-iact` redundante) | |
| Refleja la realidad: hay BA y PM, son dos prácticas distintas | |

### Opción 2 — TODO en `gestion/ba/`

```
gestion/ba/
├── index.rst
├── plan-documentacion-uc-con-uml.rst
├── ejemplos-uml-aplicados-iact.rst
├── ejemplos-oop-aplicados-iact.rst
├── ejemplos-analisis-dominio-aplicados-iact.rst
├── ejemplos-relaciones-uml-aplicados-iact.rst
├── ejemplos-agregacion-interfaces-aplicados-iact.rst
└── ejemplos-casos-uso-aplicados-iact.rst
```

| Pros | Cons |
|------|------|
| Plan + ejemplos juntos (ejecutor tiene todo a mano) | Mezcla naturalezas: ejemplos no son gestión |
| Un solo cajón nuevo | `gestion/` se llena de material que es realmente cognitivo |
| Cross-links menos invasivos | |

### Opción 3 — TODO en `normativa/estandares/`

```
normativa/estandares/
├── metodologia-oop-para-ucs.rst              (existente)
├── metodologia-analisis-dominio-ucs.rst      (existente)
├── plan-documentacion-uc-con-uml.rst         (movido)
├── ejemplos-uml-aplicados-iact.rst           (movido)
├── ejemplos-oop-aplicados-iact.rst           (movido)
├── ejemplos-analisis-dominio-aplicados-iact.rst (movido)
├── ejemplos-relaciones-uml-aplicados-iact.rst (movido)
├── ejemplos-agregacion-interfaces-aplicados-iact.rst (movido)
└── ejemplos-casos-uso-aplicados-iact.rst     (movido)
```

| Pros | Cons |
|------|------|
| Ejemplos compañeros directos de metodologías | `estandares/` es para reglas normativas, no precedentes ni planes |
| Sin nuevos cajones | Diluye el propósito del cajón |

## Recomendación

**Opción 1 (SPLIT)**:

- Plan → `gestion/ba/` (BA Plan = gestión BABOK, paralelo a PM).
- 6 ejemplos → `base-cognitiva/_aplicaciones-iact/` (aplicaciones
  de técnicas de modelado al dominio).

Razones:

1. Cumple los descriptores literales de los skills disponibles.
2. Respeta el propósito de cada cajón.
3. No mezcla naturalezas distintas en un solo lugar.
4. Permite nombres simplificados en los ejemplos.
5. Crea pareja `pm/` (PMBOK) ↔ `ba/` (BABOK) en gestión.

## Pendiente de aprobación del ejecutor

Confirmación de la opción a aplicar (1 / 2 / 3).

## Trazabilidad

- **Skill aplicada**: `workflow-analyze` (Phase 3 ANALYZE).
- **Origen del análisis**: cuestionamiento del ejecutor sobre
  la colocación inicial en `gestion/pm/`.
- **Skills consultados**: `pm-*` (PMBOK) vs `ba-*` (BABOK) —
  descriptores leídos de `.claude/skills/`.
- **Decisión pendiente**: aplicación de opción 1, 2 o 3.
