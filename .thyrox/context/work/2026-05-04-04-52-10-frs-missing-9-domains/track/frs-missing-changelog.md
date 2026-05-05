```yml
created_at: 2026-05-04 04:52:10
project: IACT-docs
work_package: 2026-05-04-04-52-10-frs-missing-9-domains
phase: Phase 11 — TRACK
author: NestorMonroy
```

# Changelog — FRs Missing 9 Domains

## Added

- `source/requisitos/requisitos-funcionales/permissions/` — nuevo dominio de FRs
  (T-001..T-012)
- FR-012.01..04 derivados de UC_PERM_01 (Asignar Grupo a Usuario)
- FR-013.01..02 derivados de UC_PERM_02 (Revocar Grupo a Usuario)
- FR-014.01..02 derivados de UC_PERM_03 (Conceder Permiso Excepcional)
- FR-015.01..02 derivados de UC_PERM_04 (Revocar Permiso Excepcional)
- FR-016.01..03 derivados de UC_PERM_05 (Crear/Modificar/Retirar Grupo)
- FR-017.01..02 derivados de UC_PERM_06 (Asignar Funciones a Grupo)
- FR-018.01..02 derivados de UC_PERM_07 (Verificar Permiso Usuario)
- FR-019.01..02 derivados de UC_PERM_08 (Generar Menu Dinamico)
- FR-020.01..02 derivados de UC_PERM_09 (Auditar Acceso write side)
- FR-021.01 derivado de UC_PERM_10 (Consultar Auditoria Permisos)
- 22 archivos FR + 11 index.rst + dominio index.rst en total
- `source/requisitos/requisitos-funcionales/index.rst`: agregado `permissions/index`

## Added (continuación)

- `source/requisitos/requisitos-funcionales/operator/` — dominio operator (T-013..T-014)
  - FR-022.01..FR-031.01 derivados de UC_OPR_01..10
- `source/requisitos/requisitos-funcionales/reports/` — dominio reports (T-015..T-016)
  - FR-032.01..FR-047.01 derivados de UC_RPT_01..17 (excluyendo rpt-05/06)
- `source/requisitos/requisitos-funcionales/alerts/` — dominio alerts (T-017..T-018)
  - FR-050.01..FR-054.01 derivados de UC_ALR_01..05
- `source/requisitos/requisitos-funcionales/audit/` — dominio audit (T-019..T-020)
  - FR-055.01..FR-058.01 derivados de UC_AUD_01..04
- `source/requisitos/requisitos-funcionales/logs/` — dominio logs (T-021..T-022)
  - FR-059.01..FR-065.01 derivados de UC_LOG_01..07
- `source/requisitos/requisitos-funcionales/caller/` — dominio caller (T-023..T-024)
  - FR-066.01..FR-070.01 derivados de UC_CLI_01..05
- `source/requisitos/requisitos-funcionales/pipeline/` — dominio pipeline (T-025..T-026)
  - FR-071.01..FR-074.01 derivados de UC_PIP_01..04
- `source/requisitos/requisitos-funcionales/supervision/` — dominio supervision (T-027..T-028)
  - FR-075.01..FR-077.01 derivados de UC_SUP_01..03
- `source/requisitos/requisitos-funcionales/index.rst`: agregados 6 dominios nuevos
  (alerts, audit, logs, caller, pipeline, supervision) — T-029

## Status de promoción a CHANGELOG.md raíz

Pendiente — WP en curso (falta verificación trazabilidad T-030 y commit final T-031).
