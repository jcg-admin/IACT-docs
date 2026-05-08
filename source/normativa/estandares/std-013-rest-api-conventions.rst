.. meta::
 :artefacto: STD_013
 :tipo: Estandar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _std-013:

==================================================
STD-013 — REST API Conventions (URLs y verbos)
==================================================

Convenciones de diseño de URLs para los endpoints del backend
IACT, basadas en OpenAPI 3.0 / OAS3 y RFC 3986.

Regla principal
===============

**URLs son recursos, no acciones.**

::

   ✅  POST   /api/access/function-assignments        ← sustantivo
   ✅  DELETE /api/access/function-assignments/{id}   ← sustantivo + HTTP method
   ✅  POST   /api/access/separation-rules/validate   ← recurso + sub-acción

   ❌  POST   /api/access/functions/assign            ← verbo en path
   ❌  POST   /api/access/validate-pii                ← verbo + acrónimo
   ❌  GET    /api/access/revoke-permissions          ← verbo en path

Estructura de URL base (OAS3)
=============================

::

   https://api.example.com/v1/users?role=admin
   \______________________/\__/\___/\________/
          server URL       ver  recurso  query params

El servidor base se declara en ``REACT_APP_API_URL``. Todos los
paths son relativos a esa base.

Convenciones de naming para paths
=================================

Sustantivos en plural para colecciones
--------------------------------------

::

   GET  /access/functions              ← lista de funciones
   GET  /access/functions/{id}         ← función individual
   POST /access/functions              ← crear función

Kebab-case para recursos multi-palabra
--------------------------------------

::

   ✅  /access/separation-rules
   ✅  /access/function-assignments
   ✅  /access/function-groups
   ❌  /access/separationRules         ← camelCase no aplica a URLs
   ❌  /access/separation_rules        ← snake_case no es estándar web

Sin acrónimos de dominio en paths
---------------------------------

Las mismas reglas de naming que para identificadores de código
(STD-008) aplican a los paths de URL:

::

   ✅  /access/separation-rules/validate
   ❌  /access/validate-pii
   ❌  /access/etl-jobs

Acciones no-CRUD: sub-recursos o verbo calificador
---------------------------------------------------

Para operaciones que no son CRUD puro, usar un sub-recurso o un
verbo calificador como último segmento:

::

   ✅  POST /access/separation-rules/validate    ← validar reglas
   ✅  POST /access/audit-exports                ← crear una exportación
   ✅  POST /access/sessions/revoke              ← revocar sesiones activas

HTTP method expresa la acción
=============================

.. list-table::
 :widths: 30 25 45
 :header-rows: 1

 * - Acción
   - HTTP Method
   - Ejemplo
 * - Crear
   - ``POST``
   - ``POST /access/function-assignments``
 * - Leer lista
   - ``GET``
   - ``GET /access/functions``
 * - Leer uno
   - ``GET``
   - ``GET /access/functions/{id}``
 * - Actualizar completo
   - ``PUT``
   - ``PUT /access/functions/{id}``
 * - Actualizar parcial
   - ``PATCH``
   - ``PATCH /access/functions/{id}``
 * - Eliminar
   - ``DELETE``
   - ``DELETE /access/function-assignments/{id}``

Mapa de URLs canónicas — módulo Access
======================================

.. list-table::
 :widths: 25 25 25 10
 :header-rows: 1

 * - Operación
   - URL anterior (incorrecta)
   - URL canónica (IACT-docs)
   - Estado
 * - Validar identificador PII
   - ``POST /access/validate-pii``
   - ``POST /access/separation-rules/validate``
   - Corregido
 * - Asignar funciones a usuario (bulk)
   - ``POST /access/functions/assign``
   - ``POST /users/{userId}/functions/``
   - Corregido (TD-ACC-01)
 * - Revocar funciones de usuario (bulk)
   - ``POST /access/functions/revoke``
   - ``DELETE /users/{userId}/functions/``
   - Corregido (TD-ACC-02)
 * - Exportar auditoría (async)
   - ``POST /access/audit/export`` → blob
   - ``POST /audit/export/`` → ``202 + {job_id}``
   - Corregido (TD-ACC-03)
 * - Asignar grupo de acceso (AGR)
   - ``POST /access/function-groups/assign``
   - ``POST /users/{userId}/access-groups/``
   - Corregido (TD-ACC-04)
 * - Asignar segmento a usuario
   - ``POST /access/segments/assign``
   - ``PATCH /users/{userId}/`` con body ``{segment_id}``
     (canónico — el segmento es atributo del User per
     :doc:`/requisitos/casos-uso/users/uc-usr-03/index`)
   - Corregido (TD-ACC-05)

Las URLs canónicas de TD-ACC-01..05 están verificadas con los
diagramas de secuencia UML de UC_ACC_01, UC_ACC_02, UC_ACC_04,
UC_AUD_03 y UC_USR_03 en IACT-docs.

.. note:: TD-ACC-05 — Asignación de segmento

 La asignación de segmento NO es un endpoint separado en
 ``/access/``: el segmento es **atributo del User** (BR-012:
 cada usuario tiene segmento único, ver
 :doc:`/requisitos/reglas-negocio/br-012-usuario-segmento-unico`).
 Por lo tanto la operación canónica es ``PATCH /users/{userId}/``
 con ``{segment_id}`` en el body (mismo endpoint de
 modificación general del User, UC_USR_03). NO crear un
 endpoint ``/access/segments/assign`` — sería duplicación de
 estado y violación de la regla "URLs son recursos, no
 acciones".

Query parameters
================

Los filtros y la paginación van como query params, **nunca en el
path**:

::

   ✅  GET /access/functions?category=audit&state=active
   ✅  GET /users?state=ACTIVE&page=2&limit=25
   ❌  GET /access/functions/active            ← estado como path segment
   ❌  GET /users/state/ACTIVE                 ← filtro como path segment

Versionado
==========

El prefijo de versión va en el servidor base (``/api/v1/``), no
en cada path:

::

   ✅  server: https://api.example.com/v1
       path:   /access/functions

   ❌  path:   /v1/access/functions    ← versión repetida en cada path

Trazabilidad
============

Esta convención es referenciada por:

- :doc:`/normativa/estandares/std-007-convencion-naming` — naming
  general (kebab-case en paths se alinea con kebab-case en
  filenames).
- :doc:`/normativa/estandares/std-008-naming-identificadores` —
  identifiers en código (mismas reglas de naming aplican a paths).
- :doc:`/normativa/estandares/std-010-vocabulario-abstracto` —
  prohibición de acrónimos de dominio (``etl``, ``pii``) en
  identifiers públicos.
- :doc:`/backend/conventions` — convenciones backend específicas.

Referencias externas
====================

- OpenAPI 3.0 Server Object:
  https://spec.openapis.org/oas/v3.0.3#server-object
- RFC 3986 — Uniform Resource Identifier (URI): Generic Syntax.
- REST API Design Best Practices (Roy Fielding, 2000).
