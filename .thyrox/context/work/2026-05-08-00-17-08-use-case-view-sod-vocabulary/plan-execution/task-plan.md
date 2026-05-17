```yml
created_at: 2026-05-08 00:55:00
project: IACT-docs
work_package: 2026-05-08-00-17-08-use-case-view-sod-vocabulary
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Aprobado
version: 1.0.0
type: Task Plan
```

# Task Plan — sod vocabulary cleanup (scope ampliado)

## Reglas de rename

| Forma actual | Forma canonica |
|---|---|
| `VALIDAR_SOD` (alias plantuml) | `VALIDAR_SEPARATION_RULES` |
| `SOD_RULE_*` (eventos audit) | `SEPARATION_RULE_*` |
| `"Validar SoD\n(...)"` (caption usecase) | `"Validar regla de separacion\n(...)"` |
| `"reglas SoD"` / `"reglas SoD evaluadas"` (narrativa) | `"reglas de separacion"` |
| `"reglas estaticas SOD-001..003"` (narrativa de codigos) | `"reglas estaticas SOD-001..003"` (PRESERVAR — codigos BD) |
| `uc-acc-05-gestionar-reglas-sod.rst` | `uc-acc-05-gestionar-reglas-de-separacion.rst` |
| `uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst` | `uc-adm-01-gestionar-ciclo-de-vida-de-reglas-de-separacion.rst` |
| Anchors `_at_uc_*_sod` | `_at_uc_*_separacion` |

## Excepciones (NO tocar)

- Tokens opacos `access:view_sod`, `access:update_sod`,
  `access:disable_sod` (catalogo-funciones — fuera de
  use-case-view).
- `:doc:`/requisitos/reglas-negocio/rbac/sod`` en
  `mapa-funciones-rbac.rst:184` — cross-ref a archivo
  externo (out-of-scope).
- Codigos BD `SOD-001..003` en narrativa (preservar).
- "Separation of Duties" en prosa explicativa larga.

## Bloque EXECUTE — 13 archivos = 13 commits

Cada commit consolida TODAS las categorias de cambio que
apliquen al archivo (Cat-1 + Cat-2 + Cat-3 si coexisten).

### Cluster access (4 archivos)

- [ ] **T-001** — `access/uc-acc-01-asignar-funciones.rst`
  (Cat-1 + Cat-2 + Cat-3).
- [ ] **T-002** — `access/uc-acc-04-asignar-agrupador.rst`
  (Cat-1 + Cat-2 + Cat-3).
- [ ] **T-003** — `access/uc-acc-08-permiso-temporal.rst`
  (Cat-1 + Cat-2 + Cat-3).
- [ ] **T-004** — `access/uc-acc-05-gestionar-reglas-sod.rst`
  → `access/uc-acc-05-gestionar-reglas-de-separacion.rst`
  (Cat-4 git mv + anchors + body content).
- [ ] **T-005** — `access/index.rst`
  (Cat-4 toctree update).

### Cluster admin (3 archivos)

- [ ] **T-006** — `admin/uc-adm-03-gestionar-catalogo-de-agrupadores-del-sistema.rst`
  (Cat-1 + Cat-2 + Cat-3).
- [ ] **T-007** — `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst`
  → `admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-de-separacion.rst`
  (Cat-4 git mv + Cat-2 + Cat-3 + anchors).
- [ ] **T-008** — `admin/index.rst`
  (Cat-4 toctree update).

### Cluster permissions (4 archivos)

- [ ] **T-009** — `permissions/uc-perm-01-asignar-grupo-a-usuario.rst`
  (Cat-1 + Cat-2 + Cat-3).
- [ ] **T-010** — `permissions/uc-perm-03-conceder-permiso-excepcional.rst`
  (Cat-1 + Cat-2 + Cat-3).
- [ ] **T-011** — `permissions/uc-perm-06-asignar-funciones-a-grupo.rst`
  (Cat-1 + Cat-2 + Cat-3).
- [ ] **T-012** — `permissions/uc-perm-10-consultar-auditoria-de-permisos.rst`
  (Cat-2 caption AuditEvent SOD_RULE).

### Vista global (1 archivo)

- [ ] **T-013** — `mapa-funciones-rbac.rst`
  (Cat-3 narrativa "reglas SoD"; preservar Cat-5 cross-ref
  a `rbac/sod`).

## Bloque TRACK (1 tarea)

- [ ] **TR-01** — Cierre: changelog + wp-state status=Cerrado.
  Build serial diferido al final de la cola.

## Convenciones de commit (Tim Pope)

| Categoria | Patron |
|---|---|
| Solo Cat-1 | `Rename VALIDAR_SOD to VALIDAR_SEPARATION_RULES in {file}` |
| Solo Cat-2 | `Replace SoD captions with Separation in {file}` |
| Solo Cat-3 | `Replace SoD narrative references in {file}` |
| Cat-4 (rename) | `Rename {old-file} to {new-file}` |
| Combinado | `Replace SOD identifiers and narrative in {file}` |

Body referencia:
- Categoria(s) aplicada(s).
- Backend A-001 (alineacion).
- Directiva ejecutor "no Sod en identificadores".

## Validacion final

```bash
# Esperado: cero hits (excepto las 3 excepciones explicitas)
grep -rnE "VALIDAR_SOD\b|SOD_RULE_|reglas SoD|Validar SoD|reglas-sod\.rst" source/arquitectura-tecnica/use-case-view/

# Cross-ref preservada (cat-5):
grep -rn "/reglas-negocio/rbac/sod" source/arquitectura-tecnica/use-case-view/  # 1 hit OK

# Codigos BD preservados (cat-3 narrativa codigos):
grep -rn "SOD-00[0-9]" source/arquitectura-tecnica/use-case-view/  # ok si solo en narrativa de codigos
```
