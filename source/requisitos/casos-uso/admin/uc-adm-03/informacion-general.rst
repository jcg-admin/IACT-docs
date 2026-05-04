.. _uc-adm-03-parte-01:

============================================
Parte 1 — Informacion general de UC_ADM_03
============================================

1.1 Identificacion
==================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID UC**
   - UC_ADM_03
 * - **Nombre**
   - Gestionar Catalogo de Agrupadores del Sistema
 * - **Version spec**
   - 1.0.0
 * - **Modulo**
   - MOD_Admin

1.2 Proposito
=============

UC_ADM_03 gestiona la composicion de los **12 agrupadores predefinidos
del sistema** (AGR-001..012). A diferencia de UC_PERM_05 (crear grupos
custom), este UC modifica los AGR de sistema — inmutables para
operadores, mutables solo por ``admin_sistema``.

Los AGR de sistema son la configuracion base que determina que
funciones tiene cada rol predefinido. Su modificacion es una operacion
de configuracion del modelo, no de asignacion a usuarios.

1.3 Alcance
===========

1.3.1 IN
--------

- **Modificar composicion** de AGR de sistema: agregar o remover
  funciones atomicas del catalogo a un AGR-NNN existente
  (``assign_functions_to_group``, scope AGR-001..012).
- **Ver composicion** actual de un AGR de sistema.
- **Ver impacto**: que usuarios tienen el AGR y cuales funciones
  efectivas cambiarian (vista informativa, sin cambiar asignaciones).

1.3.2 OUT
---------

- Cambios en composicion de AGR afectan el effective_set de todos
  los usuarios que tienen el AGR asignado (MOD_Permissions recalcula).
- Operacion auditada con alta criticidad (MOD_Audit).
- No se crean ni eliminan AGR de sistema — solo se modifica
  su composicion.

1.3.3 Posicion en el flujo
--------------------------

UC_ADM_03 es configuracion del modelo RBAC — modifica que funciones
incluye cada AGR predefinido, no quien tiene asignado el AGR
(eso es MOD_Access).

1.4 Trazabilidad inicial
========================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **CNST**
   - CNST-029 (modelo RBAC — 12 grupos predefinidos)
 * - **Funciones RBAC**
   - ``assign_functions_to_group``
     (scope: AGR-001..012, solo ``admin_sistema``)
 * - **AGR actor**
   - AGR-009 (admin_sistema — unico actor autorizado para AGR sistema)
 * - **UCs relacionados**
   - UC_PERM_05 (crea grupos custom — diferente scope),
     UC_PERM_06 (modifica grupos custom),
     UC_PERM_01 (effective_set — consume composicion del AGR),
     UC_ACC_01/02 (asigna/revoca AGR a usuarios)
 * - **Clase primaria**
   - ``FunctionGroup`` (AGR de sistema, is_system=True)

.. seealso::

 :doc:`/arquitectura-tecnica/uc-module-view/mod-admin`
 :doc:`/requisitos/reglas-negocio/br-006-rbac-flat-nist`
