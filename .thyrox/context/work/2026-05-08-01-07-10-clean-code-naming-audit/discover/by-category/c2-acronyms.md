```yml
created_at: 2026-05-08 01:20:00
project: IACT-docs
work_package: 2026-05-08-01-07-10-clean-code-naming-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: Cat-2 Audit (Acronimos en identificadores)
```

# Cat-2 — Acronimos en identificadores no-opacos

> Norma: CLEAN_CODE_NAMING_PRINCIPLES §8.

## 1. Resumen

| Acronimo | Refs totales | En use-case-view | En requisitos/casos-uso | En domain-model | Files con acronimo en nombre |
|---|---|---|---|---|---|
| `SOD/SoD/sod` | **1225** | 2 (post-cleanup) | 637 | 29 | **10 archivos** |
| `RBAC` | 1373 | — | — | — | varios |
| `AGR_id` | 1 | — | 1 (jerarquia-de-actores) | — | — |

## 2. Distribucion `SOD/SoD/sod`

### 2.1 use-case-view (post-cleanup WP previo)

**2 hits — ambos excepciones documentadas:**

- `mapa-funciones-rbac.rst:184` — cross-ref `:doc:` a archivo
  externo `/reglas-negocio/rbac/sod` (out-of-scope, archivo
  externo no renombrado en ese WP).
- `uc-adm-01-...-de-separacion.rst:24` — codigos BD
  `SOD-001..003` (excepcion §8.3 IDs persistidos).

✅ use-case-view limpio.

### 2.2 requisitos/casos-uso/ — 637 refs (mayor concentracion)

Sample de archivos afectados:

```
source/requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst
source/requisitos/casos-uso/access/uc-acc-01/diagramas-uml/diagrama-de-sod-validation.rst
source/requisitos/casos-uso/access/uc-acc-05/diagramas-uml/diagrama-de-estados-sodrule.rst
source/requisitos/casos-uso/admin/uc-adm-01/* (multiples archivos)
... etc
```

**Severidad alta.** Estos archivos son la fuente principal de
spec textual de UCs.

### 2.3 requisitos/reglas-negocio/ — 58 refs

Concentrados en:

- `br-007-separacion-funciones-sod.rst` (filename con sod).
- `rbac/sod.rst` (filename con sod).

### 2.4 backend/ — 44 refs, domain-model/ — 29 refs

Refs en docs de implementacion + domain-model:

- `domain-model/separation-rule.rst`, `separation-rule-repo.rst`
  pueden tener refs SoD remanentes.
- `backend/` tiene docs de implementacion DRF que mencionan
  SoD endpoints (algunos ya renombrados en WP
  `endpoint-sod-rules-rename`).

## 3. Filenames con acronimo `sod` (10 archivos)

```
source/requisitos/reglas-negocio/br-007-separacion-funciones-sod.rst
source/requisitos/reglas-negocio/rbac/sod.rst
source/arquitectura-tecnica/design-view/act-sod-check.rst
source/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod.rst
source/requisitos/requisitos-funcionales/access/uc-010-asignar-funciones/fr-010-02-validar-sod-antes-asignar.rst
source/normativa/gobernanza/raci-rbac/raci-sod.rst
source/arquitectura-tecnica/modulos/rbac-core/diagramas/evaluacion-conflicto-sod.rst
source/requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst
source/requisitos/casos-uso/access/uc-acc-01/diagramas-uml/diagrama-de-sod-validation.rst
source/requisitos/casos-uso/access/uc-acc-05/diagramas-uml/diagrama-de-estados-sodrule.rst
```

**Cada filename rename requiere:**

- `git mv` del archivo.
- Update toctree(s) que lo referencian.
- Update cross-refs `:doc:` desde otros archivos del corpus.
- Update anchors `:ref:` si los hay.

Renames propuestos (sin tildes ni acentos por STD-007):

