.. _uc_083_bloquear_usuario:

==================================================
UC-083: Bloquear Usuario
==================================================

.. note::

   UC documentado retroactivamente por la iniciativa
   ``alinear-numeracion-uc-api-ui``. El marker
   ``UC_USR_05`` existe en codigo UI
   (``IACT-ui/src/services/userGateway.js`` +
   ``redux/slices/user.js`` +
   ``pages/users/UserManagement/``) pero NO en codigo
   API.

.. warning::

   **Gap api detectado:** la UI llama
   ``POST /api/users/{id}/block/`` pero el endpoint no
   existe en ``IACT-api/callcentersite/apps/users/urls.py``.
   Cualquier intento de bloquear usuario desde la UI
   resultaria en 404. Registrado como deuda en
   iniciativa candidata
   ``implementar-uc-usr-05-bloquear-usuario``.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-083
   * - **Marker código UI**
     - ``UC_USR_05``
   * - **Marker código API**
     - (ausente)
   * - **Nombre**
     - Bloquear Usuario
   * - **Actor**
     - Admin
   * - **Módulo**
     - MOD_Users
   * - **Tipo**
     - Funcional / Admin / Seguridad

2. Especificación
-----------------

Endpoint admin que bloquea (suspende) una cuenta de
usuario sin eliminarla. Invalida todas las sesiones
activas del usuario afectado. Reversible via UC-084.

Endpoint esperado: ``POST /api/users/{id}/block/``.
Response: ``200 OK`` con usuario actualizado +
``state='BLOCKED'``.

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker UI**
     - ``UC_USR_05`` (userGateway.js, slices/user.js)
   * - **Marker API**
     - **AUSENTE — implementacion pendiente**
   * - **TEST**
     - TST-fr-083-XX (pendiente)
   * - **Iniciativa origen**
     - alinear-numeracion-uc-api-ui
