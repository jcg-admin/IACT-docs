.. _uc_085_editar_perfil_propio:

==================================================
UC-085: Editar Perfil Propio
==================================================

.. note::

   UC documentado retroactivamente por
   ``alinear-numeracion-uc-api-ui``. Marker
   ``UC_USR_07`` existe en UI
   (``IACT-ui/src/pages/Profile.jsx``).

   **API implementada:** PATCH /api/users/profile/ en
   ``apps/users/profile_view.py`` (ProfileView con
   metodo patch). El UC esta funcionalmente cubierto en
   ambos repos pero faltaba documentacion.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-085
   * - **Marker código UI**
     - ``UC_USR_07``
   * - **Marker código API**
     - (sin marker explicito; implementacion
       en ``apps/users/profile_view.py`` PATCH)
   * - **Nombre**
     - Editar Perfil Propio
   * - **Actor**
     - Usuario autenticado (cualquier rol)
   * - **Módulo**
     - MOD_Users
   * - **Tipo**
     - Funcional / Self-service

2. Especificación
-----------------

Endpoint self-service que permite al usuario autenticado
editar su propio perfil: nombre, apellido, correo,
preferencias de notificacion. Endpoint:
``PATCH /api/users/profile/``.

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker UI**
     - ``UC_USR_07`` (Profile.jsx)
   * - **Marker API**
     - sin marker — sugerencia: agregar
       ``UC_USR_07`` al docstring de
       ProfileView.patch para cerrar paridad.
   * - **TEST**
     - TST-fr-085-XX (pendiente)
   * - **Iniciativa origen**
     - alinear-numeracion-uc-api-ui
