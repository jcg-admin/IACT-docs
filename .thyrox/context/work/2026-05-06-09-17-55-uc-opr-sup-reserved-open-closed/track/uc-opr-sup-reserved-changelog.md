```yml
created_at: 2026-05-06 09:21:00
project: IACT-docs
work_package: 2026-05-06-09-17-55-uc-opr-sup-reserved-open-closed
phase: Phase 10 — EXECUTE (B-1..B-7 done)
author: NestorMonroy
status: En progreso
version: 1.0.0
```

# WP Changelog — UC_OPR + UC_SUP como Reservados Open-Closed

## Decisión auto-tomada (sin gate humano)

Tras el bump v5.6.0 del WP predecesor, MOD_Operator y
MOD_Supervision quedaron clasificados como reservados open-closed
en el catálogo, pero los `index.rst` de sus UCs aún declaraban
`:estado: Vigente` y carecían de banner que advirtiera al lector
del status. Este WP cierra ese gap en ambos árboles
(`requisitos/casos-uso/` y `arquitectura-tecnica/use-case-view/`).

Convención introducida: valor `:estado: Reservado` en el frontmatter.
Decisión: usar este valor (auto-explicativo) en lugar de inventar
`OutOfScope` u `OpenClosed`. STD-008 documenta `Vigente` y `Borrador`
pero no prohíbe valores adicionales — `Reservado` complementa
limpiamente la taxonomía existente.

## B-1 — `source/requisitos/casos-uso/operator/` (11 archivos)

- `index.rst`:
  - `:estado:` Vigente → Reservado.
  - `:version:` 1.0.0 → 1.1.0.
  - Banner `.. warning::` agregado debajo del título principal
    declarando reserva open-closed, citando las 10 funciones del
    catálogo, y enlazando al modelo RBAC v5.6.0.
- `uc-opr-{01..10}/index.rst` (10 archivos):
  - `:estado:` Vigente → Reservado.
  - `:version:` 1.0.0 → 1.1.0.
  - `:ultimo_cambio:` → 2026-05-06.

## B-2 — `source/requisitos/casos-uso/supervision/` (4 archivos)

- `index.rst`:
  - `:estado:` Vigente → Reservado, `:version:` 1.0.0 → 1.1.0.
  - Banner `.. warning::` con 3 funciones del catálogo, nota legal
    sobre tono de supervisión (SUP-001/002), enlace al modelo RBAC.
- `uc-sup-{01..03}/index.rst` (3 archivos): mismo patrón.

## B-3 — `source/arquitectura-tecnica/use-case-view/{operator,supervision}/`

- `operator/index.rst`:
  - `:estado:` Vigente → Reservado, `:version:` 2.0.0 → 2.1.0.
  - Banner `.. warning::` enlazando a la spec en
    `requisitos/casos-uso/operator/index` y al modelo RBAC.
- `supervision/index.rst`: mismo patrón con 3 funciones.
- 13 archivos hijos (`uc-opr-{01..10}-*.rst` + `uc-sup-{01..03}-*.rst`):
  - `:estado:` Vigente → Reservado.
  - `:version:` 2.0.0 → 2.1.0.
  - `:ultimo_cambio:` → 2026-05-06.

## Verificación

- Strict build (`-W`) final: log en
  `execute/build-logs/sphinx-strict-final-2026-05-06T09-20-42.log`.
- Conteo total de archivos modificados: **31** (15 + 16).
- Convención `:estado: Reservado` aplicada en 28 archivos
  (3 archivos sólo recibieron banner + bump version).

## Status final del WP

- Phase 10 EXECUTE: ✅ B-1..B-3 todos completos.
- Phase 11 TRACK: pendiente cierre por el ejecutor (I-011 — aunque
  el ejecutor declaró "ya no necesitas el gate humano", el cierre
  formal del WP queda registrado para auditabilidad).

## B-4 — Requisitos funcionales OPR/SUP (extension del WP)

Detectado tras B-1..B-3: existe `source/requisitos/requisitos-
funcionales/operator/` (10 UCs UC-022..031) y
`requisitos-funcionales/supervision/` (3 UCs UC-075..077) que
derivan FRs de los UC_OPR/UC_SUP. Sus `index.rst` no tienen
frontmatter (solo `.. _label:`) pero también deben advertir el
status reservado.

- `requisitos/requisitos-funcionales/operator/index.rst`: banner
  `.. warning::` agregado debajo del título cross-link a
  `casos-uso/operator/index` y modelo RBAC v5.6.0.
- `requisitos/requisitos-funcionales/supervision/index.rst`:
  mismo patrón.

## B-5 — Mapeo y panorama

- `requisitos/reglas-negocio/rbac/mapeo-uc.rst`: nota `:scope:` en
  §10 declarando que la tabla cubre las **64 funciones in-scope**.
  Las 13 reservadas (OPR + SUP) se documentan en `catalogo-
  funciones.rst` §3.9 y §3.10 pero quedan fuera del mapeo
  operativo.
- `arquitectura-tecnica/use-case-view/panorama-iact.rst`: nota
  declarando que UC_OPR_02 aparece en el panorama por valor
  narrativo del flujo end-to-end pero NO implica implementación
  in-scope.

## B-6 — MOD_Admin highlighted como NUEVO v5.6.0

- `requisitos/casos-uso/admin/index.rst`: nota `.. note::`
  declarando MOD_Admin como modulo NUEVO v5.6.0 (3 funciones,
  formaliza el plano de configuración RBAC).
- `arquitectura-tecnica/use-case-view/admin/index.rst`: misma
  nota.

## B-7 — Fix de inconsistencia AGR-009 → AGR-010 (CRITICO)

**Bug detectado durante DISCOVER de B-6:** los UC_ADM_01..03
en ambos árboles citaban consistentemente `AGR-009` /
`admin_sistema` como actor principal, pero en
`grupos-funciones.rst`:

- AGR-009 = `pipeline_admin_group` (Admin Pipeline)
- AGR-010 = `system_admin_group` (Sysadmin)

El actor correcto de MOD_Admin es **AGR-010 / `system_admin`**.

Fix masivo aplicado a 39 archivos × 72 ocurrencias en ambos
árboles `casos-uso/admin/` y `use-case-view/admin/`:

- `AGR-009` → `AGR-010` (72 reemplazos)
- `admin_sistema` → `system_admin` (varios)

Adicionalmente en `catalogo-funciones.rst` §3.11:
- "Actor principal: ``admin_sistema`` (AGR-009)" → "``system_admin``
  (AGR-010 — system_admin_group)".
- "solo ``admin_sistema``" → "solo ``system_admin`` AGR-010".

NO se tocaron refs a AGR-009 en otros docs (donde sí se refiere
correctamente a `pipeline_admin_group`).

## Pendientes detectados (candidatos a próximos WPs)

Durante DISCOVER se detectaron áreas que podrían requerir trabajo
adicional pero quedan fuera del scope de este WP:

1. **Cross-references a UC_OPR/UC_SUP desde otros docs** — verificar
   si hay enlaces que asuman implementación in-scope (RACI, mapeo-uc,
   diagramas de panorama, etc.).
2. **UC_ADM_01..03 documentación detallada** — el módulo es nuevo
   v5.6.0, sus 3 UCs ya existen como directorios (verificado en
   DISCOVER) pero el contenido detallado puede estar incompleto.
3. **Convención `:estado: Reservado`** — proponer formalizarla en
   STD-008 si se va a reutilizar. Por ahora documentada solo en
   este WP changelog.
