.. _uc-adm-01-parte-01:

============================================
Parte 1 — Informacion general de UC_ADM_01
============================================

1.1 Identificacion
==================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID UC**
   - UC_ADM_01
 * - **Nombre**
   - Gestionar Ciclo de Vida de Reglas de Separacion
 * - **Version spec**
   - 1.0.0
 * - **Modulo**
   - MOD_Admin

1.2 Proposito
=============

UC_ADM_01 administra el ciclo de vida completo de las **reglas de separacion**:
crear, actualizar parametros y activar/desactivar. Diferencia con
UC_ACC_05 (vista operativa de reglas): este UC gestiona el modelo —
que reglas EXISTEN — mientras UC_ACC_05 cubre la consulta/vista
de las reglas vigentes para operadores.

Las tres reglas estaticas actuales (SOD-001..003, CNST-030) fueron
definidas en migraciones. UC_ADM_01 es el mecanismo formal para
agregar una 4a regla o modificar las existentes desde la aplicacion.

1.3 Alcance
===========

1.3.1 IN
--------

- **Crear** nueva regla de separacion (``create_separation_rule``): declarar
  par de conjuntos de funciones mutuamente excluyentes, nombre,
  descripcion, scope.
- **Actualizar** parametros de regla existente
  (``update_separation_rule``): display_name, descripcion,
  conjuntos de funciones.
- **Activar/Desactivar** regla (``disable_separation_rule``):
  toggle ACTIVE ↔ INACTIVE.
- **Ver** reglas (``view_separation_rules``): listado con estado.

1.3.2 OUT
---------

- Cambios auditados automaticamente (MOD_Audit, alta criticidad).
- Reglas activas consumidas por UC_ACC_01, UC_ACC_04, UC_PERM_03
  para enforcement en write-time.

1.3.3 Posicion en el flujo
--------------------------

UC_ADM_01 es operacion de configuracion critica — modifica el modelo
RBAC, no asignaciones. Requiere AGR-010 (system_admin). Toda
modificacion genera notificacion a stakeholders de seguridad.

1.4 Trazabilidad inicial
========================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Reglas**
   - BR-007 Separacion de Funciones (separation of duties)
 * - **CNST**
   - CNST-029 (modelo RBAC), CNST-030 (reglas de separacion estaticas)
 * - **Funciones RBAC**
   - ``view_separation_rules``,
     ``create_separation_rule`` (NUEVA v5.6.0),
     ``update_separation_rule``,
     ``disable_separation_rule``
 * - **AGR actor**
   - AGR-010 (system_admin — unico actor autorizado)
 * - **UCs relacionados**
   - UC_ACC_05 (vista operativa),
     UC_ACC_01/04/PERM_03 (consumidores de enforcement)
 * - **Clase primaria**
   - ``SeparationRule``

.. seealso::

 :doc:`/arquitectura-tecnica/use-case-view/admin/index`
 :doc:`/requisitos/reglas-negocio/br-007-separacion-de-funciones`
