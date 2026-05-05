```yml
project: IACT-docs
work_package: 2026-05-05-14-30-00-uml07-conformance-deep-analysis
created_at: 2026-05-05 14:30:00
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-05-14-06-10-use-case-view-deep-audit
target: Análisis profundo de TODOS los errores de uml-07 conformance en use-case-view
```

# WP — UML-07 Conformance Deep Analysis

## Trigger

El usuario detecta que pese a los WPs previos
(rewrite + audit + restructure + 83 stubs), las
implementaciones siguen sin **respetar las reglas de
``source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/``**.

Petición explícita: análisis profundo de TODOS los
errores. NO ejecutar fixes hasta tener el inventario
completo.

## Método

1. Extraer reglas literales de los **11 archivos canónicos**
   en ``uml-07-diagramas-casos-uso/``.
2. Auditar las **96 instancias de diagrama** en
   ``use-case-view/`` (13 module-level + 83 per-UC).
3. Catalogar errores con severidad (BLOCKER / MAJOR / MINOR).
4. Producir plan de remediación por capas (no solo fix
   superficial).

## Outputs

- ``analyze/uml-07-rules-extracted.md`` — 12 reglas
  canónicas con cita literal.
- ``analyze/errors-catalog.md`` — 14 errores tipificados.
- ``analyze/per-file-audit.md`` — matriz archivo × regla.
- ``analyze/remediation-plan.md`` — plan ordenado por
  severidad y dependencia.

## Stopping points

- **SP-01**: tras catalogar las 12 reglas (no inventar).
- **SP-02**: tras catalogar todos los errores (no fix
  parcial).
- **SP-03**: validación con el ejecutor antes de aplicar
  cualquier remediation.
