```yml
project: IACT-docs
work_package: 2026-07-03-22-15-30-auditar-implementacion-ucs-api-ui
created_at: 2026-07-03 22:15:30
updated_at: 2026-07-03 22:15:30
current_phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
```

# Risk Register — auditar-implementacion-ucs-api-ui

| ID | Riesgo | Prob. | Impacto | Mitigación | Estado |
|----|--------|-------|---------|------------|--------|
| R-1 | Falsos gaps por grep ciego (mapping lineal, case, markers compuestos) | Alta | Crítico | Protocolo grep-validated: mapping textual, expansión de compuestos/rangos, inspección de buckets negativos (FG-1..FG-3) | Mitigado — 3 falsos gaps evitados |
| R-2 | Sobre-reclamo por rangos en comentarios (`UC_RPT_01..17` "probaría" RPT_05/06) | Media | Alto | Clasificación evidencia fuerte vs débil; débil exige verificación funcional | Mitigado |
| R-3 | Mapping heredado 2026-05-19 desactualizado para UCs nuevos | Media | Alto | uc-078..090 mapeados por campo `Marker código` declarado en su RST; uc-091 por declaración explícita | Mitigado |
| R-4 | Build Sphinx roto por nuevos RST (refs, toctree) | Media | Medio | Build estricto con log en WP antes de commit | Abierto hasta build |
