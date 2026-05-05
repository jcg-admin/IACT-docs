.. _arq-mod-007-componentes:

================================================
ARQ_MOD_007 — Componentes Tecnicos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Componentes de Aplicacion
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Descripcion
 * - apps.common.audit
   - Modelo AuditLog, decoradores, servicios

----

Modelos de Datos
================

**DSC_MOD_008_AuditLog** — Registro de auditoria

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

----

Tipos de Accion Auditada
=========================

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Accion
   - Descripcion
   - Modulo Origen
 * - AUTH_LOGIN
   - Inicio de sesion exitoso
   - :ref:`arq-mod-001`
 * - AUTH_LOGOUT
   - Cierre de sesion
   - :ref:`arq-mod-001`
 * - AUTH_FAILED
   - Intento de login fallido
   - :ref:`arq-mod-001`
 * - USER_CREATE
   - Creacion de usuario
   - :ref:`arq-mod-002`
 * - USER_UPDATE
   - Modificacion de usuario
   - :ref:`arq-mod-002`
 * - USER_DELETE
   - Baja logica de usuario
   - :ref:`arq-mod-002`
 * - ROLE_ASSIGN
   - Asignacion de rol
   - :ref:`arq-mod-003`
 * - ROLE_REVOKE
   - Retiro de rol
   - :ref:`arq-mod-003`
 * - PERMISSION_GRANT
   - Permiso directo asignado
   - :ref:`arq-mod-003`
 * - REPORT_EXPORT
   - Exportacion de reporte
   - :ref:`arq-mod-005`
 * - ALERT_CREATE
   - Configuracion de alerta
   - :ref:`arq-mod-006`
 * - PASSWORD_CHANGE
   - Cambio de contrasena
   - :ref:`arq-mod-001`

----

Decorador de Auditoria
=======================

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

----

APIs Expuestas
==============

**API_008_Audit_Endpoints**

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - GET
   - /api/v1/audit/logs
   - Listar eventos (paginado)
 * - GET
   - /api/v1/audit/logs/{id}
   - Detalle de evento
 * - POST
   - /api/v1/audit/export
   - Exportar a CSV/Excel
 * - GET
   - /api/v1/audit/reports/permissions
   - Reporte de cambios de permisos
