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

.. code-block:: python

 class Role(models.Model):
     code = models.CharField(max_length=50, unique=True)  # R001, R002...
     name = models.CharField(max_length=100)
     category = models.CharField(max_length=50)  # OPERATIVO, GESTION, ADMIN
     permissions = models.ManyToManyField('Permission')
     is_active = models.BooleanField(default=True)

 class Permission(models.Model):
     code = models.CharField(max_length=100)  # reports.view, users.create
     module = models.CharField(max_length=50)
     action = models.CharField(max_length=50)

 class DataSegment(models.Model):
     code = models.CharField(max_length=50)
     segment_type = models.CharField  # CENTRO, SERVICIO, REGION
     value = models.CharField(max_length=100)

 class UserRole(models.Model):
     user = models.ForeignKey(User)
     role = models.ForeignKey(Role)
     assigned_at = models.DateTimeField(auto_now_add=True)
     assigned_by = models.ForeignKey(User, related_name='assignments')

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
