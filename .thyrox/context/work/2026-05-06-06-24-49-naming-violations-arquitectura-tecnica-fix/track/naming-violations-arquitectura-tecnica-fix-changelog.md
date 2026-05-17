```yml
created_at: 2026-05-06 06:30:00
project: IACT-docs
work_package: 2026-05-06-06-24-49-naming-violations-arquitectura-tecnica-fix
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — Naming Violations Arquitectura-Tecnica Fix

## Resumen

| Metrica | Antes | Despues |
|---|---|---|
| Violaciones STD-008 zona productiva | 2 archivos, 7 clases | **0** |
| Audit script C-07 | NO existia | ✅ creado |
| STD-008 con excepcion explicita | NO | ✅ §3.5.1 + §3.5.2 |
| ADRs revisados | 2 | confirmados como descriptivos del legacy (NO violacion) |

## Added

- `scripts/validate-naming-arquitectura-tecnica.sh` — audit
  C-07 que detecta identificadores en espanol en zonas
  productivas (`source/arquitectura-tecnica/`,
  `source/databases/`) excluyendo zonas pedagogicas declaradas
  en STD-008 §3.5.1.
- `analyze/violations-inventory.md` — pendiente (consolidado en
  wp-state.md para WP pequeño).
- Este changelog.

## Changed

### `source/arquitectura-tecnica/system-view/clases-sistema-iact.rst` v1.0.0 → v2.0.0

Renombrado de clases en espanol a vocabulario canonico del
domain-model:

| Antes (ES) | Despues (canonico) |
|---|---|
| SistemaIACT | AuthorizationGuard |
| ReportingService | BaseReportService |
| DisparadorETL | (eliminado — PipelineExecution ya tiene start()) |
| ReporteLlamadasAbandonadas | AbandonmentReportService |
| ReporteTransferencias | TransferReportService |
| AuditoriaAcceso | AuditEvent + AuditService |
| CancelEjecucionETL | (eliminado — PipelineExecution.cancel()) |
| ReintentoETL | (eliminado — PipelineExecution.retry()) |
| EstadoEnum (IN_PROGRESS, exitoso, fallido) | PipelineState (SCHEDULED, RUNNING, COMPLETED, FAILED, CANCELLED) |

Diagrama reorganizado con stereotype `<<sistema>>` en clases
de servicio + cross-refs `seealso` a domain-model y
design-view/state-pipeline-execution.

### `source/arquitectura-tecnica/domain-model/caller-report-service.rst`

`ClientesReport` → `ClientsReport` (4 ocurrencias). Alinea con
el resto del archivo que ya usa prefijo `Client*` (ClientFilters).

### `source/normativa/estandares/std-008-naming-identificadores.rst` v1.1.0 → v1.2.0

Agregadas dos sub-secciones nuevas en §3.5:

- **§3.5.1 Excepciones — Zonas Pedagogicas**: enumera paths
  donde identifiers en espanol estan permitidos
  (`_metodologia-aplicacion`, `_uml`, `metodologia-*-ucs.rst`,
  ADRs descriptivos del legacy). Convencion sintactica: prefijo
  `_` en algun segmento del path marca contenido didactico.
- **§3.5.2 Zona Productiva — Ingles Obligatorio**: enumera zonas
  donde no hay excepcion (`arquitectura-tecnica/`, `databases/`,
  codigo real). Referencia al audit script C-07 para validacion
  automatizada.

## Verified — NO modificados (legitimos)

- `source/backend/adr-back-003-orm-sql-hybrid-permissions.rst` —
  contiene `class GrupoPermisoAdmin(admin.ModelAdmin):`. Es
  **codigo real del legacy codebase** documentado en ADR. No
  prescriptivo, no violacion (per nueva §3.5.1).
- `source/frontend/adr-front-010-typescript-adopcion-gradual.rst`
  — contiene `export class PermisosClient` referenciando
  `import type { Permiso, Usuario } from "@/types/permisos.types"`.
  Es **codigo real del legacy frontend** TypeScript. No
  prescriptivo, no violacion (per nueva §3.5.1).
- 65 archivos en zonas pedagogicas (58 metodologia + 5 _uml + 2
  normativa metodologia-*) — confirmados legitimos per §3.5.1.

## Removed

- N/A.

## Verified

- Audit C-07 (`scripts/validate-naming-arquitectura-tecnica.sh`):
  PASSED 0 violations.
- Las 2 violaciones reales identificadas en bootstrap fueron
  corregidas.
- Los 2 ADRs revisados son descriptivos del legacy, no
  violaciones (documentado en §3.5.1).

## Status de promocion a CHANGELOG.md raiz

Aplicable al merge a main. STD-008 v1.2.0 es cambio sustantivo
al estandar; documentar en release notes.

## WPs sucesores derivados

1. (opcional) `audit-naming-zonas-pedagogicas-completeness` —
   revision del whitelist de paths pedagogicos (¿estan TODAS
   las zonas didacticas en §3.5.1?).
2. (opcional) Si futuros archivos legacy se migran al sistema
   nuevo, los ejemplos en ADRs descriptivos pueden necesitar
   actualizar (cuando ya no sean codigo "actual").

## Refs

- Trigger: critica del analisis informal del ejecutor revelo
  diagrama EventoAuditoria en zona pedagogica + violaciones
  reales en zona productiva.
- Predecesor de validacion: WP `2026-05-05-21-56-47-functional
  -decomposition-antipattern-audit` (cubrio domain-model pero
  NO system-view).
- Naming canonico de referencia: WP `2026-05-05-20-28-12-use-
  case-view-uml07-standalone-pass`.
