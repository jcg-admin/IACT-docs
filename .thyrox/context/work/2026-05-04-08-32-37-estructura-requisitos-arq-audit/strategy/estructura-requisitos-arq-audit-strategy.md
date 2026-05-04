```yml
created_at: 2026-05-04 10:54:18
project: IACT-docs
work_package: 2026-05-04-08-32-37-estructura-requisitos-arq-audit
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Aprobado
```

# Strategy — Reestructuración de source/arquitectura-tecnica/

## Marco de decisión

El framework de Rozanski & Woods (documentado en `base-cognitiva/_uml/uml-14-*`)
es el estándar de referencia para evaluar y decidir la estructura de
`arquitectura-tecnica/`. El mapeo de los 7 viewpoints Rozanski a las 6 vistas
del modelo 5+1 IACT define qué contenido es correcto en cada directorio.

## Principios rectores (del Stage 5)

Los principios P-01..P-05 documentados en `base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/concerns-principles-decisions.rst`
se aplican a las decisiones de reestructuración. Adicionalmente:

| ID | Principio de reestructuración |
|----|-------------------------------|
| **R-01** | `arquitectura-tecnica/` contiene únicamente artefactos que describen la arquitectura del sistema: diagramas UML de vistas, especificaciones de módulo y decisiones de diseño. No contiene requisitos ni normativa. |
| **R-02** | Cada directorio de vista 5+1 usa granularidad de módulo o variante de infraestructura, NO granularidad UC-individual. Las vistas son arquitectónicas (nivel sistema/módulo), no documentación funcional per-UC. |
| **R-03** | Los diagramas redundantes (copias idénticas de un template genérico sin información arquitectónica real) se eliminan. Se mantiene un diagrama canónico por módulo/variante. |
| **R-04** | No se mueve ni elimina ningún contenido sin primero crear el destino correcto y actualizar todas las referencias cruzadas. Impacto cero en el build. |
| **R-05** | El contenido tipo BR (reglas de negocio RBAC, SoD, AGRs) y gobernanza (RACI) se mueve a los directorios semánticamente correctos (`requisitos/reglas-negocio/`, `normativa/gobernanza/`). |
| **R-06** | Todo diagrama nuevo o corregido en este WP usa exactamente los nombres canónicos de clases, atributos y métodos del modelo de dominio (`bounded-contexts/`). Identificadores: `user_id` (UUID) no `id` (int); `state` (enum UserState) no `is_active` (bool); estados en inglés (ACTIVE/ACKNOWLEDGED/DISABLED). Las inconsistencias encontradas en archivos existentes se corrigen en el mismo PR. Decisiones documentadas en `strategy/trazabilidad-decisiones.md`. |

## Decisiones estratégicas

### SD-01: Granularidad de las vistas 5+1 → nivel módulo

Todas las vistas actualmente implementadas a nivel UC-individual se
reestructuran al nivel correcto:

| Vista | Estado actual | Objetivo |
|-------|---------------|---------|
| Use Case View | 81 per-UC (boilerplate) + 15 mod-indexed | 13 `mod-*.rst` módulo-indexados en `use-case-view/`; eliminar `uc-module-view/` |
| Process View | 81 per-UC (flujo UC incorrecto) | 5-8 diagramas de concurrencia real (ETL, alertas, JWT); reclasificar actuales |
| Deploy View | 80 per-UC (71 copias idénticas) | 3 diagramas canónicos por variante de infra |
| Design View | 160 per-UC (boilerplate 4 pasos) | 12 diagramas canónicos por módulo |
| Implementation View | 80 per-UC (12 únicos) | 12 `mod-*.rst` por módulo |
| Domain Model | 170 archivos mezclados | `overview.rst` + 8 BC de `bounded-contexts/`; eliminar per-UC |

### SD-02: Domain Model → un archivo por clase

`arquitectura-tecnica/domain-model/` debe tener granularidad de clase, no de
bounded context. La estructura objetivo es:

- `overview.rst` — diagrama global: 25 clases en 7 BCs con sus relaciones
- Un archivo por cada clase canónica del dominio (26 archivos):
  - Auth: `user.rst`, `session.rst`, `internal-mailbox.rst`
  - RBAC: `function.rst`, `function-group.rst`, `access-group.rst`,
    `assignment.rst`, `exceptional-permission.rst`, `separation-rule.rst`
  - Calls: `call.rst`, `campaign.rst`
  - Reports: `report.rst`, `metric.rst`, `export-job.rst`,
    `scheduled-report.rst`, `saved-view.rst`
  - Pipeline ETL: `etl-ejecucion.rst`
  - Alerts: `alert.rst`, `threshold.rst`, `subscription.rst`
  - Audit: `audit-event.rst`
  - Logs: `application-log.rst`, `etl-log.rst`, `infrastructure-log.rst`,
    `system-health.rst`, `technical-metric.rst`

