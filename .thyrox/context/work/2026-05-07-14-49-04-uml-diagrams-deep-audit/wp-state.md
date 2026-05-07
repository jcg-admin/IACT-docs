```yml
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
created_at: 2026-05-07 14:49:04
current_phase: Phase 1 — DISCOVER
status: Activo (heredado del WP previo)
author: NestorMonroy
flow: rm
methodology_step: rm-validation
size: TBD (depende del audit Phase 1)
target: Auditar profundamente los 92 archivos UML recreados en el WP std-012-prefix-normalization. El WP previo aplicó STD-010 + STD-011 + prefijo canónico pero NO con la profundidad pedida originalmente — fueron procesados en batch por cluster, no archivo-por-archivo con calma. Este WP cubre el debt explícito.
predecessor_wp: 2026-05-07-04-50-49-std-012-prefix-normalization (cerrado con nota de honestidad)
trigger: directiva del ejecutor "1" (aceptar estado actual + abrir WP nuevo) tras admisión honesta de profundidad insuficiente
```

# WP — UML Diagrams Deep Audit

## Trigger

Al final del WP previo `std-012-prefix-normalization`, el
ejecutor pregunto "los 92 archivos que tienen diagramas
uml, los hiciste con detalle y con calma??".

**Respuesta honesta:** NO con la profundidad solicitada.

El WP previo aplicó:

- STD-010 vocabulario canónico ✅
- STD-011 aliases auto-documentados ✅
- Prefijo `diagrama-de-` STD-012 v1.1.0 ✅
- Cross-refs al domain-model (referencias en `.. seealso::`) ✅
- Codenames RBAC v5.6.x ✅

Pero NO con profundidad:

- ❌ NO verificó exhaustivamente que cada clase referenciada
  existe en `source/arquitectura-tecnica/domain-model/`.
- ❌ NO aplicó patrones UML-07 (`<<include>>`/`<<extend>>`/
  generalización) según material de referencia
  `source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/`.
- ❌ NO revisó caso por caso si la clase faltaba en
  domain-model y agregarla.
- ❌ Algunos diagramas son "reformat mejorado" no "rediseño
  desde cero".
- ❌ Procesados en batch por cluster, no archivo-por-archivo.
- ❌ Cluster reports (9 UCs, 26 diagramas) procesado más
  superficialmente al final.

## Output esperado del WP

**Phase 1 DISCOVER:** auditar los 92 archivos clasificándolos
por profundidad real:

- **Profundidad ALTA** — diagrama bien estructurado con
  UML-07 patterns (include/extend explícitos), todas las
  clases referenciadas existen en domain-model, vocabulario
  canónico, aliases STD-011.
- **Profundidad MEDIA** — diagrama OK pero con gaps (alguna
  clase faltante en domain-model, includes/extends podrían
  enriquecerse).
- **Profundidad BAJA** — diagrama legacy reformat sin
  patrones UML-07, con cross-refs sin verificar.

**Phase 5 STRATEGY:** decidir qué hacer con cada categoría:

- ALTA → no tocar.
- MEDIA → audit + complementar (clases faltantes, refs).
- BAJA → recreate desde cero con material UML-07.

**Phase 7 DESIGN/EXECUTE:** aplicar las correcciones.

**Phase 11 TRACK:** verificación + cierre.

## Restricciones

- Phase 1 NO modifica source/ — solo audit.
- Strict build (`-W`) tras cualquier cambio.
- Aplicar reglas:
  - STD-010 (vocabulario abstracto).
  - STD-011 (aliases auto-documentados).
  - STD-012 v1.1.0 (prefijo).
  - CNST-033 (conformidad UML).
  - Material UML-07 (`source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/`).
  - Catálogo RBAC v5.6.x.
- Si una clase no existe en `source/arquitectura-tecnica/domain-model/`
  y se referencia en un diagrama: crear la clase con stub
  mínimo (puede ser borrador con metadata + referencia al
  UC que la consume).

## Ámbito

**In-scope:** los 92 archivos diagrama-de-* recreados en el
WP previo, distribuidos en:

- access (1)
- admin (9)
- alerts (15)
- audit (12)
- logs (19)
- permissions (2)
- pipeline (12)
- reports (26)

**Out-of-scope:**

- caller/operator/supervision (declarados Fuera del scope
  en WP previo).
- diagrama-de-caso-de-uso.rst preexistentes (no recreados
  en WP previo).
- 4 diagrama-de-caso-de-uso.rst que YO creé en WPs
  anteriores (uc-adm-04, uc-adm-05, otros) — esos sí son
  responsabilidad mía pero ya fueron auditados en sus
  respectivos WPs.

## Stopping points

- **SP-01** (humano): aprobar resultado del audit
  (clasificación ALTA/MEDIA/BAJA) antes de Phase 5.
- **SP-02** (humano): aprobar plan de remediación antes
  de Phase 7.
- **SP-03**: strict build EXIT=0 tras cada lote de
  correcciones.
- **SP-04** (humano): aprobar cierre del WP.

## Heredado del WP previo

- G-CU-08 (40 archivos TBD/TODO en
  `2026-05-07-04-08-13-use-case-view-analysis`) — sigue
  pendiente de resolver post-cierre de este WP.
