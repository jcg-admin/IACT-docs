.. _uc-auth-01-parte-11:

==================================
Parte 11 — Implementacion tecnica
==================================

Referencia tecnica para la fase de
implementacion del UC. Stack canonico,
estructura de archivos backend / frontend,
endpoints, modelos. Las cifras concretas (TTL
de tokens, costo de hash, limites de
throttling) viven en los CNST y futuros ADRs
de implementacion, no aqui.

11.1 Stack tecnologico
======================

Per ADR-DEVOPS-001 (stack canonico del
proyecto) y CNST-021 (Ubuntu + Apache +
mod_wsgi):

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Backend framework**
   - Django + Django REST Framework (DRF)
 * - **Lenguaje**
   - Python 3.x
 * - **Web server**
   - Apache 2.4 + mod_wsgi (CNST-021)
 * - **Base de datos**
   - MySQL 8.0 InnoDB
 * - **Autenticacion**
   - DRF SimpleJWT (CNST-009)
 * - **Hashing**
   - algoritmo de hash (libreria de la plataforma o
     ``passlib``)
 * - **Cache**
   - Django DatabaseCache (no Redis ni
     Memcached — explicitamente fuera del
     stack)
 * - **Frontend framework**
   - React 18
 * - **State management**
   - Redux Toolkit
 * - **Build**
   - Webpack
 * - **HTTP client**
   - axios

Stack **prohibido** en este UC (per ADR-DEVOPS-001):

- Docker / Kubernetes — no.
- Nginx — no (Apache + mod_wsgi).
- Gunicorn / uWSGI — no.
- Celery — no (no necesario aqui; la
  notificacion via InternalMailbox es sincrona
  o cron-driven).
- Redis / Memcached — no (DatabaseCache).
- PostgreSQL — no (MySQL).

11.2 Endpoint
=============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Method**
   - POST
 * - **URL**
   - ``/api/auth/login/``
 * - **Authentication**
   - publico (sin token)
 * - **Throttling**
   - ``AnonRateThrottle`` + ``UserRateThrottle``
     (CNST-011)
 * - **View class**
   - ``LoginEndpoint(APIView)``

11.3 Estructura de archivos backend
===================================

Ubicacion canonica del codigo (CNST-022
estructura de directorios):

::

   backend/
   └── apps/
       └── auth_app/
           ├── __init__.py
           ├── apps.py                       # AppConfig
           ├── urls.py                       # POST /api/auth/login/
           ├── views.py                      # LoginEndpoint, LogoutEndpoint, ...
           ├── serializers.py                # LoginRequestContract
           ├── services.py                   # AuthService.authenticate()
           ├── strategies.py                 # AuthenticationStrategy +
           │                                 # LocalPasswordStrategy
           ├── throttles.py                  # AnonLoginThrottle, UserLoginThrottle
           ├── exceptions.py                 # InvalidCredentials,
           │                                 # AccountBlocked, etc.
           ├── audit.py                      # @audits decorator + emit functions
           ├── tests/
           │   ├── __init__.py
           │   ├── test_login_view.py        # CA-01..CA-16
           │   ├── test_serializer.py
           │   ├── test_service.py
           │   └── test_strategies.py
           └── README.rst

Archivos en otras apps que UC_AUTH_01 toca:

::

   backend/apps/users/models.py             # class User
   backend/apps/sessions/models.py          # class Session
   backend/apps/audit/models.py             # class AuditEvent
   backend/apps/mailbox/models.py           # class InternalMailbox
   backend/apps/audit/middleware.py         # AuditEmitter middleware

11.4 Modelo Django de Session (extracto)
========================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.5 LoginEndpoint (esqueleto)
================================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.6 AuthService (esqueleto)
============================

.. note::

 Los detalles de implementacion de este requisito estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.

11.7 Frontend (React)
=====================

Estructura de archivos:

::

   frontend/src/
   └── features/
       └── auth/
           ├── LoginPage.jsx                # pagina /login
           ├── LoginForm.jsx                # componente formulario
           ├── authSlice.js                 # Redux slice
           ├── authApi.js                   # axios calls
           ├── selectors.js
           └── tests/
               ├── LoginPage.test.jsx
               └── LoginForm.test.jsx

LoginForm responsabilidades:

- Renderizar dos campos (username, password)
  con validacion cliente-side basica.
- Submit via ``authApi.login()``.
- Manejar respuestas 200 / 4xx / 5xx con
  feedback visible al usuario.
- Redirigir tras exito segun ``next_step``:

  - ``null`` → ``/`` (landing por AccessGroup)
  - ``"change_password"`` → ``/change-password``

11.8 Toctree de la spec
=======================

Este archivo es la **Parte 11** del spec de
12 partes de UC_AUTH_01:

- :doc:`index`
- :doc:`informacion-general`
- :doc:`actores-precondiciones`
- :doc:`flujo-principal`
- :doc:`flujos-alternos`
- :doc:`excepciones`
- :doc:`requisitos-no-funcionales`
- :doc:`datos-involucrados`
- :doc:`diagramas-uml/index`
- :doc:`criterios-aceptacion`
- :doc:`patrones-diseno`
- :doc:`testing`
