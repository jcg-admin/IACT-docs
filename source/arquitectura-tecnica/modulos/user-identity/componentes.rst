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

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

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
