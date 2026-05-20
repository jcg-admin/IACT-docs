.. _uc_084_desbloquear_usuario:

==================================================
UC-084: Desbloquear Usuario
==================================================

.. note::

   UC documentado retroactivamente por
   ``alinear-numeracion-uc-api-ui``. Marker
   ``UC_USR_06`` existe en UI, ausente en API.

.. warning::

   **Gap api:** UI llama
   ``POST /api/users/{id}/unblock/`` — endpoint no
   existe en API. Deuda registrada como iniciativa
   candidata ``implementar-uc-usr-06-desbloquear-usuario``.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-084
   * - **Marker código UI**
     - ``UC_USR_06``
   * - **Marker código API**
     - (ausente)
   * - **Nombre**
     - Desbloquear Usuario
   * - **Actor**
     - Admin
   * - **Módulo**
     - MOD_Users
   * - **Tipo**
     - Funcional / Admin / Seguridad

2. Especificación
-----------------

Reverso de UC-083 (bloquear). Re-habilita una cuenta
previamente bloqueada. Endpoint esperado:
``POST /api/users/{id}/unblock/``.

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker UI**
     - ``UC_USR_06``
   * - **Marker API**
     - **AUSENTE — implementacion pendiente**
   * - **TEST**
     - TST-fr-084-XX (pendiente)
   * - **Iniciativa origen**
     - alinear-numeracion-uc-api-ui
