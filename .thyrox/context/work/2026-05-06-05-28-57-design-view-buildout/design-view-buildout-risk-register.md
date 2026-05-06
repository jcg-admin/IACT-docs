```yml
created_at: 2026-05-06 05:32:00
project: IACT-docs
work_package: 2026-05-06-05-28-57-design-view-buildout
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Risk Register — Design View Buildout

| ID | Riesgo | Probabilidad | Impacto | Mitigacion |
|---|---|---|---|---|
| R-01 | Drift hacia ImplementationView (componentes) o DeployView (nodos) | media | alta | Adherirse a uml-03..09 + 11; NO uml-12 ni uml-13 |
| R-02 | Duplicar clases del domain-model en class-{mod} | alta | media | En cada `class-{mod}.rst` referenciar via `:doc:` y solo mostrar relaciones |
| R-03 | Inconsistencia naming entre seq-* nuevos y armonizados | media | alta | Audit script: validar TODOS los actores `<<sistema>>` existen en domain-model |
| R-04 | 14 seq-* existentes peor tras armonizacion | baja | media | Commit por seq, revisable individualmente |
| R-05 | 40 archivos = 6-7 horas wall-clock | alta | media | T-001..T-040 desglose; pausas humanas SP entre batches |
| R-06 | Falsos positivos PlantUML por sintaxis no estandar | media | alta | Build strict `-W` post cada batch |
| R-07 | Auditor sesgado (mismo que produce los archivos) | alta | media | Audit script independiente del autor; reverso UC→designview pre-cierre |
| R-08 | Cache PlantUML stale tras batch (90+ diagramas nuevos) | alta | media | Correr prerender post EXECUTE antes del strict build final |
