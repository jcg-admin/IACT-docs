```yml
created_at: 2026-05-06 10:36:00
project: IACT-docs
work_package: 2026-05-06-10-19-34-corpus-tech-debt-cleanup
phase: Phase 10 — EXECUTE (B-1..B-11 done)
author: NestorMonroy
status: En progreso
version: 1.0.0
```

# WP Changelog — Corpus Tech-Debt Cleanup

## B-1 — RBAC model contexts (system_admin AGR-010, 4 archivos)

`admin_sistema` (PROHIBIDO per CNST-033) reemplazado por
`system_admin` (AGR-010, ``system_admin_group``) en:

- `fnd-04-trazabilidad.rst:493`
- `fnd-05-jerarquia-4-niveles.rst:326,330`
- `function-group-repo.rst:56`
- `fnd-03-casos-de-uso.rst:750` (UC-073 logs)

## B-2 — Users abstract context (3 archivos)

"Rol admin_sistema" → "grupo system_admin_group (AGR-010)":

- `fr-008-01-validar-usuario-activo.rst:62,92`
- `fr-009-01-obtener-lista-paginada.rst:106`

## B-3 — ETL pipeline contexts (3 archivos)

`admin_sistema` en contexto ETL → `pipeline_admin` (AGR-009);
también `operador_etl` (no canónico) → `system_admin_group`
o eliminado:

- `br-002-etl-batch-nocturno.rst:116,144`
- `br-001-fuente-operacional-inmutable.rst:217`
- `fnd-03:680` (UC-053 ETL)

## B-4 — Audit canonical AGR mapping en fnd-03

§3.4 reescrita con los 12 AGR en orden y nombres v5.6.0 inglés:

- AGR-001 basic_operator_group, AGR-002 report_viewer_group,
  AGR-003 quality_supervisor_group, AGR-004 data_exporter_group,
  AGR-005 alert_manager_group, AGR-006 user_admin_group,
  AGR-007 permission_admin_group, AGR-008 auditor_group,
  AGR-009 pipeline_admin_group, AGR-010 system_admin_group,
  AGR-011 call_center_operator_group (RESERVADO),
  AGR-012 call_center_supervisor_group (RESERVADO).

§3.5 (Mapeo Legacy R00x→AGR) preservada con nota explicando
que sus aliases son v5.2.x. §8.2/8.5/8.6 actualizados con
canonical AGR. §3.6 R-mapping: operador_etl → pipeline_admin.

## B-5 — Fix sistemático admin_seguridad (15 ocurrencias, 9 archivos)

`admin_seguridad` se usaba con AGR-008, pero AGR-008 es
`auditor_group` (auditoría), NO `permission_admin_group`. El
admin de seguridad real es **AGR-007** (`permission_admin_group`).

Archivos:

- `br-003,br-004,br-005,br-006,br-007.rst`
- `rbac/catalogo-funciones.rst` §3.11
- `fr-005-01,fr-005-02.rst` (auth/sesiones)
- `fnd-03-casos-de-uso.rst` (UC_ADM_01 ejemplo, §3.5 nota,
  §UC_ACC_09)

Otros legacy fixes:

- `domain-model/access-group.rst:32` ejemplo "agr_supervisor"
  → "quality_supervisor_group"
- `operational-view/system-administration.rst:39,82`
  "agr_admin" → "system_admin AGR-010"
- `fnd-00:462` "AGR_006 (agr_auditor)" → "AGR-008
  (auditor_group)"

## B-6 — STD-013 REST API Conventions (NUEVO)

Creado `source/normativa/estandares/std-013-rest-api-conventions.rst`
formalizando convenciones canónicas:

- URLs son recursos (sustantivos), no acciones
- Estructura URL base OAS3 (server URL + version + path)
- Naming: plural para colecciones, kebab-case multi-palabra,
  sin acrónimos de dominio (alineado con STD-008)
- HTTP methods (POST/GET/PUT/PATCH/DELETE) expresan acción
- Tabla canónica TD-ACC-01..05: URL anterior → URL canónica
- TD-ACC-05 (segmentos) corregido en B-8

Agregado al index estandares (toctree). Bump v2.0.0 → v2.1.0.

## B-7 — Fix AGR_NN malformed refs

5 refs en `fnd-00-contexto-y-jerarquia.rst` con formato
incorrecto AGR_NNN + aliases inexistentes:

- "AGR_008 (agr_exportador)" → "AGR-004
  (``data_exporter_group``)" — exportar es AGR-004
- "AGR_010 (agr_soporte)" → "AGR-010
  (``system_admin_group``)" — agr_soporte no existe
- "Un usuario AGR_008" en contexto exportar → "AGR-004"

## B-8 — TD-ACC-05 Asignación de segmento resuelto

STD-013 actualizado: NO requiere endpoint separado. Per BR-012
(Usuario Segmento Único), el segmento es atributo del User.
Operación canónica: `PATCH /users/{userId}/` con
`{segment_id}` (mismo endpoint de UC_USR_03).

NO crear `/access/segments/assign` — sería duplicación de
estado y violación de "URLs son recursos, no acciones".

## B-9 — AGR-011/012 marcados como RESERVADOS open-closed

`grupos-funciones.rst` tenía AGR-011 (call_center_operator_group)
y AGR-012 (call_center_supervisor_group) listados como activos.
Ahora marcados consistentemente con MOD_Operator/MOD_Supervision
(out-of-scope v5.6.0):

- §4.1 tabla: AGR-011/012 prefijo "(RESERVADO v5.6.0 —
  open-closed)" + columna propósito anotada.
- §4.2 detalle: headers actualizados + bloque `.. warning::`
  + descripción "(reservadas open-closed)".
- Agregado bloque "CAMBIO v5.6.0" documentando reclasificación.

## B-10 — ARQ_MOD_009 + ARQ_MOD_010 marcados Reservado

`arquitectura-tecnica/modulos/operator/index.rst` y
`supervision/index.rst` tenían `:estado: Vigente` sin marca de
reserva. Ahora:

- `:estado:` Vigente → Reservado
- `:version:` 1.0.0 → 1.1.0
- Banner `.. warning::` declarando out-of-scope v5.6.0,
  cross-link a casos-uso/{operator,supervision}/index y modelo
  RBAC.

## B-11 — RACI conventions AGR-011/012 marcados

`raci-rbac/convenciones.rst:99,102`: AGR-011 y AGR-012 sin marca
de reserva. Ahora prefijo "(RESERVADO v5.6.0 — open-closed)" +
nota "Mapea a MOD_{Operator,Supervision} out-of-scope".

## Verificación final

- Strict build (`-W`) tras cada batch B-1..B-11: EXIT=0.
- Conteo final residual:

```bash
grep -rE "admin_sistema" source/ → 2 (cnst-033 regla + rbac-historia evidencia, ambos intencionales)
grep -rE "operador_etl" source/ → 1 (en mapeo legacy con anotación de renombrado)
grep -rE "admin_seguridad" source/ → 0 (solo cnst-033 + rbac-historia)
grep -rE "AGR_[0-9]" source/ → 0 (formato malformado eliminado)
grep -rE "agr_(exportador|soporte|admin|operador|...)" source/ → 0
```

## Status del WP

- Phase 10 EXECUTE: ✅ B-1..B-11 todos completos.
- Phase 11 TRACK: pendiente cierre del ejecutor (I-011).
- Total: ~30 archivos modificados, 1 archivo nuevo (STD-013),
  11 strict builds OK.
