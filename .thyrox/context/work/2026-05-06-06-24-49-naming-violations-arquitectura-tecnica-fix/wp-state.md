```yml
project: IACT-docs
work_package: 2026-05-06-06-24-49-naming-violations-arquitectura-tecnica-fix
created_at: 2026-05-06 06:24:49
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: pequeno (Stages 1, 3, 10, 11)
parallel_with: 2026-05-06-05-28-57-design-view-buildout (no toca los mismos archivos)
target: Corregir violaciones STD-008 (identifiers en ingles) en arquitectura-tecnica/. Producir audit script C-07 que detecte ES en zona productiva. Actualizar STD-008 con excepcion explicita para zonas pedagogicas.
```

# WP — Naming Violations Arquitectura-Tecnica Fix

## Trigger

Auditoria de naming detecto que mientras 58+5+2 = 65 archivos
con clases en espanol son **legitimos** (zonas pedagogicas:
`requisitos/_metodologia-aplicacion/`, `base-cognitiva/_uml/`,
`normativa/estandares/metodologia-*-ucs.rst`), hay **2
violaciones reales** en zona productiva:

| # | Archivo | Severidad | Clases ES |
|---|---|---|---|
| 1 | `arquitectura-tecnica/system-view/clases-sistema-iact.rst` | ❌ ALTA | DisparadorETL, ReporteLlamadasAbandonadas, ReporteTransferencias, AuditoriaAcceso, CancelEjecucionETL, ReintentoETL |
| 2 | `arquitectura-tecnica/domain-model/caller-report-service.rst` | ⚠ PARCIAL | ClientesReport (modulo caller out-of-scope) |

Adicionalmente:

- 2 ADRs (`backend/adr-back-003`, `frontend/adr-front-010`)
  con clases en espanol — verificar si son ejemplos o canonico.
- Sin audit script automatizable que distinga zonas didacticas
  de productivas.

## Causa raiz documentada

1. No hay separacion visual/convencion formal entre zonas
   didacticas (`_metodologia-aplicacion`, `_uml`) y productivas
   (`arquitectura-tecnica/`).
2. STD-008 dice "identifiers en ingles" pero no enumera
   excepciones para zonas pedagogicas — autor no sabe si su
   archivo aplica.
3. Audit Brown 1998 cubrio `domain-model/` (84/85 OK) pero NO
   cubrio `system-view/` — por eso `clases-sistema-iact.rst`
   paso sin deteccion.
4. Sin check automatizable: la regla "ingles en arquitectura-
   tecnica/" no esta en ningun audit script.

## Objetivo

1. Fix de las 2 violaciones reales en arquitectura-tecnica/.
2. Verificar 2 ADRs y decidir.
3. Extender audit con check C-07 "no Spanish identifiers in
   arquitectura-tecnica/".
4. Actualizar STD-008 con excepcion explicita para zonas
   pedagogicas.

## Scope (in)

- Fix `system-view/clases-sistema-iact.rst` — traducir clases
  a vocabulario canonico del domain-model.
- Decision sobre `domain-model/caller-report-service.rst` —
  eliminar o renombrar.
- Inspeccionar `backend/adr-back-003`, `frontend/adr-front-010`.
- Crear `scripts/validate-naming-arquitectura-tecnica.sh` con
  check C-07 (regex de palabras espanolas comunes en zonas
  productivas).
- Update `source/normativa/estandares/std-008-naming-identifiers.rst`
  (o equivalente) con excepcion para zonas pedagogicas.

## Out of scope

- Refactorizar las 65 lecciones pedagogicas (correctas).
- Cambiar STD-008 fuera del addendum sobre excepciones.
- Modificar codigo Python real.

## Stopping points

- **SP-01** (gate humano): aprobar plan de traduccion para
  `system-view/clases-sistema-iact.rst`.
- **SP-02** (gate tecnico): build strict 0 warnings post-fix.
- **SP-03** (gate humano): aprobar audit script + STD-008 update.

## Plan de traduccion para `system-view/clases-sistema-iact.rst`

| Antes (ES) | Despues (EN canonico) | Justificacion |
|---|---|---|
| DisparadorETL | PipelineTrigger o ETLDispatcher | trigger del pipeline |
| ReporteLlamadasAbandonadas | AbandonmentReport | ya existe en domain-model |
| ReporteTransferencias | TransferReport | ya existe en domain-model |
| AuditoriaAcceso | AccessAudit o AuditEvent | AuditEvent existe |
| CancelEjecucionETL | CancelETLExecution | accion |
| ReintentoETL | RetryETL | accion |

Validar mapeos contra `domain-model/` antes de aplicar.

## Riesgos

| ID | Riesgo | Mitigacion |
|---|---|---|
| R-01 | Conflicto con WP design-view-buildout en build paralelo | Solo tocar archivos no-design-view |
| R-02 | Traducciones inventadas que no existen en domain-model | Validar cada nombre nuevo contra `ls domain-model/` |
| R-03 | Audit C-07 false positives en archivos legitimos | Whitelist explicito de paths pedagogicos |
| R-04 | STD-008 update introduce ambiguedad | Excepcion sintacticamente unica (paths con prefijo `_`) |

## Anatomia

```
2026-05-06-06-24-49-naming-violations-arquitectura-tecnica-fix/
├── wp-state.md
├── analyze/
│   └── violations-inventory.md
├── execute/
│   └── build-logs/
└── track/
    └── naming-violations-arquitectura-tecnica-fix-changelog.md
```
