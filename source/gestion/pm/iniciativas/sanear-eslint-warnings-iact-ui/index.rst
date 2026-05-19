.. meta::
   :artefacto: INICIATIVA-SANEAR-ESLINT-WARNINGS-IACT-UI
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-ui
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T22:25:00
   :ultimo_cambio: 2026-05-19T22:25:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-sanear-eslint-warnings-iact-ui:

==============================================================
Iniciativa: Sanear ESLint Warnings IACT-ui
==============================================================

P3 plan #7. Aplica ``npm run lint -- --fix`` y documenta
las 198 warnings restantes con priorizacion por categoria.

Resultado
==========

* 204 warnings inicial -> 198 tras ``--fix`` (6
  auto-fixable cerradas).
* 6 archivos modificados (cambio trivial de formato).
* npm test sin regresion: 250 suites / 2381 tests
  passing.
* Commit IACT-ui ``caa17ce``.

Distribucion de las 198 warnings restantes
=============================================

.. list-table::
   :header-rows: 1
   :widths: 12 50 18 20

   * - Cantidad
     - Regla
     - Severidad
     - Iniciativa candidata
   * - 138
     - ``no-unused-vars``
     - Baja-mecanica
     - sanear-eslint-no-unused-vars-iact-ui
   * - 43
     - ``react/prop-types``
     - Media (TS migration deferred)
     - migrar-iact-ui-a-typescript
   * - 11
     - ``react-hooks/exhaustive-deps``
     - Alta (potenciales bugs)
     - revisar-react-hooks-deps-iact-ui
   * - 6
     - ``no-console``
     - Baja
     - adoptar-logger-estructurado-iact-ui

Decision arquitectonica
========================

**NO silenciar reglas globalmente.** Cada warning
representa deuda real:

* ``react/prop-types`` se resuelve naturalmente con
  migracion a TypeScript (proyecto declarado JS pero ya
  tiene ``tsconfig.json`` y babel-preset-typescript —
  migracion incremental viable).
* ``no-unused-vars`` cada caso es un olvido de
  cleanup o un parametro intencional sin marcar con
  ``_`` prefix.
* ``react-hooks/exhaustive-deps`` es la categoria MAS
  importante — puede esconder bugs sutiles de stale
  closures.
* ``no-console`` es cosmetico pero el dia que se
  introduzca un logger estructurado, todos deben
  migrar coherentemente.

Iniciativas candidatas derivadas (4)
=====================================

Las 4 sub-iniciativas listadas arriba pueden
priorizarse por riesgo:

1. **Alta** — ``revisar-react-hooks-deps-iact-ui`` (11
   warnings, riesgo bugs).
2. **Media** — ``migrar-iact-ui-a-typescript`` (43
   prop-types + beneficios colaterales, scope grande).
3. **Baja** — ``sanear-eslint-no-unused-vars-iact-ui``
   (138, mecanico).
4. **Baja** — ``adoptar-logger-estructurado-iact-ui``
   (6, requiere decision de libreria — pino, winston,
   etc.).
