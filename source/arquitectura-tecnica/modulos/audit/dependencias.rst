.. _arq-mod-007-dependencias:

==================================
ARQ_MOD_007 — Dependencias
==================================


Depende de
==========

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-001`
   - Requiere sesion para identificar usuario
 * - :ref:`arq-mod-003`
   - Verifica permisos de ver auditoria (R017)

----

Es Requerido por
================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-001`
   - Registra login/logout
 * - :ref:`arq-mod-002`
   - Registra cambios de usuarios
 * - :ref:`arq-mod-003`
   - Registra cambios de roles/permisos
 * - :ref:`arq-mod-005`
   - Registra exportaciones
 * - :ref:`arq-mod-006`
   - Registra configuracion de alertas
