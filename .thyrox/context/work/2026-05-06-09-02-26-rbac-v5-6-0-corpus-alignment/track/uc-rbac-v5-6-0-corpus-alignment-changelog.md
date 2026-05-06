```yml
created_at: 2026-05-06 09:14:00
project: IACT-docs
work_package: 2026-05-06-09-02-26-rbac-v5-6-0-corpus-alignment
phase: Phase 10 — EXECUTE (B-1..B-6 done)
author: NestorMonroy
status: En progreso
version: 1.0.0
```

# WP Changelog — RBAC v5.6.0 Corpus Alignment

## Decisión de framing

Bumpear el corpus a **RBAC v5.6.0** con scope re-categorizado:

- **9 módulos activos / 64 funciones in-scope:** MOD_Auth (4),
  MOD_Users (9), MOD_Access (12), MOD_Pipeline (4), MOD_Reports (11),
  MOD_Alerts (10), MOD_Audit (4), MOD_Logs (7), **MOD_Admin (3 — NUEVO
  v5.6.0)**.
- **2 módulos reservados / 13 funciones out-of-scope (open-closed):**
  MOD_Operator (10) y MOD_Supervision (3) — declarados en el catálogo
  como extension points, no implementables en esta release.
- **Total catálogo declarado:** 77 funciones (= 64 activas + 13 reservadas).
- 12 grupos AGR-001..012 y 3 reglas SoD se mantienen sin cambio.

Conteo verificado por enumeración automática del catálogo:
`4+9+12+4+11+10+4+7+3 = 64` (in-scope) + `10+3 = 13` (reservadas) = `77`.

## B-1 — RBAC canónico (`source/arquitectura-tecnica/rbac/`)

### Changed

- `modelo-rbac-iact/index.rst`: `:version: 5.5.0` → `5.6.0`; nota
  reescrita explicando los 9 módulos in-scope (con MOD_Admin nuevo)
  y los 2 reservados open-closed (OPR+SUP).
- `modelo-rbac-iact/arquitectura.rst`: tabla §2.1 reorganizada en
  3 secciones — 64 activas (con MOD_Admin), 13 reservadas open-closed
  (OPR+SUP), total 77.
- `modelo-rbac-iact/implementacion.rst`: §8.8 "74 Funciones (v5.5.0)"
  → "64 Funciones Activas (v5.6.0)"; comentario `# Inicializar RBAC
  v5.2.1` → `v5.6.0`; comando `initialize_functions # 74 funciones`
  → `# 64 funciones activas (in-scope)`.
- `modelo-rbac-iact/modelo-datos.rst`: tabla functions = 64 activas.
- `modelo-rbac-iact/diagramas/clases-entidades-rbac.rst`: caption
  ahora cita v5.6.0 + 64 activas + 77 declaradas.
- `modelo-rbac-iact/resumen.rst`: §12.1 metricas reescrito (modulos
  activos vs reservados); footer §12.2 metadata bumpeado v5.2.1 →
  v5.6.0 con changelog completo (5.2.0 → 5.6.0). RST fix: blank lines
  entre paragraphs y bullet list.

## B-2 — Reglas de negocio RBAC (`source/requisitos/reglas-negocio/`)

- `rbac/catalogo-funciones.rst`: header §3 "73 FUNCIONES" → "77
  FUNCIONES (v5.6.0)" con desglose 64 activas + 13 reservadas.
- `br-006-rbac-flat-nist.rst`: 3 lugares "74 funciones atomicas"
  actualizados a "64 activas (catalogo declara 77...)".
- `br-009-bajas-logicas.rst`: §5.3 header "RBAC v5.4.0 motivados"
  → "v5.4.0+ ... vigentes en v5.6.0".

## B-3 — Base cognitiva (frontmatter compartido + fnd*)

11 archivos con boilerplate `"Sin Pretensiones" del modelo vigente
v5.5.0: 74 funciones atomicas + 12 grupos predefinidos AGR-001..012`
actualizado a `v5.6.0: 64 funciones atomicas activas (catalogo
declara 77 con 13 reservadas open-closed para MOD_Operator y
MOD_Supervision) + 12 grupos`:

- `_ontologia-sbvr/index.rst`, `sbvr-01..05.rst` (6 archivos)
- `_taxonomias-y-metamodelos/metamodelos/mtm-01-...rst`
- `_taxonomias-y-metamodelos/taxonomias/txm-01-...rst`,
  `txm-03-...rst`
- `_fundamentos-conceptuales/fnd-03-casos-de-uso.rst`,
  `fnd-06-derivacion-vs-transformacion.rst`

Adicionales:

- `_taxonomias-y-metamodelos/metamodelos/mtm-03-metamodelo-rbac.rst`:
  3 ocurrencias de "74 funciones" actualizadas a "64 funciones
  activas".
