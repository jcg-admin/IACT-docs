```yml
project: IACT-docs
work_package: 2026-05-08-00-17-08-use-case-view-sod-vocabulary
created_at: 2026-05-08 00:17:08
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: mediano-grande (~12 archivos, ~60 ediciones, ~2-3 h)
target: **Eliminar TODAS las apariciones de "Sod"/"SOD"/"sod" en cualquier forma controlada por el proyecto** en `source/arquitectura-tecnica/use-case-view/` (Cat-1 plantuml aliases, Cat-2 captions, Cat-3 narrativa, Cat-4 filenames+toctrees+anchors). Directiva del ejecutor (post Phase 1 inicial): "no queremos nada que diga Sod, porque puede confundir". Excepciones inmovibles: tokens opacos backend (`access:*_sod`), "Separation of Duties" en prosa explicativa larga, codigos BD `SOD-001..003`. Alcance ampliado documentado en `discover/rule-and-context.md`.
predecessor_wp: 2026-05-07-23-30-26-use-case-view-users-alignment (cerrado)
trigger: el ejecutor detecto refs `VALIDAR_SOD` en plantuml de use-case-view tras cierre del WP std-010-compliance — confirmacion de que el cleanup previo no cubrio todos los identificadores tecnicos
```

# WP — use-case-view SOD vocabulary cleanup

## Trigger

Tras cerrar 4 WPs (uml-deep-audit, endpoint-sod-rules-rename,
std-010-compliance, users-alignment), el ejecutor detecto que
en `use-case-view/permissions/uc-perm-01-asignar-grupo-a-usuario.rst`
sigue apareciendo:

```
note bottom of VALIDAR_SOD
```

El audit confirma que existen **27 refs** a `VALIDAR_SOD` en
7 archivos, mas eventos `SOD_RULE_*`, codigos `SOD-001..003`
y filenames con "sod" — todos identificadores tecnicos que el
proyecto controla y que NO son tokens opacos del catalogo
RBAC.

## Distincion conceptual (continuidad de WPs previos)

| Tipo | Ejemplo | Decision |
|---|---|---|
| **Token opaco backend RBAC** | `access:view_sod`, `access:update_sod` | **PRESERVAR** (contrato API) |
| **Concepto/dominio "SoD"** | "reglas SoD", "Separation of Duties" | **PRESERVAR** (vocabulario de dominio, como JWT) |
| **PlantUML alias** | `VALIDAR_SOD as VALIDAR_SOD` | **RENOMBRAR** (identificador del proyecto) |
| **Backend event identifier** | `SOD_RULE_CREATED` | **RENOMBRAR** a `SEPARATION_RULE_CREATED` (alineacion A-001) |
| **Filename con "sod"** | `uc-acc-05-gestionar-reglas-sod.rst` | **RENOMBRAR** + actualizar toctrees + cross-refs |

## Scope del WP

### In-scope (renombrar)

**Cat-1: PlantUML aliases (27 refs en 7 archivos):**

- `permissions/uc-perm-01-asignar-grupo-a-usuario.rst` (4 refs).
- `permissions/uc-perm-03-conceder-permiso-excepcional.rst` (3 refs).
- `permissions/uc-perm-06-asignar-funciones-a-grupo.rst` (4 refs).
- `admin/uc-adm-03-gestionar-catalogo-de-agrupadores-del-sistema.rst` (5 refs).
- `access/uc-acc-01-asignar-funciones.rst` (4 refs).
- `access/uc-acc-04-asignar-agrupador.rst` (4 refs).
- `access/uc-acc-08-permiso-temporal.rst` (3 refs).

`VALIDAR_SOD` → `VALIDAR_SEPARATION_RULES` (caption "Validar SoD"
puede preservarse o cambiarse — decision en Phase 5).

**Cat-2: Backend event identifiers (5 refs en 2 archivos):**

- `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst` (3 refs).
- `permissions/uc-perm-10-consultar-auditoria-de-permisos.rst` (1 ref).

`SOD_RULE_*` → `SEPARATION_RULE_*` (alinea con backend A-001).

**Cat-3: Codigos de regla "SOD-001..003":**

- `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst` (1 ref).

Decidir en Phase 5 si son codigos estables del proyecto o
renombrables (probablemente PRESERVAR — son identificadores
de regla en BD).

**Cat-4: Filenames con "sod" (2 archivos + 2 toctrees + 1 cross-ref):**

- `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst`
  → `...-de-reglas-de-separacion.rst`.
- `access/uc-acc-05-gestionar-reglas-sod.rst`
  → `...-gestionar-reglas-de-separacion.rst`.
- Update `admin/index.rst:300` toctree.
- Update `access/index.rst:150` toctree.
- Update anchors `_at_uc_adm_01_gestionar_ciclo_de_vida_de_reglas_sod`
  y `_at_uc_acc_05_gestionar_reglas_sod`.

**Cat-5: Cross-ref `:doc:` a archivo externo:**

- `mapa-funciones-rbac.rst:184` referencia
  `:doc:`/requisitos/reglas-negocio/rbac/sod`` que SI EXISTE
  con ese path. Dos opciones:
  - **Opcion 5a:** preservar la ref (el archivo target conserva
    su nombre actual).
  - **Opcion 5b:** abrir WP separado para renombrar tambien
    el archivo target en reglas-negocio (out-of-scope este WP).

### Out-of-scope (preservar)

1. **Tokens opacos:** `access:view_sod`, `access:update_sod`
   en `catalogo-funciones.rst` — contrato backend.
2. **Concepto SoD en narrativa:** "reglas SoD", "Validar SoD"
   en captions plantuml. SoD = Separation of Duties es
   vocabulario de dominio establecido (analogo a JWT).
3. **STD-013 §82:** `❌ /access/sod-rules` ejemplo educativo.
4. **`source/requisitos/reglas-negocio/rbac/sod.rst`:** archivo
   externo, no afectado por este WP (Opcion 5a).

## Output esperado

**Phase 1 DISCOVER:** este artefacto + audit detallado.

**Phase 5 STRATEGY:** decisiones sobre Cat-3 (codigos),
Cat-4 (filename rename approach), Cat-5 (preservar cross-ref).

**Phase 8 PLAN EXECUTION:** task-plan con T-NNN.

**Phase 10 EXECUTE:** rename atomicamente, 1 archivo = 1 commit.

**Phase 11 TRACK:** build clean serial + cierre.

## Restricciones

- NO renombrar tokens opacos backend.
- NO renombrar concepto "SoD" en captions plantuml ni
  narrativa (es vocabulario de dominio).
- NO renombrar `reglas-negocio/rbac/sod.rst` (out-of-scope).
- Preservar codigos de regla SOD-001..003 (probablemente
  IDs estables — confirmar en Phase 5).
- Strict build (`-W -j 1`) tras los cambios.

## Stopping points

- **SP-01:** aprobar lista de cambios antes de Phase 7/8.
- **SP-02:** strict build EXIT=0.
- **SP-03:** aprobar cierre.

## Hipotesis iniciales

- ~10 archivos con cambios.
- ~50 ediciones individuales.
- 0 cross-refs rotos esperados.
- Build serial al final (consistente con cola actual).

## Refs

- WP `endpoint-sod-rules-rename` (cerrado, mismo dominio).
- WP `std-010-compliance` (cerrado, dejo este gap detras).
- Backend A-001..A-005 (rename SodRule → SeparationRule).