Los archivos `bounded-context-*.rst` de `bounded-contexts/` contienen el
diagrama multi-clase del BC — se usan como **fuente** para extraer las clases
individuales, no se mueven tal cual (no conservan el prefijo "bounded-context").

Los 160 archivos per-UC actuales en `domain-model/` se relocalizan a los UC
specs o se eliminan si ya están duplicados ahí.

### SD-03: RBAC textual → requisitos/reglas-negocio/

Los 10 archivos textuales de `rbac/modelo-rbac-iact/` que contienen BR
(catalogo-funciones, sod, grupos-funciones, mapeo-uc) se mueven a
`requisitos/reglas-negocio/rbac/`. Los de tipo ARCH decision
(implementacion, arquitectura, resumen, permisos-temporales, modelo-datos)
permanecen en `arquitectura-tecnica/rbac/` — son decisiones de diseño.

### SD-04: RACI → normativa/gobernanza/

`arquitectura-tecnica/rbac/raci-rbac-iact/` (7 archivos de tablas RACI)
se mueve a `normativa/gobernanza/raci-rbac/`. Son artefactos de gobernanza,
no arquitectura técnica.

### SD-05: modulos/ ARCH textual — se queda (D-02 confirmado)

Los archivos `responsabilidades.rst`, `componentes.rst`, `dependencias.rst`,
`restricciones.rst` de cada módulo permanecen en `arquitectura-tecnica/modulos/`.
Son especificaciones de módulo necesarias. Los `casos-uso.rst` son redundantes
con `requisitos/casos-uso/` — se eliminan con aviso.

### SD-06: Process View real — crear contenido de concurrencia

Además de reclasificar los 81 diagramas actuales (→ UC spec behavior),
se crean los diagramas reales de concurrencia IACT:
- Pipeline ETL (disparadores, colas, workers, retry)
- Procesamiento paralelo de alertas
- Sincronización de sesiones JWT
- Dashboard de alto volumen (concurrencia de consultas)

## Scope de este WP

**Dentro del scope (tareas T-NNN):**
- Corrección de granularidad de Use Case View (H-14) — PRIORIDAD 1
- Consolidación domain-model + bounded-contexts (H-07, H-09) — PRIORIDAD 2
- Reducción deploy-view a 3 canónicos (H-10) — PRIORIDAD 3
- Reducción design-view a 12 canónicos (H-11) — PRIORIDAD 4
- Reducción implementation-view a 12 canónicos (H-12) — PRIORIDAD 5
- Reclasificación process-view + creación de concurrencia real (H-15) — PRIORIDAD 6
- Movimiento RBAC textual → requisitos/reglas-negocio/ (H-08) — PRIORIDAD 7
- Movimiento RACI → normativa/gobernanza/ (SD-04) — PRIORIDAD 8

**Fuera del scope (diferido):**
- `requisitos/_metodologia-aplicacion/` — separar DIAG de REQ (P-03) — WP futuro
- `bounded-contexts/` narrativo textual — evaluar si mueve a base-cognitiva (P-02 parcial)
- Creación de la Vista Context (ausente en 5+1) — WP futuro separado
- Creación de la Vista Operational (ausente en 5+1) — WP futuro separado

## Secuencia de ejecución

Los hallazgos tienen dependencias. La secuencia correcta es:

```
1. Use Case View: integrar uc-module-view/ → use-case-view/, eliminar uc-module-view/
   (H-14 — alta visibilidad, sin dependencias de otros H)

2. Domain Model: mover bounded-contexts/ → domain-model/, relocar per-UC a UC specs
   (H-07 + H-09 — consolidar antes de mover)

3. Deploy View: crear 3 canónicos, eliminar 77 redundantes
   (H-10 — autónomo, no depende de otros H)

4. Design View: crear 12 canónicos, eliminar 148 redundantes
   (H-11 — autónomo, requiere actualizar índice)

5. Implementation View: crear 12 canónicos, eliminar 68 redundantes
   (H-12 — autónomo, requiere actualizar índice)

6. Process View: reclasificar 81 existentes + crear 4-8 de concurrencia real
   (H-15 — última en vistas porque requiere crear contenido nuevo)

7. RBAC textual → requisitos/reglas-negocio/
   (H-08 — después de que las vistas estén correctas; actualizar 38 refs)

8. RACI → normativa/gobernanza/
   (SD-04 — autónomo, pocas referencias)
```

## Criterio de completación

El WP está completo cuando:
1. `arquitectura-tecnica/` no contiene ninguna copia duplicada de diagramas
2. Todas las vistas 5+1 están en granularidad módulo/variante
3. El build Sphinx compila 0 WARNING / 0 ERROR / 0 CRIT
4. Los hallazgos H-07, H-08, H-09, H-10, H-11, H-12, H-14, H-15 están resueltos
5. Los principios R-01..R-05 son verificables en la estructura resultante
```
