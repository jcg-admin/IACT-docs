.. _arq-mod-002-dependencias:

==================================
ARQ_MOD_002 — Dependencias
==================================


Depende de
==========

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-003`
   - Para mostrar roles en perfil (solo lectura)

----

Es Requerido por
================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-001`
   - Valida que usuario existe y esta activo
 * - :ref:`arq-mod-003`
   - Calcula permisos sobre el usuario
 * - :ref:`arq-mod-007`
   - Registra cambios en usuarios
