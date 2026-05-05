.. _arq-mod-001-dependencias:

=================================
ARQ_MOD_001 — Dependencias
=================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Depende de
==========

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-002`
   - Necesita validar que el usuario existe y esta activo
 * - :ref:`arq-mod-003`
   - Consulta roles basicos para incluir en claims del token

----

Es Requerido por
================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Modulo
   - Razon
 * - :ref:`arq-mod-003`
   - Necesita sesion valida para calcular permisos
 * - :ref:`arq-mod-005`
   - Requiere autenticacion para acceder
 * - :ref:`arq-mod-006`
   - Requiere autenticacion para ver notificaciones
 * - :ref:`arq-mod-007`
   - Registra eventos de login/logout
 * - TODOS
   - Todos los modulos requieren sesion autenticada
