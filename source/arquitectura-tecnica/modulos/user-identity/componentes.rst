.. _arq-mod-002-componentes:

================================================
ARQ_MOD_002 — Componentes Tecnicos
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
 * - apps.users
   - Modelos User, SecurityQuestion, vistas de gestion

----

Modelos de Datos
================

**DSC_MOD_001_User** — Usuario del sistema

.. code-block:: python

 class User(AbstractBaseUser):
     username = models.CharField(max_length=50, unique=True)
     first_name = models.CharField(max_length=100)
     last_name = models.CharField(max_length=100)
     organizational_unit = models.CharField(max_length=100)
     status = models.CharField(choices=USER_STATUS_CHOICES)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     deleted_at = models.DateTimeField(null=True, blank=True)
     deleted_by = models.ForeignKey('self', null=True)

 class SecurityQuestion(models.Model):
     user = models.ForeignKey(User)
     question = models.CharField(max_length=200)
     answer_hash = models.CharField(max_length=128)

----

APIs Expuestas
==============

**API_002_Users_Endpoints**

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - POST
   - /api/v1/users
   - Crear usuario
 * - GET
   - /api/v1/users/{id}
   - Obtener usuario
 * - PUT
   - /api/v1/users/{id}
   - Actualizar usuario
 * - DELETE
   - /api/v1/users/{id}
   - Baja logica
 * - GET
   - /api/v1/users/{id}/profile
   - Perfil completo
 * - PUT
   - /api/v1/users/{id}/security-questions
   - Gestionar preguntas
