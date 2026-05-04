.. _uc-adm-02-parte-01:

============================================
Parte 1 — Informacion general de UC_ADM_02
============================================

1.1 Identificacion
==================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID UC**
   - UC_ADM_02
 * - **Nombre**
   - Gestionar Catalogo de Funciones
 * - **Version spec**
   - 1.0.0
 * - **Modulo**
   - MOD_Admin

1.2 Proposito
=============

UC_ADM_02 gestiona el **catalogo de funciones atomicas** del sistema
RBAC. Las 74+ funciones actuales se administran via migraciones Django
— no existe mecanismo de UI para agregar, desactivar o modificar
funciones sin despliegue de codigo. Este UC formaliza esa capacidad.

1.3 Alcance
===========

1.3.1 IN
--------

- **Crear** nueva funcion atomica: nombre (codename), descripcion,
  scope, modulo, estado activo.
- **Actualizar** descripcion o metadata de funcion existente.
- **Desactivar** funcion: estado activo → inactivo (no DELETE — puede
  haber asignaciones historicas).
- **Listar/Ver** funciones del catalogo con filtros por modulo,
  estado, scope.

1.3.2 OUT
---------

- Funciones activas consumidas por MOD_Permissions para construir
  effective_set y menu dinamico.
- Cambios auditados (MOD_Audit, alta criticidad).
- Requiere migracion de datos para persistencia estructural.

1.3.3 Posicion en el flujo
--------------------------

UC_ADM_02 modifica el modelo base del RBAC — la definicion de que
funciones existen. Opera antes que cualquier asignacion (MOD_Access)
o verificacion (MOD_Permissions).

1.4 Trazabilidad inicial
========================

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **CNST**
   - CNST-029 (modelo RBAC Flat — 74+ funciones atomicas)
 * - **Funciones RBAC**
   - ``manage_function_catalog`` (NUEVA v5.6.0)
 * - **AGR actor**
   - AGR-009 (admin_sistema — unico actor autorizado)
 * - **UCs relacionados**
   - UC_PERM_01 (effective_set — consume catalogo),
     UC_ADM_01 (SoD referencia funciones del catalogo)
 * - **Clase primaria**
   - ``Function`` (modelo Django)

.. seealso::

 :doc:`/arquitectura-tecnica/use-case-view/mod-admin`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/catalogo-funciones`
