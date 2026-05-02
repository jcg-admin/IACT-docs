.. _arq-mod-008-dependencias:

==================================
ARQ_MOD_008 — Dependencias
==================================


Depende de
==========

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-001`
   - Requiere sesion (solo para UI de logs)
 * - :ref:`arq-mod-003`
   - Verifica permisos de ver logs tecnicos

----

Es Requerido por
================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - TODOS
   - Todos los modulos generan logs tecnicos
 * - :ref:`arq-mod-006`
   - Puede generar alertas por health degradado
