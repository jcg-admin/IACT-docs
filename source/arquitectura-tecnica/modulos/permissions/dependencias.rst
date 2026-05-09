.. _arq-mod-003-dependencias:

==================================
ARQ_MOD_003 — Dependencias
==================================


Depende de
==========

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-002`
   - Necesita datos del usuario para calcular permisos
 * - :ref:`arq-mod-001`
   - Necesita sesion valida

----

Es Requerido por
================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-005`
   - Consulta permisos para mostrar/ocultar dashboards
 * - :ref:`arq-mod-006`
   - Consulta permisos para configurar alertas
 * - :ref:`arq-mod-007`
   - Registra cambios de roles/permisos
 * - TODOS
   - Todos los modulos consultan permisos
