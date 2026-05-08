```yml
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
created_at: 2026-05-05 20:28:12
updated_at: 2026-05-05 20:28:12
current_phase: Phase 1 — DISCOVER
author: NestorMonroy
```

# Risk Register — `use-case-view-uml07-standalone-pass`

> Documento vivo. Se actualiza cada vez que cambia el estado de un riesgo
> o cuando se identifica uno nuevo.

## Riesgos identificados (Phase 1 DISCOVER)

| ID | Riesgo | Prob | Impacto | Estado | Mitigación | Owner |
|----|--------|------|---------|--------|------------|-------|
| R-01 | uml-06 base "shallow" del predecesor (extends incompletos) | A | M | Identificado | Releer flujos-alternos.rst + excepciones.rst antes de derivar uml-07 | Claude |
| R-02 | Sistemas como actores con nombre NO canónico vs domain-model (e.g. `LogStore` vs `application-log`) | M | M | Identificado | Tabla mapping uml-06 actor → archivo domain-model en analyze/; verificación en cada diagrama de que actor `<<sistema>>` corresponde a archivo `domain-model/<entity>.rst` | Claude |
| R-03 | 83 archivos × revisión humana = ~1-2h por módulo × 13 = mucho effort downstream | A | A | Aceptado | SP-02 valida pattern con 5 sample antes de propagar; commits checkpoint por módulo permiten review por chunks | NestorMonroy |
| R-04 | Drift de scope (repetir error del predecesor — desviar a casos-uso/) | M | C | Identificado | L-01: re-leer wp-state.md::target en cada Phase; auditoría en cada commit que NO se tocan archivos en casos-uso/ | Claude |
| R-05 | Conflictos con PR #14 sin merge (este WP requiere los 53 nuevos uml-06 como insumo) | B | M | Identificado | Esperar merge de PR #14 a feature/solve-problem-docs antes de bifurcar nueva rama; alternativa: trabajar pre-merge sobre feature/cnst-033-uml-conformance (decisión SP-01) | NestorMonroy |
| R-06 | Build break al actualizar 13 module index para apuntar a 83 archivos nuevos (orden importa) | M | A | Identificado | Generar 83 archivos PRIMERO, después actualizar index files; validar build incremental por módulo | Claude |
| R-07 | Casos-uso/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst (uml-06) cambia durante este WP, descrónizando con el uml-07 generado | B | M | Identificado | Snapshot de uml-06 al inicio de cada UC; verificar consistencia al final | Claude |
| R-08 | sphinxcontrib-plantuml falla en pre-render con sintaxis específica (e.g. extension points multi-línea, notas largas) | B | A | Identificado | Pilot 5 sample UCs en SP-02 cubre los patterns principales; iterar template hasta render limpio | Claude |
| R-09 | Vocabulario CNST-033 incompleto en diagramas (e.g. mezcla `view_pipeline_*` con `view_etl_*` heredado) | B | M | Identificado | Audit script verifica 0 codename functions como ACTORES (R-12); pasan a notas si necesario | Claude |
| R-10 | Module index updates rompen toctrees existentes (warnings `toc.not_included` o `toc.not_readable`) | M | A | Identificado | Update incremental de index file por módulo + build local strict por módulo antes de commit | Claude |
| R-11 | Crear ~18 clases nuevas en domain-model con scope inflado (over-engineering, métodos especulativos) | M | M | Identificado | Solo crear clases REFERENCIADAS por los 83 UCs (no especular); spec mínima por clase: atributos, métodos referenciados, relaciones, BR/CNST relevantes; revisión humana SP por lote | Claude |
| R-12 | Métodos faltantes a clases existentes pueden romper consistencia con código real (si existe) | M | A | Identificado | Documentar cada método agregado con la firma referenciada en el UC + aclaración "spec — verificar contra implementación cuando exista"; NO modificar firmas existentes ya validadas | Claude |
| R-13 | Naming variants legacy (e.g. `AssignmentRepository` → `AssignmentRepo`) inconsistentes en UC specs hereados de predecesores | A | M | Identificado | Audit script en Phase 3 que detecta uso de variants no-canónicos en specs de UCs; corregir en seealso de uml-07 (NO en specs textuales — TD para WP de vocabulary cleanup) | Claude |

## Leyenda

- **Prob**: Alta (A) / Media (M) / Baja (B).
- **Impacto**: Crítico (C) / Alto (A) / Medio (M) / Bajo (B).
- **Estado**: Identificado / En mitigación / Materializado / Cerrado.
- **Owner**: Quien gestiona la mitigación.

## Riesgos cerrados

(Ninguno aún — WP en Phase 1.)

## Riesgos materializados (eventos que ocurrieron)

(Ninguno aún — WP en Phase 1.)

## Notas

- R-04 tiene impacto **Crítico** porque repetir el desvío del predecesor invalida
  el WP. Mitigación L-01 es **no negociable** — re-leer `wp-state.md::target` debe
  ocurrir en cada Phase transition.
- R-08 motiva el SP-02 PILOT con 5 sample UCs antes de propagar. El predecesor no
  hizo PILOT formal y sufrió race condition + sintaxis no detectada hasta build limpio.
- R-11 + R-12 + R-13 son específicos del scope de domain-model completion. Mitigación
  conjunta: dedicar Phase 3 ANALYZE íntegramente a `analyze/domain-model-completion-
  analysis.md` con tabla canónica de gaps detectados; bloquear avance a Phase 5
  STRATEGY hasta que el ejecutor apruebe la lista de adiciones propuestas.
