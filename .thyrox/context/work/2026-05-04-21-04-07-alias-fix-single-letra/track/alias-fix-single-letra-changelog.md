```yml
created_at: 2026-05-05 01:23:31
project: THYROX
work_package: 2026-05-04-21-04-07-alias-fix-single-letra
phase: Phase 11 — TRACK
author: NestorMonroy
status: Borrador
```

# Changelog — alias-fix-single-letra

## Added

- `logs/build-2026-05-04T212453.txt` — primera build clean (mató al 34%)
- `logs/build-2026-05-04T225347.txt` — build incremental (80% en corte de sesión)
- `logs/build-2026-05-04T231914.txt` — build incremental post-alias: EXIT:0, 2 warnings
- `logs/build-2026-05-04T232112.txt` — clean build pre-transición-fix: EXIT:0, 168 warnings
- `logs/build-2026-05-04T235014.txt` — clean build post-seealso/uc-adm/cnst fix: EXIT:0, 16 warnings
- `logs/build-2026-05-05T002157.txt` — clean build post-caret fix: EXIT:0, 5 warnings
- `logs/build-2026-05-05T005308.txt` — clean build final: EXIT:0, **0 warnings** ✓

## Changed

### Alias corrections — batch 1 (non-conflicting, 265 replacements, 17 archivos)

Commit `47f6aa4` — aliases SINGLE_LETTER + LETRA_NUMERO corregidos en scope
definido por `discover/scope-analysis.md`:

| Alias | Corrección | Método |
|-------|-----------|--------|
| `A`, `C`, `D`, `E`, `G`, `L`, `P`, `R` | `BC_AUTH`, `BC_CALLS`, `BC_AUDIT`, `BC_ETL`, `BC_LOGS`, `BC_ALERTS`, `BC_REPORTS`, `BC_RBAC` | UML-block scoped (solo dentro de `@startuml...@enduml`) |
| `A1`, `A2` | `INICIAR_SESION`, `CERRAR_SESION` | word-boundary |
| `C01–C05` | `LLAMAR_SISTEMA_IVR`..`RESPONDER_ENCUESTA_CSAT` | word-boundary |
| `L01–L07`, `L1` | `VER_LOGS_SISTEMA`..`CONSULTAR_LOGS` | word-boundary |
| `O01–O10` | `CAMBIAR_ESTADO_AGENTE`..`VER_BUZON_MENSAJES` | word-boundary |
| `P1–P11`, `P08–P09` | `PASO_AUTENTICACION`..`VALIDAR_ANTI_SELF` | word-boundary |
| `R01–R17`, `R1–R5`, `R3A–R3C` | `VER_DASHBOARD_IVR`..`REPORTE_CLIENTES_UNICOS` | word-boundary |
| `S01–S03`, `S1–S3`, `S2A`, `S2B` | `MONITOREAR_LLAMADAS_EN_VIVO`..`VERIFICAR_RESULTADO_ETL` | word-boundary |
| `U1` | `CRUD_USUARIOS` | word-boundary |

### Alias corrections — batch 2 (conflicting per-file, 100 replacements, 6 archivos)

Commit `cfda3d4` — aliases con significado distinto según archivo:

| Alias | mod-auth.rst | mod-audit.rst | mod-permissions.rst | mod-pipeline.rst | mod-users.rst | diagrama-uc-rpt.rst |
|-------|-------------|--------------|--------------------|-----------------|--------------|--------------------|
| A01–A05 | INICIAR_SESION..GESTIONAR_SESIONES | VER_AUDITORIA..REPORTE_COMPLIANCE | — | — | — | — |
| P01–P07 | — | — | ASIGNAR_GRUPO..VERIFICAR_PERMISO_USUARIO | VER_ESTADO_ETL..REINTENTAR_ETL | — | — |
| U01–U04 | — | — | — | — | CREAR_USUARIO..ELIMINAR_USUARIO | VER_DASHBOARD_IVR..EXPORTAR_REPORTE |
| U07–U14 | — | — | — | — | — | PROGRAMAR_REPORTE..REPORTE_CAMPANAS |

### RST warning fixes (168 → 0 warnings)

Commit `42b9bf2`:

- **152 trailing transition markers** (`----` al final de archivo) eliminados
  de archivos en `source/base-cognitiva/`, `source/requisitos/` y
  `source/arquitectura-tecnica/`.
- **5 empty seealso directives** eliminados de domain-model stubs:
  application-log, audit-event, etl-ejecucion, infrastructure-log, system-health.
- **3 unexpected indentation** en uc-adm-01/02/03 `excepciones.rst`:
  líneas de continuación con espacio inicial unidas a la línea anterior.
- **2 list-table column mismatch** en `cnst-033-vocabulario-unificado-rbac.rst`:
  agregada celda vacía como tercera columna en cada fila de datos.
- **1 inline emphasis** en `proceso-definicion-arquitectonica.rst`:
  `CNST-*` → `CNST-\*` (asterisco escapado).
- **5 title level inconsistent** en `std-010` y `std-011`:
  subniveles `^` cambiados a `-` para coincidir con jerarquía establecida.

## Status de promoción a CHANGELOG.md raíz

Pendiente de merge a main. Las entradas relevantes para CHANGELOG.md serán:

```
## Added
- Corrección de 99 aliases SINGLE_LETTER y LETRA_NUMERO en 22 archivos RST
  (265 reemplazos en batch no-conflictivo + 100 reemplazos per-file en batch
  conflictivo). Aliases ahora cumplen SCREAMING_SNAKE_CASE según STD-011.

## Fixed
- 168 warnings pre-existentes de Sphinx RST eliminados: trailing transitions,
  empty directives, indentation issues, list-table column mismatches, title
  hierarchy inconsistencies. Build limpio: 0 warnings, EXIT:0.
```
