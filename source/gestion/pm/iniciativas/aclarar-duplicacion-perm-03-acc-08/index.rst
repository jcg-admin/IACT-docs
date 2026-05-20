.. meta::
   :artefacto: INICIATIVA-ACLARAR-DUPLICACION-PERM-03-ACC-08
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-api
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T22:15:00
   :ultimo_cambio: 2026-05-19T22:15:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-aclarar-duplicacion-perm-03-acc-08:

==============================================================
Iniciativa: Aclarar Duplicacion UC_PERM_03 vs UC_ACC_08
==============================================================

P2 plan #10. Resuelve la pregunta abierta en
``verificar-mapping-docs-codigo-todos-los-dominios``:
¿son UC_PERM_03 y UC_ACC_08 duplicados o endpoints
distintos?

Resultado: NO es duplicacion
==============================

Investigacion en
``apps/access/exceptional_permission_views.py`` y
``exceptional_permission_service.py``:

* **UC_ACC_08** = ``ExceptionalGrantView`` (clase).
  Endpoint ``POST /api/users/{user_id}/exceptional-permissions/``.
  **Concede el permiso excepcional con persistencia** —
  crea ``ExceptionalPermission`` y emite audit log.

* **UC_PERM_03** = ``ExceptionalPreviewView`` (clase).
  Endpoint ``GET /api/users/{user_id}/exceptional-permissions/preview/``.
  **Calcula impacto sin persistir** ni emitir audit
  (CA-PERM-01: preview sin side-effects).

Son **dos endpoints distintos del mismo UC docs**
(uc-014-conceder-permiso-excepcional-perm):

* GET (preview): UC_PERM_03 — el admin valida que
  asignar X permisos al usuario tiene el impacto
  deseado antes de comprometer.
* POST (commit): UC_ACC_08 — confirma la operacion,
  persiste, audita.

El docstring del archivo
``apps/access/exceptional_permission_views.py`` ya lo
documenta literalmente:

::

   UC_ACC_08/PERM_03 — Conceder permiso excepcional.
   UC_PERM_03        — Preview sin persistir.

Separacion legitima (read-only preview vs
state-changing commit) — patron comun en APIs de
RBAC y compliance.

Cambios aplicados
==================

Ninguno en codigo (los markers ya documentan la
separacion correctamente). Esta iniciativa **cierra la
pregunta** como NO-DUPLICACION confirmada.

Iniciativa candidata derivada
================================

* ``documentar-preview-vs-commit-en-uc-014``: P3
  trivial. Anadir nota en el RST de
  ``uc-014-conceder-permiso-excepcional-perm`` que
  documente la separacion preview/commit y sus dos
  markers. Mejora la trazabilidad para futuras
  auditorias.
