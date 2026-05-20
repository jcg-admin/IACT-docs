.. _uc_078_permisos_efectivos_del_usuario:

==================================================
UC-078: Consultar Permisos Efectivos del Usuario
==================================================

.. note::

   UC documentado retroactivamente por la iniciativa
   ``documentar-ucs-implementados-no-declarados``. El
   marker ``UC_ACC_03`` ya existia en codigo
   (apps/access/) con la descripcion "Permisos del
   usuario (alias accessService)" pero carecia de RST
   en docs.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-078
   * - **Marker código**
     - ``UC_ACC_03``
   * - **Nombre**
     - Consultar Permisos Efectivos del Usuario
   * - **Actor**
     - Admin / Sistema
   * - **Módulo**
     - MOD_Access
   * - **Tipo**
     - Inclusion / Consulta (alias accessService)

2. Especificación
-----------------

Endpoint de consulta agregada que retorna el conjunto
efectivo de permisos para un usuario dado, considerando:

* Funciones asignadas directamente (UC-010 / UC_ACC_01).
* Grupos (AGR) asignados (UC-012 / UC_PERM_01).
* Permisos excepcionales activos (UC-014 / UC_PERM_03).
* Excepciones revocadas (UC-015 / UC_PERM_04).

Es la pieza usada por ``apps.access.services.accessService``
y por el middleware de autorizacion (HasFunction) para
resolver "puede X" sin recorrer todas las relaciones FK
en cada request.

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker código**
     - ``UC_ACC_03``
   * - **Implementación**
     - ``apps/access/`` (alias accessService)
   * - **TEST**
     - TST-fr-078-XX (pendiente — alta prioridad por
       impacto en RBAC)
   * - **Iniciativa origen**
     - documentar-ucs-implementados-no-declarados
