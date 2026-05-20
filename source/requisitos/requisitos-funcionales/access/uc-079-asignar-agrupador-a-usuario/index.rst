.. _uc_079_asignar_agrupador_a_usuario:

==================================================
UC-079: Asignar Agrupador a Usuario
==================================================

.. note::

   UC documentado retroactivamente por la iniciativa
   ``documentar-ucs-implementados-no-declarados``. El
   marker ``UC_ACC_04`` ya existia en codigo
   (apps/access/) con la descripcion "Asignar
   agrupador a usuario" pero carecia de RST en docs.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-079
   * - **Marker código**
     - ``UC_ACC_04``
   * - **Nombre**
     - Asignar Agrupador a Usuario
   * - **Actor**
     - Admin
   * - **Módulo**
     - MOD_Access
   * - **Tipo**
     - Funcional / Admin

2. Especificación
-----------------

Endpoint admin que asigna un agrupador (categoria
organizativa, distinta de AccessGroup/grupo de permisos)
a un usuario. Cubre necesidades de reporting y filtros
por agrupador en dashboards.

Distinto de UC-012 (asignar AccessGroup): los
agrupadores no otorgan permisos, son metadata
organizativa.

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker código**
     - ``UC_ACC_04``
   * - **Implementación**
     - ``apps/access/``
   * - **TEST**
     - TST-fr-079-XX (pendiente)
   * - **Iniciativa origen**
     - documentar-ucs-implementados-no-declarados
