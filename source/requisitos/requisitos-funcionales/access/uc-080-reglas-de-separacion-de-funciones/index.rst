.. _uc_080_reglas_de_separacion_de_funciones:

=====================================================
UC-080: Gestionar Reglas de Separación de Funciones
=====================================================

.. note::

   UC documentado retroactivamente por la iniciativa
   ``documentar-ucs-implementados-no-declarados``. El
   marker ``UC_ACC_05`` ya existia en codigo
   (apps/access/) con la descripcion "Reglas de
   Separacion de Funciones" pero carecia de RST en
   docs.

1. Identificación
-----------------

.. list-table::
   :widths: 25 75

   * - **ID**
     - UC-080
   * - **Marker código**
     - ``UC_ACC_05``
   * - **Nombre**
     - Gestionar Reglas de Separación de Funciones
   * - **Actor**
     - Admin / Compliance
   * - **Módulo**
     - MOD_Access
   * - **Tipo**
     - Funcional / Admin / Compliance

2. Especificación
-----------------

CRUD de reglas que declaran pares de funciones
incompatibles (separation of duties). Una regla
``{funcion_A, funcion_B}`` significa que ningun usuario
puede tener asignadas simultaneamente ambas funciones.

Las reglas se validan en:

* UC-010 / UC_ACC_01 al asignar nueva funcion (rechaza
  si conflicto).
* UC-012 / UC_PERM_01 al asignar AccessGroup (rechaza
  si el grupo contiene una funcion en conflicto con la
  existente del usuario).

Endpoints:

* GET /api/access/separation-rules/
* POST /api/access/separation-rules/
* GET /api/access/separation-rules/{id}/
* PATCH /api/access/separation-rules/{id}/
* DELETE /api/access/separation-rules/{id}/

3. Trazabilidad
---------------

.. list-table::
   :widths: 20 80

   * - **Marker código**
     - ``UC_ACC_05``
   * - **Implementación**
     - ``apps/access/`` views SeparationRule*
   * - **TEST**
     - TST-fr-080-XX (pendiente)
   * - **Iniciativa origen**
     - documentar-ucs-implementados-no-declarados
   * - **CNST**
     - CNST-COMPLIANCE (separation of duties)