- `_fundamentos-conceptuales/fnd-00-contexto-y-jerarquia.rst`:
  bullet "Modelo RBAC v5.5.0 con 74 funciones" → "v5.6.0 con 64
  activas (77 declaradas, 13 reservadas open-closed) y 12
  agrupadores"; cuadro "MODELO RBAC v5.5.0" expandido con desglose
  módulos activos / reservados / total.
- `_fundamentos-conceptuales/fnd-03-casos-de-uso.rst`:
  §3.4 "Agrupadores RBAC v5.5.0" → "v5.6.0"; §8 "modelo RBAC v5.5.0"
  → "v5.6.0" + clarificación "11 modulos declarados (9 activos + 2
  reservados open-closed)".

## B-4 — Arquitectura técnica (`source/arquitectura-tecnica/`)

- `modelo-dominio-iact.rst`: 7 ocurrencias.
- `domain-model/overview.rst`: 3 ocurrencias.
- `domain-model/access-group-function.rst`: 1.
- `context-view/context-diagram.rst`: 1.
- `context-view/stakeholders.rst`: 2.
- `perspectivas/perspectiva-security.rst`: 1.
- `operational-view/system-installation.rst`: 1.
- `matriz-dependencias-uc-iact.rst`: 1.

Patrón aplicado: "RBAC v5.5.0" → "v5.6.0"; "74 funciones [atomicas]"
→ "64 funciones activas (77 declaradas, 13 reservadas open-closed)".

## B-5 — Backend ADRs + normativa

- `backend/adr-back-005-middleware-decoradores-permisos.rst`:
  cifras del modelo bumpeadas.
- `backend/adr-back-001-grupos-funcionales-sin-jerarquia.rst`:
  cita "19 funciones / 130+ capacidades vs 74 funciones / 12" →
  "vs 64 funciones activas / 12".
- `normativa/restricciones/cnst-029-rbac-modelo-plano.rst`:
  "modelo plano + 74 funciones" → "+ 64 activas (77 declaradas)".
- `normativa/gobernanza/raci-rbac/index.rst`,
  `raci-rbac/trazabilidad.rst`: alineados a v5.6.0 + 64 activas.
- `normativa/gobernanza/adr-gob-009-rbac-modelo-conceptual.rst`:
  §2.1 catálogo reescrito (catálogo cerrado al set activo, abierto
  a extensión); §3.3 cifra "61/10/3" → "64/12/3"; bloque "74
  funciones distribuidas" expandido con desglose
  in-scope/reservado.
- `normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm.rst`:
  "Catalogo cerrado: 74 funciones atomicas..." → "Catalogo cerrado
  al set activo, abierto a extension: 64 activas + 13 reservadas
  open-closed + 12 grupos".

## B-6 — Metodología y casos de uso

- `requisitos/_metodologia-aplicacion/plan-documentacion-uc.rst`:
  cita "OPR, SUP, CLI con sus 74 funciones" → "64 funciones
  activas".
- `requisitos/_metodologia-aplicacion/relaciones-uml/agregacion-grupo-
  agrega-funciones.rst`: caption del diagrama UML.
- `requisitos/_metodologia-aplicacion/relaciones-uml/funcion-compuesta-
  funcion-funcion.rst`: caption.
- `requisitos/_metodologia-aplicacion/agregacion-interfaces/funcion-
  grupo-catalogo-rbac-iact.rst`: caption.

NOTA: refs a "12 agrupadores predefinidos del sistema" en
`uc-adm-03/informacion-general.rst` y
`use-case-view/admin/uc-adm-03-...rst` se mantuvieron sin cambio
— el conteo de grupos no varía entre v5.5.0 y v5.6.0.

## Verificación

- 6 batches × strict build (`-W`) tras edición de cada zona — todos
  EXIT=0 (`execute/build-logs/sphinx-strict-*.log`).
- Conteo final residual:

```
grep -rniE "RBAC v5.5.0|74 funciones" source/ → 0 ocurrencias relevantes
grep -rnE "73 [Ff]unciones" source/ → 0 ocurrencias
```

Refs históricas preservadas (con contexto temporal):
- `fnd-03-casos-de-uso.rst:342, 837` — "RBAC v5.2.x" (mención de
  versiones pasadas, OK).
- `std-006-versionado-semantico.rst:251` — "MODELO RBAC v5.2.x"
  (referencia histórica de versionado, OK).

## Status final del WP

- Phase 10 EXECUTE: ✅ B-1..B-6 todos completos.
- Phase 11 TRACK: pendiente cierre por el ejecutor (I-011).

## Pendiente declarado por el ejecutor

> "cuando terminas vas a abrir un nuevo wp, para actualizar
> source/arquitectura-tecnica/* y source/requisitos/*"

Próximo WP: bootstrap pendiente de scope explícito del ejecutor.
