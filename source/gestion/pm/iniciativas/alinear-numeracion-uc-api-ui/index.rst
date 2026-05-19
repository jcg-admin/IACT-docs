.. meta::
   :artefacto: INICIATIVA-ALINEAR-NUMERACION-UC-API-UI
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T22:10:00
   :ultimo_cambio: 2026-05-19T22:10:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-alinear-numeracion-uc-api-ui:

==============================================================
Iniciativa: Alinear Numeracion UC api ↔ ui
==============================================================

P3 plan #11. Resuelve los 3 markers ``UC_USR_05/06/07`` que
existian en UI sin contraparte en API ni en docs.

Investigacion completada
==========================

Aplicando ``grep-validated-audit`` sobre IACT-ui:

* **UC_USR_05** = Bloquear Usuario. UI:
  ``userGateway.js::blockUser``, ``slices/user.js::blockUser``,
  ``pages/users/UserManagement/handleBlockUser``. Llama
  ``POST /api/users/{id}/block/``. **API: endpoint
  AUSENTE** (verificado en
  ``apps/users/urls.py``). Documentado como
  **uc-083** con admonicion warning gap-api.

* **UC_USR_06** = Desbloquear Usuario. UI:
  ``userGateway.js::unblockUser``, ``slices/user.js::unblockUser``.
  Llama ``POST /api/users/{id}/unblock/``. **API: endpoint
  AUSENTE**. Documentado como **uc-084** con admonicion.

* **UC_USR_07** = Editar Perfil Propio. UI:
  ``pages/Profile.jsx``. Llama
  ``PATCH /api/users/profile/``. **API: implementado** en
  ``apps/users/profile_view.py`` ProfileView.patch (sin
  marker explicito). Documentado como **uc-085**.

Cambios aplicados
==================

* RST nuevos:

  - ``requisitos-funcionales/users/uc-083-bloquear-usuario/``
  - ``requisitos-funcionales/users/uc-084-desbloquear-usuario/``
  - ``requisitos-funcionales/users/uc-085-editar-perfil-propio/``

* Enlace en ``users/index.rst`` bajo caption
  "UCs documentados retroactivamente".

* Cada UC con admonicion explicita sobre estado de api:
  uc-083/084 con WARNING gap, uc-085 con NOTE implementado.

Iniciativas candidatas derivadas
==================================

* ``implementar-uc-usr-05-bloquear-usuario``: P1 nueva.
  Implementar endpoint API ``POST /api/users/{id}/block/``
  con state transition + invalidacion de sesiones +
  tests + audit log.
* ``implementar-uc-usr-06-desbloquear-usuario``: P1 nueva.
  Reverso de UC-083.
* ``marcar-uc-usr-07-en-profile-view-api``: P3 trivial.
  Anadir ``UC_USR_07`` al docstring de
  ``apps/users/profile_view.py`` ProfileView.patch para
  cerrar paridad de markers.

.. toctree::
   :maxdepth: 1

   tareas-y-progreso-alinear-numeracion-uc-api-ui
