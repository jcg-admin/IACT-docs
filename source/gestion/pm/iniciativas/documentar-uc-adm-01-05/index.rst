.. meta::
   :artefacto: INICIATIVA-DOCUMENTAR-UC-ADM-01-05
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-20T03:00:00
   :ultimo_cambio: 2026-05-20T03:30:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-documentar-uc-adm-01-05:

============================================================================
Iniciativa: Documentar UC_ADM_01..05 (spec-from-code retroactivo)
============================================================================

Origen
======

Durante el audit funcional ``auditar-conformidad-uc-codigo-vs-docs``,
el sponsor pregunto explicitamente: **"en el Dominio no ace falta
el de admin?"**. Verificacion confirmo deuda inversa: 5 UCs
implementados en codigo (API + UI) sin spec en
``source/requisitos/requisitos-funcionales/``.

Resultado
=========

Creados 5 UCs nuevos en
``source/requisitos/requisitos-funcionales/admin/``:

.. list-table::
   :header-rows: 1
   :widths: 12 28 25 35

   * - Marker codigo
   * - UC nuevo
   * - Component UI
   * - FRs creados
   * - UC_ADM_01
   * - UC-086 catalogo-reglas-separacion-funciones
   * - SeparationRulesCatalog.jsx
   * - 3 FRs (listar / CRUD / validate preview)
   * - UC_ADM_02
   * - UC-087 catalogo-funciones-rbac
   * - FunctionCatalogPage
   * - 1 FR (GET readonly)
   * - UC_ADM_03
   * - UC-088 catalogo-grupos-acceso
   * - AGRCatalog.jsx
   * - 1 FR (listar) + alias declarado a UC-016/UC_PERM_05
   * - UC_ADM_04
   * - UC-089 catalogo-menu-items
   * - MenuItemCatalog.jsx
   * - 2 FRs (CRUD + bulk reorder)
   * - UC_ADM_05
   * - UC-090 ciclo-vida-menu-items
   * - (backend service MenuLifecycleService)
   * - 2 FRs (state machine + auto-archive 90d)

Total: 5 UCs + 9 FRs documentados.

Verificacion epistemica (recursive audit)
==========================================

Tras crear las specs, sponsor pidio verificar conformidad
textual vs IACT-ui/docs. Agent Explore audito 15 claims:

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Veredicto
     - Count
     - Significado
   * - **PROVEN**
     - 9
     - Claim + codigo verificado + docs IACT-ui menciona
   * - **AMPLIACION**
     - 6
     - Claim + codigo verificado; docs UI no menciona pero
       no contradice (codigo mas completo que docs UI)
   * - **SPECULATIVE**
     - 0
     - —
   * - **NO-CONFORME**
     - 0
     - —

Cero inventos, cero malinterpretaciones. Las 6 "ampliaciones"
indican que el codigo esta mas completo que la documentacion
interna de IACT-ui — situacion opuesta a deuda, mas bien
**documentacion incompleta del lado UI** que esta iniciativa
cierra.

Lecciones
=========

L-1 — Existe deuda inversa: implementacion sin spec
----------------------------------------------------

UC_ADM_01..05 fueron implementados antes de que existiera la
spec canonica. Este patron (similar a uc-078..082 cerrado por
``documentar-ucs-implementados-no-declarados``) requiere
vigilancia continua — un audit periodico de markers UC en
codigo vs UC carpetas en docs.

L-2 — Spec-from-code es valido si se verifica
-----------------------------------------------

Crear spec basado en codigo SIEMPRE requiere verificacion
recursiva (este audit con 15/15 PROVEN/AMPLIACION lo confirma).
El metodo "leer codigo y describir su comportamiento" es
distinto de "inventar requisitos" — la diferencia es la
verificacion textual contra observables.

L-3 — IACT-ui/docs es complementario, no canonico
---------------------------------------------------

Las menciones en ``IACT-ui/docs/HALLAZGOS-*.md`` y
``project-scope/`` son utiles como evidencia de uso (componentes
existen, refactors fueron hechos) pero NO sustituyen una spec
canonica. La verdad esta en el codigo + IACT-docs spec
canonica.

Estado de cierre
=================

* 5 UCs creados, 9 FRs, todos wireados en toctree.
* dominio ``admin/`` agregado al index global de funcionales.
* Verificacion recursiva: 15/15 PROVEN o AMPLIACION.
* Commit ``feature/documentar-uc-adm-01-05`` empujado.
* Iniciativa ``auditar-conformidad-uc-codigo-vs-docs``
  actualizada para reflejar +5 UCs nuevos en scope.
