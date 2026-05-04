.. _arq-mod-001-componentes:

==============================================
ARQ_MOD_001 — Componentes Tecnicos
==============================================

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
   - Contiene vistas de login, logout, modelos de sesion

----

Modelos de Datos
================

- **DSC_MOD_001_User** - Usuario del sistema (referencia)
- **DSC_MOD_004_Session** - Sesion activa en base de datos

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

----

APIs Expuestas
==============

**API_001_Auth_Endpoints**

.. list-table::
 :widths: 15 35 50
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - POST
   - /api/v1/auth/login
   - Iniciar sesion
 * - POST
   - /api/v1/auth/logout
   - Cerrar sesion
 * - POST
   - /api/v1/auth/refresh
   - Renovar token
 * - POST
   - /api/v1/auth/password/recovery
   - Recuperar contrasena
 * - PUT
   - /api/v1/auth/password/change
   - Cambiar contrasena
 * - GET
   - /api/v1/auth/sessions
   - Listar sesiones activas
 * - DELETE
   - /api/v1/auth/sessions/{id}
   - Cerrar sesion especifica

----

Middleware
==========

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

----

Seguridad
=========

Validaciones Obligatorias
--------------------------

- Contraseña hasheada con algoritmo de hash de contraseña
- Token de autenticación firmado con algoritmo de firma simétrica, expiración 1 hora
- Refresh token con expiracion 24 horas
- Validacion de IP en cada request
- Validacion de User-Agent en cada request

Ataques Mitigados
-----------------

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Ataque
   - Mitigacion
 * - Brute Force
   - Rate limiting en login (5 intentos/minuto)
 * - Session Hijacking
   - Validacion IP + User-Agent
 * - Token Theft
   - Blacklist de tokens, sesion unica
 * - CSRF
   - Tokens de autenticación (no cookies de sesión)

----

Metricas y Monitoreo
====================

.. list-table::
 :widths: 40 30 30
 :header-rows: 1

 * - Metrica
   - Tipo
   - Umbral Alerta
 * - Logins exitosos/hora
   - Counter
   - N/A (informativo)
 * - Logins fallidos/hora
   - Counter
   - > 100 (posible ataque)
 * - Sesiones activas
   - Gauge
   - > 500 (capacidad)
 * - Tiempo de respuesta login
   - Histogram
   - > 2s (degradacion)
