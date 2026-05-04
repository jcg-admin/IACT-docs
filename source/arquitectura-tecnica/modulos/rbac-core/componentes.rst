.. _arq-mod-003-componentes:

================================================
ARQ_MOD_003 — Componentes Tecnicos
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
 * - apps.common.permissions
   - Logica RBAC, enforcers, calculadores

----

Modelos de Datos
================

- **DSC_MOD_002_Role** — Roles funcionales
- **DSC_MOD_003_Permission** — Permisos del sistema

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
----

APIs Expuestas
==============

**API_003_RBAC_Endpoints**

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - GET
   - /api/v1/roles
   - Listar roles
 * - POST
   - /api/v1/roles
   - Crear rol
 * - GET
   - /api/v1/users/{id}/permissions
   - Permisos efectivos
 * - POST
   - /api/v1/users/{id}/roles
   - Asignar rol
 * - DELETE
   - /api/v1/users/{id}/roles/{roleId}
   - Retirar rol
 * - GET
   - /api/v1/users/{id}/simulate
   - Simular acceso
 * - GET
   - /api/v1/rbac/matrix
   - Matriz consolidada
