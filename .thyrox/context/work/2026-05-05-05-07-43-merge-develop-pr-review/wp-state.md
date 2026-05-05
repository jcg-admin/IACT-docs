```yml
project: IACT-docs
work_package: 2026-05-05-05-07-43-merge-develop-pr-review
created_at: 2026-05-05 05:07:43
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-validation
predecessor_wp: 2026-05-01-23-20-25-new-ucs-from-uml06
target: Revisar merge feature/solve-problem-docs → develop
```

# WP — Merge Develop PR Review

## Trigger

Se intentó merge de `feature/solve-problem-docs` (227 commits)
hacia `develop`. La rama feature contiene trabajo desde:

- 61 UCs canónicos originales en estructura 12-part
- 18 UCs nuevos derivados del principio UML-06 (OPR/SUP/CLI)
- 4 UCs ADM agregados por el equipo en PR #11
- Refactor masivo: STD_010 (vocabulario stack-agnostic),
  STD_011 (alias PlantUML), domain-model per-class,
  Kruchten 4+1 views, Operational + Context viewpoints
- 168 warnings RST preexistentes resueltos → 0-warning build
- Restructura masiva de diagramas UML (1 archivo por diagrama)
- Refactor RBAC v5.3 → v5.5.0

## PR Checklist GitHub (templated)

Items a validar antes del merge:

| Item | Estado declarado | Validación independiente |
|------|------------------|--------------------------|
| Tested locally (make html succeeds) | ✅ Copilot dice OK | Pendiente verificar |
| RST formatting conventions | ✅ Copilot dice OK | Pendiente verificar |
| Conventional commit messages | ⚠️ Copilot dice no | Pendiente verificar (riesgo) |
| Documentation updated | ✅ Copilot dice OK | Pendiente verificar |
| No breaking changes conf.py/deps | ⚠️ Copilot dice cambios | Pendiente verificar (riesgo) |

## Análisis Copilot — observaciones que requieren validación

### R1 — Conventional commit messages (warning)

Copilot detectó que la mayoría de commits NO siguen
``type(scope): description``. Riesgo: el repo declara este
estilo en `.claude/rules/commit-conventions.md` (Tim Pope
desde ÉPICA 4) — pero el template del PR pide convencionales.
Hay **inconsistencia entre la regla del repo y el template
del PR**. Requiere alineación de ambos antes del merge.

### R2 — Cambios a conf.py y uv.lock

Copilot dice que conf.py fue modificado (extensiones
removidas/reemplazadas + `sphinxcontrib.plantuml` agregada)
y `uv.lock` actualizado. Necesario validar:

- ¿Son cambios documentados en ADR?
- ¿El equipo de develop ya conoce las nuevas dependencias?
- ¿El cambio rompe builds en otras ramas?

## Áreas a revisar (por dominio)

1. **R-build**: verificar `make html` con build limpio en HEAD.
2. **R-warnings**: contar warnings actuales y compararlos
   con el claim de 0-warning build.
3. **R-conf**: diff de `conf.py` y análisis de impacto.
4. **R-deps**: diff de `uv.lock` y `pyproject.toml`.
5. **R-commits**: validar formato de commits vs reglas del
   repo y vs template del PR.
6. **R-rst**: spot-check de overline/underline en archivos
   recién creados/modificados.
7. **R-rbac**: verificar consistencia v5.5.0 (counts, names).
8. **R-ucs**: 83 UCs estructura 12-part canónica.
9. **R-domain-model**: 26 clases en 8 bounded contexts,
   integridad referencial.
10. **R-kruchten**: 4+1 views completos en uc/ vs en
    casos-uso/.
11. **R-stack-agnostic**: spot-check de STD_010 (no Python
    code, no SQL ejecutable, no nombres de framework).
12. **R-aliases**: STD_011 PlantUML aliases legibles.
13. **R-trazabilidad**: BR → BReq → UC → FR cadena
    íntegra.
14. **R-no-breaking**: no destrucción de UCs originales.

## Output esperado

`discover/merge-pr-review-analysis.md` con:

- Hallazgos por área (F-NN), severidad (BLOCKER, MAJOR, MINOR).
- Action plan recomendado (lo que se debe hacer ANTES del
  merge a develop).
- Veredicto: APROBAR / APROBAR-CON-CONDICIONES / BLOQUEAR.
