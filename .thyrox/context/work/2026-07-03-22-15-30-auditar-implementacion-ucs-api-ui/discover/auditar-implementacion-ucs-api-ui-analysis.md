```yml
created_at: 2026-07-03 22:15:30
project: IACT-docs
analysis_version: 1.0
author: NestorMonroy
status: Aprobado
```

# DISCOVER — Auditar implementación de UCs en api y ui

## Problema

El sponsor pide auditar que los UCs mencionados en docs estén
implementados en IACT-api e IACT-ui, y registrar la auditoría como
nueva iniciativa en IACT-docs. La última auditoría de cobertura
(2026-05-19) cubrió 75 UCs; el corpus actual tiene 88 (se agregaron
uc-078..091 y se retiró uc-047), y el código ganó markers nuevos en
ambos repos. No existía respuesta verificada para el corpus actual.

## Contexto heredado (re-verificado)

- Mapping textual UC↔marker verificado en
  `verificar-mapping-docs-codigo-todos-los-dominios` (2026-05-19):
  users NO lineal, reports con gap RPT_05/06, cross-dominio
  uc-014/uc-020. Reutilizado para uc-001..077.
- uc-078..090 declaran campo `Marker código` en su RST
  (retro-documentados por `documentar-ucs-implementados-no-declarados`).
- uc-091 declara implementación vía APScheduler (sin marker UC_).
- Protocolo obligatorio: `.claude/rules/grep-validated-audit.md`.

## Alcance del WP

Investigación read-only (api, ui) + artefactos de iniciativa en docs.
Tamaño: pequeño (Phases 1, 3, 10, 11 según escalabilidad THYROX).
Sin `flow:` de metodología (investigación directa).

## Stakeholders

- Sponsor/ejecutor: NestorMonroy — decide apertura de iniciativas
  derivadas y cierre del WP.

## Resultado (síntesis)

88 UCs en docs; 18 OUT declarados y consistentes (0 markers);
70/70 in-scope implementados en api y 69/69 aplicables en ui.
0 gaps docs→código. Hallazgos F-01..F-07 (conformidad de markers y
deuda inversa) documentados en la iniciativa
`source/gestion/pm/iniciativas/auditar-implementacion-ucs-api-ui/`.
Evidencia y comandos: `analyze/evidencia/matriz-uc-api-ui.md`.
