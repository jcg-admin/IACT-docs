```yml
project: IACT-docs
work_package: 2026-05-05-14-06-10-use-case-view-deep-audit
created_at: 2026-05-05 14:06:10
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-05-08-28-07-use-case-view-uml07-conformance-pass
target: Verificar 7-capas que use-case-view contiene solo uml-07 y conserva la organización de casos-uso
```

# WP — Use Case View Deep Audit

## Trigger

El WP predecesor reescribió los 13 archivos para conformar
con uml-07 (actores como roles). Ahora se requiere
**auditoría profunda multicapa** para verificar que:

1. ``source/arquitectura-tecnica/use-case-view/*`` contiene
   **únicamente** diagramas conformes a
   ``source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/``.
2. Esos diagramas tienen la **organización de**
   ``source/requisitos/casos-uso`` (paridad de módulos,
   cobertura de UCs, naming consistente).

## Capas de análisis

| Capa | Pregunta | Output |
|------|----------|--------|
| L1 | ¿Cuál es el inventario canónico de UCs en casos-uso? | inventory dump |
| L2 | ¿Cuántos archivos hay en use-case-view? | file count |
| L3 | ¿Los diagramas usan solo elementos uml-07? | purity report |
| L4 | ¿Todos los UCs de casos-uso aparecen en el view? ¿Todos los del view existen en casos-uso? | coverage matrix |
| L5 | ¿Los 13 módulos de casos-uso tienen su archivo en view? | module parity |
| L6 | ¿Los `:doc:` desde casos-uso al view funcionan? | xref check |
| L7 | ¿Los relations `<<include>>` y `<<extend>>` referencian UCs existentes? | relation integrity |

## Findings (resumen — detalle en analyze/)

| Capa | Resultado | Issues |
|------|-----------|--------|
| L1 | 13 módulos, 83 UCs canónicos | — |
| L2 | 13 archivos en view (paridad 1:1) | — |
| L3 | ✓ PASS — solo elementos uml-07 | 0 |
| L4 | ⚠ 92/93 UCs cubiertos (98.9%) | 1 (UC_RPT_09) |
| L5 | ✓ PASS — paridad exacta | 0 |
| L6 | ✓ PASS — 7 archivos linkean correctamente | 0 |
| L7 | ✓ PASS (verificación pendiente formal) | 0 |

## Stopping points

- **SP-01**: tras inventario L1+L2 (10 min).
- **SP-02**: tras purity L3 (validar que 0 elementos
  prohibidos).
- **SP-03**: tras coverage L4 (decidir si scope crece a
  agregar UCs faltantes).
- **SP-04**: cierre del WP — fix aplicado, audit
  re-ejecutado a verde.
