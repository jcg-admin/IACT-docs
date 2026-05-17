```yml
created_at: 2026-05-04 14:58:37
project: THYROX
work_package: 2026-05-04-14-53-38-uml-arq-coverage-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# DISCOVER — Análisis de cobertura: base-cognitiva/_uml vs arquitectura-tecnica/

## Objetivo

Verificar que `source/arquitectura-tecnica/` implementa **todo** lo prescrito en
`source/base-cognitiva/_uml/` (uml-01..uml-14). Identificar gaps y definir WPs correctivos.

---

## Corpus analizado

### base-cognitiva/_uml — documentos leídos

| Archivo | Artefacto | Hallazgos clave |
|---------|-----------|-----------------|
| `uml-14-uml-vistas-arquitectonicas/vistas-y-viewpoints.rst` | UML_14_VISTAS | 7 viewpoints Rozanski definidos; Context = overarching; Table 3-2: OLTP → Context HIGH |
| `uml-14-uml-vistas-arquitectonicas/concerns-principles-decisions.rst` | UML_14_CONCERNS | P-01..P-05 definidos; traceability chain G→B→T→D; Operational ausente reconocido |
| `uml-14-uml-vistas-arquitectonicas/framework-rozanski.rst` | UML_14_ROZANSKI | Tabla 1: viewpoints × model types × diagramas UML; Operational sin equivalente en IACT |
| `uml-14-uml-vistas-arquitectonicas/perspectivas-arquitectonicas.rst` | UML_14_PERSPECTIVAS | 5 perspectivas cross-cutting (Security, Regulation, Availability, Performance, Evolution); grid perspectiva × vista para IACT |
| `uml-14-uml-vistas-arquitectonicas/contexto-empirico.rst` | UML_14_CONTEXTO | Context = HIGH, Operational = HIGH, Functional = HIGH para IACT; mapeo Rozanski → 5+1 |
| `uml-14-uml-vistas-arquitectonicas/frameworks-comparacion.rst` | UML_14_FRAMEWORKS | Operational sin equivalente en Kruchten, Soni, Clements, Garland |
| `uml-14-uml-vistas-arquitectonicas/proceso-definicion-arquitectonica.rst` | UML_14_PROCESO | Tabla 7-1: Salida = "borrador de vista Context con IVR como actor externo"; proceso iterativo 7 pasos |
| `cuando-usar-cada-diagrama/diagrama-de-componentes.rst` | — | Componentes → arquitectura de software (qué módulos y dependencias) |
| `cuando-usar-cada-diagrama/diagrama-de-casos-de-uso.rst` | — | UC diagrams → requisitos de negocio, punto de vista del usuario |

### arquitectura-tecnica/ — estado actual (PROVEN)

| Directorio | Contenido | Viewpoint Rozanski |
|------------|-----------|-------------------|
| `use-case-view/` | 13 `mod-*.rst` canónicos + index v2.0.0 | Functional ✓ |
| `domain-model/` | index + overview + 26 clases + 8 bc-*.rst | Information ✓ |
| `design-view/` | 12 `mod-*.rst` secuencias por módulo | Development (parcial) ✓ |
| `implementation-view/` | 12 `mod-*.rst` stack 5 capas | Development ✓ |
| `process-view/` | 4 diagramas: ETL, alertas, JWT, dashboard | Concurrency ✓ |
| `deploy-view/` | 3 variantes canónicas | Deployment ✓ |
| `arquitectura-sistema/` | arquitectura-general, dfd-nivel-0-contexto, dfd-nivel-1-subprocesos | Context (parcial — ver G-01) |
| `rbac/` | modelo-rbac-iact/ (arch model) + rbac-funciones-por-modulo.rst | transversal |

---

## Gaps identificados

### G-01 — Context viewpoint: cobertura parcial e incorrecta [ALTA]

**Prescripción (PROVEN):**
- `vistas-y-viewpoints.rst`: Context es el viewpoint "overarching" que "informs the scope and content of all others"
- `contexto-empirico.rst`: Context = HIGH importancia para IACT; "integración con IVR (fuente de datos externa, solo lectura)"
- `proceso-definicion-arquitectonica.rst` Tabla 7-1: Salidas = "borrador de vista Context con IVR como actor externo"
- `framework-rozanski.rst`: Context viewpoint = "describes relationships, dependencies and interactions between the system and its environment: people, systems and external entities"

**Estado actual (PROVEN — observado en `arquitectura-sistema/dfd-nivel-0-contexto.rst`):**
- Existe `dfd-nivel-0-contexto.rst` con un DFD nivel 0
- **Bug detectado**: PlantUML usa aliases `IVR`, `SUP`, `ANA`, `SCH` que NO están definidos en el diagrama; los definidos son `SistemaIVR`, `SupervisorSistema`, `AnalistaReportes`, `DisparadorScheduler` → el diagrama no renderiza
- No existe `context-view/` como viewpoint canónico en la estructura de vistas
- No está referenciado en `vistas-kruchten.rst`
- Falta: mapa de stakeholders completo (AGR_ADMIN, AGR_OPERADOR, AGR_AUDITOR, instituciones), interfaces externas con protocolos, narrativa de contexto

**WP correctivo:** WP-context-view

---

### G-02 — Operational viewpoint: completamente ausente [ALTA]

**Prescripción (PROVEN):**
- `contexto-empirico.rst`: Operational = HIGH importancia para IACT ("Auditoría, monitorización, soporte en producción")
- `frameworks-comparacion.rst`: "El viewpoint Operational de Rozanski no tiene cobertura en el modelo 5+1 actual del proyecto"
- `framework-rozanski.rst` Tabla 1: Operational cubre system installation, administration, configuration, support, migration
- `vistas-y-viewpoints.rst`: "no tiene equivalente en Kruchten 4+1, Soni, Clements ni Garland — es una contribución original de Rozanski & Woods"

**Estado actual (PROVEN):** No existe ningún directorio ni documento que cubra el viewpoint Operational en `arquitectura-tecnica/`.

**WP correctivo:** WP-operational-view

---

### G-03 — Directorio stub vacío `rbac/raci-rbac-iact/` [BAJA]

**Estado actual (PROVEN — `find -type f` = 0 archivos):**
- `arquitectura-tecnica/rbac/raci-rbac-iact/` existe como directorio vacío
- Los archivos RACI fueron movidos correctamente a `normativa/gobernanza/raci-rbac/` (Bloque G)
- El toctree de `rbac/index.rst` ya fue corregido (T-046: usa `seealso` en vez de toctree)
- El directorio vacío es un stub residual de la migración

**WP correctivo:** WP-housekeeping (con G-04, G-05, G-06)

---

### G-04 — Bug PlantUML en `dfd-nivel-0-contexto.rst` [MEDIA]

**Estado actual (PROVEN):**
```plantuml
rectangle "Sistema IVR..." as SistemaIVR  ← definido como SistemaIVR
...
IVR --> IACT : datos IVR raw              ← referencia alias IVR (no definido)
SUP --> IACT : comandos ETL / alertas     ← referencia alias SUP (no definido)
ANA --> IACT : solicitudes de reporte     ← referencia alias ANA (no definido)
SCH --> IACT : disparo ETL automatico     ← referencia alias SCH (no definido)
```
El diagrama no renderiza. Los aliases correctos son `SistemaIVR`, `SupervisorSistema`, `AnalistaReportes`, `DisparadorScheduler`.

**WP correctivo:** WP-housekeeping

---

### G-05 — `vistas-kruchten.rst` título incorrecto [BAJA]

**Estado actual (PROVEN):**
- Title: "Vista de Casos de Uso — Arquitectura Tecnica"
- Pero el archivo es el índice maestro de las 6 vistas 5+1, no solo la UC view
- Artefacto correcto en metadata: `INDEX_AT_VISTAS_KRUCHTEN`

**WP correctivo:** WP-housekeeping

---

### G-06 — Perspectivas arquitectónicas no aplicadas explícitamente [MEDIA]

**Prescripción (PROVEN):**
- `perspectivas-arquitectonicas.rst`: Grid perspectiva × vista para IACT definido (Security/Regulation/Availability/Performance/Evolution)
- "Aplicar solo las perspectivas más relevantes a las vistas"
- "El resultado de aplicar una perspectiva a una vista puede ser: Insights, Mejoras, Artefactos"

**Estado actual (INFERRED):**
- No existen documentos de perspectiva en `arquitectura-tecnica/`
- Las perspectivas están parcialmente embebidas (Security en implementation-view/5-layer stack, Regulation en normativa/)
- No hay un documento que mapee explícitamente perspectiva × vista con análisis de calidad

**Decisión (INFERRED):** Crear un documento consolidado de perspectivas en `arquitectura-tecnica/` que aplique el grid ya definido en `perspectivas-arquitectonicas.rst`. No son vistas separadas — son anotaciones transversales.

**WP correctivo:** WP-perspectivas (prioridad MEDIA — luego de Context y Operational)

---

### No-gaps confirmados (PROVEN)

| Prescripción | Estado |
|---|---|
| Use Case View — granularidad módulo (13 mod-*.rst) | ✓ Implementado (Bloque A) |
| Domain Model — 26 clases canónicas + 8 BC diagrams | ✓ Implementado (Bloque B) |
| Deploy View — 3 variantes (estandar, auth-cache, etl) | ✓ Implementado (Bloque C) |
| Design View — 12 secuencias con STD-011 CamelCase | ✓ Implementado (Bloque D) |
| Implementation View — 12 componentes stack 5 capas | ✓ Implementado (Bloque E) |
| Process View — 4 patrones concurrencia reales | ✓ Implementado (Bloque F) |
| RBAC business specs → requisitos/ (catalogo-funciones, sod, grupos, mapeo-uc) | ✓ Implementado (Bloque G) |
| RACI → normativa/gobernanza/ | ✓ Implementado (Bloque G) |
| Framework Rozanski → framework-rozanski.rst actualizado | ✓ Actualizado (pre-WP) |

---

## WPs correctivos definidos

| WP | Nombre | Prioridad | Scope |
|----|--------|-----------|-------|
| WP-1 | `uml-coverage-context-view` | ALTA | Crear viewpoint Context completo con context-view/ directory, stakeholder map, system boundary, external interfaces; fix DFD PlantUML aliases |
| WP-2 | `uml-coverage-operational-view` | ALTA | Crear viewpoint Operational: instalación, administración, configuración, soporte, migración |
| WP-3 | `uml-coverage-housekeeping` | BAJA | Eliminar `rbac/raci-rbac-iact/` stub, fix título `vistas-kruchten.rst`, add context-view a toctree |
| WP-4 | `uml-coverage-perspectivas` | MEDIA | Crear documento perspectivas arquitectónicas en `arquitectura-tecnica/` con análisis Security/Regulation/Availability/Performance/Evolution × 6 vistas |

**Secuencia recomendada:** WP-1 → WP-3 (housekeeping incluye linking) → WP-2 → WP-4

---

## Notas sobre `arquitectura-tecnica/rbac/`

El directorio **DEBE permanecer** en `arquitectura-tecnica/`. Su contenido es el modelo
ARQUITECTÓNICO del RBAC (filosofia, arquitectura, modelo-datos, implementacion, diagramas
de clases y estados) — distinto de las BUSINESS SPECS (catalogo-funciones, sod, grupos,
mapeo-uc) que sí se movieron a `requisitos/reglas-negocio/rbac/`.

La separación actual es correcta:
- `arquitectura-tecnica/rbac/modelo-rbac-iact/` → CÓMO se implementa el RBAC (arch)
- `requisitos/reglas-negocio/rbac/` → QUÉ funciones/grupos existen (business spec)
- `normativa/gobernanza/raci-rbac/` → QUIÉN es responsable de QUÉ (governance)