| Actual | Propuesto |
|---|---|
| `br-007-separacion-funciones-sod.rst` | `br-007-separacion-de-funciones.rst` |
| `rbac/sod.rst` | `rbac/separacion-de-deberes.rst` |
| `design-view/act-sod-check.rst` | `design-view/act-validacion-separacion.rst` |
| `cnst-030-reglas-de-separacion-de-funciones-sod.rst` | `cnst-030-reglas-de-separacion-de-funciones.rst` |
| `fr-010-02-validar-sod-antes-asignar.rst` | `fr-010-02-validar-separacion-antes-asignar.rst` |
| `raci-rbac/raci-sod.rst` | `raci-rbac/raci-separacion-de-deberes.rst` |
| `rbac-core/diagramas/evaluacion-conflicto-sod.rst` | `rbac-core/diagramas/evaluacion-conflicto-separacion.rst` |
| `diagrama-de-estados-sod-rule.rst` (uc-adm-01) | `diagrama-de-estados-separation-rule.rst` |
| `diagrama-de-sod-validation.rst` (uc-acc-01) | `diagrama-de-validacion-separacion.rst` |
| `diagrama-de-estados-sodrule.rst` (uc-acc-05) | `diagrama-de-estados-separation-rule.rst` |

## 4. Acronimo `RBAC` — 1373 refs

`RBAC` es **acronimo de Role-Based Access Control**, vocabulario
estandar de seguridad informatica.

Aplicacion de §8.4: "RBAC_check" → "permission_check".

Pero `RBAC` como TERMINO en prosa ("el sistema RBAC", "RBAC
v5.6.x") es vocabulario establecido de la disciplina —
analogo a JWT. Posible tratarlo como excepcion implicita
(§7 vocabulario establecido).

**Recomendacion:**

- Preservar `RBAC` como termino en prosa explicativa.
- Renombrar `RBAC` cuando aparece como prefijo/sufijo de
  identificador (ej: `RBACBackend` → `AuthProvider`,
  `RBAC_check` → `permission_check`, `RBAC-gated` →
  "controlado por permisos").

Buscar patrones especificos:

- `RBACBackend` (Cat-1 ya identificado).
- `RBACPermission` (Cat-1 ya identificado).
- `RBAC-gated`, `RBAC-specific` (en informacion-general).

## 5. Acronimo `AGR` — bajo volumen

1 hit detectado: `AGR_id` en pseudocodigo metodologico.

`AGR-NNN` (ej: `AGR-006`, `AGR-008`) son codigos del
catalogo RBAC — IDs estables similares a `SOD-NNN`.
**Excepcion §8.3**: preservar.

`AGR_id` como variable Python en pseudocodigo: violacion §8.4.

## 6. Out-of-scope (preservar)

- Tokens RBAC opacos `access:view_sod`, `access:update_sod`,
  `access:disable_sod` (§8.3).
- Codigos BD `SOD-001..003`, `AGR-001..010` (§8.3).
- "Separation of Duties" en prosa explicativa larga (regulatorio).
- "RBAC" como termino estandar de disciplina (sin sufijo de
  identificador).

## 7. Estimacion de esfuerzo

| Bloque | Ediciones | Archivos | Estimado |
|---|---|---|---|
| Filenames sod (10) | 10 git mv + ~50 cross-ref updates | ~30 | 4-6 h |
| Refs SoD/SOD/sod en casos-uso | ~600 | ~50 archivos | 8-12 h |
| Refs en domain-model (29) + backend (44) | ~70 | ~10 archivos | 2-3 h |
| `RBAC*` identifiers (subset) | ~10-20 | ~10 archivos | 1-2 h |
| **Total** | **~700-800 ediciones** | **~80 archivos** | **~15-25 h** |

## 8. Recomendacion

**WP separado** dedicado al cleanup SoD en casos-uso +
reglas-negocio + filenames. Coordinar con TD-SOD-1 y TD-SOD-2
diferidos del WP `use-case-view-sod-vocabulary`.

## Refs

- CLEAN_CODE_NAMING_PRINCIPLES §8.
- WP previo `use-case-view-sod-vocabulary` (cerrado, scope
  limitado a use-case-view).
