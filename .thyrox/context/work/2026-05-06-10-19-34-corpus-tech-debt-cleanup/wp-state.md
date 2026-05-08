```yml
project: IACT-docs
work_package: 2026-05-06-10-19-34-corpus-tech-debt-cleanup
created_at: 2026-05-06 10:19:34
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano (Stages 1, 3, 10, 11)
target: Eliminar deuda tecnica residual del bump v5.6.0 y reclasificacion AGR. Specificamente: 14 refs restantes a "admin_sistema" (vocabulario PROHIBIDO per CNST-033), 5 refs erroneos a AGR-009 que deben ser AGR-010, ref a "operador_etl" que no existe como AGR canonico. Auditoria full corpus.
predecessor_wp: 2026-05-06-10-03-46-mapeo-uc-completion (cerrado, B-1..B-5)
trigger: directiva del ejecutor "no queremos deuda tecnica, revisa si no hace falta nada que actualizar".
```

# WP — Corpus Tech-Debt Cleanup

## Trigger

Tras WP-3 (mapeo-uc-completion B-1..B-5), el ejecutor pidio
verificar y eliminar deuda tecnica residual en lugar de dejarla
pendiente.

## Hallazgos del DISCOVER

**Inventario de `admin_sistema` (PROHIBIDO per CNST-033):**

14 ocurrencias en 8 archivos. Clasificadas por contexto:

| # | Archivo | Linea | Contexto | Reemplazo correcto |
|---|---|---|---|---|
| 1 | `requisitos/reglas-negocio/br-002-etl-batch-nocturno.rst` | 116 | "Responsable: admin_sistema (AGR-009)" — ETL nocturno | `pipeline_admin` (AGR-009) |
| 2 | `requisitos/reglas-negocio/br-002-etl-batch-nocturno.rst` | 144 | "AGR-009 (admin_sistema), AGR-010 (operador_etl)" | AGR-009 `pipeline_admin`; AGR-010 `system_admin` (operador_etl no existe) |
| 3 | `requisitos/reglas-negocio/br-001-fuente-operacional-inmutable.rst` | 217 | "Notificacion a admin_sistema" — operacional ETL | `pipeline_admin` (AGR-009) |
| 4 | `requisitos/requisitos-funcionales/users/uc-008-baja/fr-008-01.rst` | 62 | "rol admin_sistema" — ultimo admin del sistema | `system_admin` (AGR-010) |
| 5 | `requisitos/requisitos-funcionales/users/uc-008-baja/fr-008-01.rst` | 92 | mismo contexto | `system_admin` (AGR-010) |
| 6 | `requisitos/requisitos-funcionales/users/uc-009-listar/fr-009-01.rst` | 106 | "actor con rol admin_sistema" | `system_admin` (AGR-010) |
| 7 | `base-cognitiva/_fundamentos-conceptuales/fnd-04-trazabilidad.rst` | 493 | "admin_sistema selecciona Gestionar Reglas SoD" — MOD_Admin | `system_admin` (AGR-010) |
| 8 | `base-cognitiva/_fundamentos-conceptuales/fnd-03-casos-de-uso.rst` | 680 | UC-053 ETL "AGR-010 (operador_etl), AGR-009 (admin_sistema)" | AGR-009 `pipeline_admin` (operador_etl no existe — separar de AGR-010) |
| 9 | `base-cognitiva/_fundamentos-conceptuales/fnd-03-casos-de-uso.rst` | 750 | UC-073 "Configurar Retencion de Logs" | `system_admin` (AGR-010) — config sistema |
| 10 | `base-cognitiva/_fundamentos-conceptuales/fnd-05-jerarquia-4-niveles.rst` | 326 | UC_ADM_01 SoD | `system_admin` (AGR-010) |
| 11 | `base-cognitiva/_fundamentos-conceptuales/fnd-05-jerarquia-4-niveles.rst` | 330 | "admin_sistema selecciona Gestionar Reglas SoD" | `system_admin` (AGR-010) |
| 12 | `arquitectura-tecnica/domain-model/function-group-repo.rst` | 56 | "mutable solo por admin_sistema" — modelo RBAC | `system_admin` (AGR-010) |
| 13 | `normativa/restricciones/cnst-033-vocabulario-unificado-rbac.rst` | 186 | Lista `agr_admin_sistema` como PROHIBIDO | NO TOCAR (es la regla que prohibe) |
| 14 | `gestion/evidencia/rbac-historia/.../v5-2-0.rst` | 479 | Documento historico de errores v5.2.0 | NO TOCAR (es archivo de evidencia historica) |

**Bug adicional detectado:** `operador_etl` no existe como grupo
AGR canonico (verificado contra `grupos-funciones.rst` AGR-001..012).
Aparece en br-002:144 y fnd-03:680 — error sistematico que asocia
operador_etl a AGR-010 cuando AGR-010 es `system_admin_group`.

## Plan de batches

| Batch | Zona | Archivos | Effort |
|---|---|---|---|
| **B-1** | RBAC model contexts (system_admin AGR-010): fnd-04, fnd-05, function-group-repo, fnd-03:750 | 4 | ~15 min |
| **B-2** | Users abstract context (fr-008, fr-009) | 2 | ~10 min |
| **B-3** | ETL pipeline contexts (br-001, br-002, fnd-03:680) | 3 | ~15 min |
| **B-4** | Audit final corpus para otros residuos | global | ~15 min |

Total: **~1h** + builds.

## Restricciones

- NO tocar `cnst-033-vocabulario-unificado-rbac.rst:186` — es la regla
  canonica que prohibe `agr_admin_sistema`.
- NO tocar `gestion/evidencia/rbac-historia/...v5-2-0.rst:479` — es
  evidencia historica.
- Strict build (`-W`) tras cada batch.
- Tim Pope commits.

## Stopping points

- **SP-01**: gate humano declarado innecesario por el ejecutor.
- **SP-02** (gate tecnico): build strict 0 warnings.
