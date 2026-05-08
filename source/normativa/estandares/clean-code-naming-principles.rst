.. meta::
 :artefacto: CLEAN_CODE_NAMING_PRINCIPLES
 :tipo: Norma de Proyecto (Naming)
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _clean-code-naming-principles:

==================================================
CLEAN_CODE_NAMING_PRINCIPLES — Norma del Proyecto
==================================================

.. note::

 Este documento es la **autoridad normativa** de naming
 para el proyecto IACT-docs e IACT-backend. Los STDs
 particulares del corpus (STD-007, STD-008, STD-010,
 STD-013) y ``backend/conventions.rst`` v2.0.0 derivan
 de esta norma. Ante divergencia, prevalece este
 documento.

 La version markdown standalone en el repositorio raiz
 (``CLEAN_CODE_NAMING_PRINCIPLES.md``) y este artefacto
 RST son **equivalentes en contenido**; la version RST se
 mantiene para integracion con el toctree de Sphinx y
 cross-refs ``:doc:``.

.. contents:: Contenido
 :depth: 2

----

1. Principios fundamentales
============================

1.1 El nombre describe el rol en el dominio
--------------------------------------------

El nombre de una clase, metodo o variable debe permanecer
valido si el framework o la libreria de implementacion
cambian. El nombre **NO** debe contener:

- Marcas del framework (``Django``, ``DRF``, ``Vue``,
  ``React``).
- Sufijos que describen mecanismo tecnico de la base
  heredada (``Serializer``, ``ViewSet``, ``Backend``).
- Patrones GoF como sufijo cuando no expresan rol del
  dominio (``Factory``, ``Builder``, ``Manager``
  genericos).

1.2 Sufijos GoF como default prohibido
---------------------------------------

Los sufijos ``Factory``, ``Builder``, ``Manager``,
``Helper``, ``Util``, ``Utils``, ``Wrapper``, ``Provider``,
``Service`` (cuando es generico) estan prohibidos como
default. Son aceptables **solo** cuando:

- Expresan rol concreto del dominio
  (``UserOnboardingService``).
- El patron GoF se materializa con su semantica completa
  (``QueryBuilder`` con interfaz fluent
  ``.where().apply().order_by()`` real).
- Son API publica de un framework externo
  (``TransactionManager`` de Django ORM).

1.3 Naming de tests
--------------------

- Datos de prueba: sufijo ``TestData``
  (``UserTestData``, ``SessionTestData``).
- NO usar sufijo ``Factory`` para datos de tests.

1.4 Distincion produccion vs tests
-----------------------------------

Una clase de produccion con sufijo prohibido se renombra a
su rol del dominio (no a ``*TestData``). Casos historicos
del corpus (WP-E):

- ``EventFactory`` (uc-perm-09 produccion) →
  ``AuditEventCreator``.
- ``UserFactory`` (uc-usr-01 patrones produccion) →
  ``UserOnboardingService``.
- ``UserFactory`` (uc-auth-01 testing) → ``UserTestData``.

1.5 Identificadores en ingles
------------------------------

Toda clase, metodo, atributo y variable se nombra en
**ingles tecnico**. La narrativa de requisitos puede ser en
español (gobernada por STD-010); los identificadores no.

::

   ✓ find_recent(period)        ✗ ejecuciones_recientes()
   ✓ find_by_state(state)       ✗ por_estado(state)
   ✓ last_successful_by_dataset ✗ ultima_ejecucion()

1.6 Nombres canonicos prefijados sobre genericos
-------------------------------------------------

Cuando un identificador puede coincidir con uno de otra
clase, prefijar con el concepto especifico:

::

   ✓ rule_id        ✗ id (en AlertRule)
   ✓ view_id        ✗ id (en SavedView)
   ✓ subscription_id ✗ id (en Subscription)
   ✓ filters_snapshot ✗ filters
   ✓ owner_user_id  ✗ owner

----

2. Sufijos prohibidos por categoria
====================================

2.1 Sufijos de framework backend (Django/DRF)
----------------------------------------------

.. list-table::
 :widths: 25 25 50
 :header-rows: 1

 * - Sufijo
   - Origen
   - Reemplazo de dominio
 * - ``Serializer``
   - DRF ``ModelSerializer``
   - ``Contract`` o ``Representation``
 * - ``ViewSet``
   - DRF ``ModelViewSet``
   - ``Endpoints``
 * - ``View`` (cuando hereda de ``APIView``)
   - DRF
   - ``Endpoint``
 * - ``Permission`` (cuando hereda de ``BasePermission``)
   - DRF
   - ``AccessPolicy`` o ``RequirePolicy``
 * - ``Backend`` (auth)
   - Django auth ``BaseBackend``
   - ``AuthProvider``
 * - ``Manager`` (Django Manager generico)
   - Django ORM
   - ``Query`` o ``Repository``
 * - ``Middleware``
   - Django/WSGI
   - rol descriptivo

**Excepciones (preservar):**

- Bases externas: ``BasePermission``, ``BaseBackend``,
  ``ModelBackend``, ``APIView``, ``ModelSerializer``,
  ``ModelViewSet``, ``ReadOnlyModelViewSet``,
  ``TemplateView``, ``DjangoModelFactory``,
  ``SubFactory``.
- API publica framework: ``TransactionManager``
  (``transaction.atomic()``).
- ``QueryBuilder`` con interfaz fluent real.

2.2 Sufijos GoF
----------------

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Sufijo
   - Aplicabilidad
 * - ``Factory``
   - **Prohibido** salvo lib externa o "rol del dominio
     que ES factory"
 * - ``Builder`` (sin fluent real)
   - **Prohibido** — usar ``Assembler``
 * - ``Builder`` (con fluent real)
   - Permitido
 * - ``Manager`` (generico)
   - **Prohibido** — usar ``OperationsCoordinator`` o
     rol especifico
 * - ``Helper``, ``Util``, ``Utils``
   - **Prohibido** — nombrar el rol del dominio
 * - ``Wrapper``
   - **Prohibido** — describir el contrato

2.3 Domain-noun preservation (criterio D4)
-------------------------------------------

Si el sufijo prohibido es **noun nominal del dominio**
(no indica rol de framework), se preserva:

.. list-table::
 :widths: 30 20 50
 :header-rows: 1

 * - Clase
   - Sufijo
   - Razon de preservacion
 * - ``SavedView``
   - ``View``
   - "vista guardada" del reporte; entidad de dominio
 * - ``AuditEventView``
   - ``View``
   - CQRS read model (DTO), no DRF View
 * - ``ExceptionalPermission``
   - ``Permission``
   - Domain entity RBAC; "permission" es noun
 * - ``TemporaryPermission`` / ``DirectPermission``
   - ``Permission``
   - Domain entities RBAC
 * - ``StorageBackend`` / ``CacheBackend``
   - ``Backend``
   - Roles de infraestructura, no Django auth
 * - ``TransactionManager``
   - ``Manager``
   - API Django ORM publica

**Criterio operativo:**

#. ¿Extiende base del framework
   (``BasePermission``, ``BaseBackend``, ``APIView``)? →
   suffix prohibido aplica → renombrar.
#. ¿Es entidad de dominio cuyo concepto se llama asi en
   el negocio? → preservar.
#. ¿Es API publica de framework externo? → preservar.

----

3. Verbos canonicos en metodos
================================

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Operacion
   - Verbo canonico
   - NO usar
 * - Crear
   - ``create``, ``register``
   - ``make``, ``new``
 * - Listar
   - ``find``, ``find_by_*``, ``find_recent``
   - ``list``, ``query`` (excepto en repos)
 * - Obtener uno
   - ``get_by_id``, ``get``
   - ``retrieve``, ``fetch``
 * - Actualizar
   - ``update``, ``modify``
   - ``edit``, ``change``
 * - Eliminar logico
   - ``deactivate``
   - ``delete`` (reservado a fisico)
 * - Validar
   - ``validate_<aspecto>``
   - ``check`` (ambiguo)
 * - Verificar permiso
   - ``has_function``, ``is_authorized``
   - ``check_permission``

----

4. Cross-references al corpus
==============================

Esta norma es autoritativa; los siguientes documentos del
corpus la implementan o la concretan:

- :doc:`/backend/conventions` v2.0.0 — aplicacion al
  contexto Django/DRF. Implementa §2.1.
- :doc:`/normativa/estandares/std-007-convencion-naming` —
  naming general (kebab-case, snake_case).
- :doc:`/normativa/estandares/std-008-naming-identificadores` —
  prohibicion de acronimos opacos.
- :doc:`/normativa/estandares/std-010-vocabulario-abstracto`
  v1.3.0 — vocabulario abstracto en narrativa
  (complementa CLEAN_CODE para narrativa; CLEAN_CODE rige
  identifiers).
- :doc:`/normativa/estandares/std-013-rest-api-conventions` —
  URLs como recursos no acciones.

----

5. Implementacion historica
============================

Esta norma fue aplicada al corpus IACT-docs en los
siguientes WPs (commits trazables en el feature branch):

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - WP
   - Alcance
 * - ``clean-code-naming-audit``
   - Inventario inicial de violaciones
 * - ``naming-rules-resolution``
   - D1: alinear ``backend/conventions.rst`` v2.0.0 con
     §2.1
 * - WP-A (Sprint 1)
   - Renombrar archivos con prefijo numerico
 * - WP-B + WP-C (Sprint 2)
   - Limpiar ``SoD`` en narrativa y clases
 * - WP-E
   - Renombrar 13 clases con sufijos
     ``Factory/Builder/Manager``
 * - WP-F
   - Renombrar 22 clases con sufijos
     ``Serializer/ViewSet/View/Permission/Backend``
 * - WP-G
   - Aplicar STD-010 vocabulario abstracto
 * - WP-H (Sprint 1)
   - ``ReportFactory`` → ``ReportTypeRegistry``
 * - TD-D5 / TD-D6
   - Ampliar STD-010 §2.5 con exenciones de scope
 * - ``uc-view-domain-alignment``
   - Cross-ref UCs↔domain-model + 3 UCs nuevos

Cada WP documenta sus decisiones en
``.thyrox/context/work/<WP>/track/``.

----

6. Aplicacion del criterio en revisiones
==========================================

Cuando se introduzca una clase nueva o se modifique una
existente, el revisor debe responder:

#. ¿El nombre describe el **rol del dominio** o el
   mecanismo del framework? Solo el rol.
#. ¿El nombre permaneceria valido si se cambia
   DRF/Django/React? Si no, renombrar.
#. ¿El sufijo es **noun de dominio** o sufijo de
   framework? Si es framework (extiende base), aplicar
   tabla §2.1.
#. ¿El identificador es generico (``id``, ``state``)
   cuando debe ser canonico (``view_id``, ``status``)?
   Aplicar §1.6.
#. ¿El identificador esta en español? Traducir a ingles
   tecnico.

----

7. Historial
=============

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Version
   - Fecha
   - Cambios
 * - 1.0.0
   - 2026-05-08
   - Documento canonico standalone — consolidacion de la
     norma aplicada al corpus IACT-docs en los WPs A-H,
     TD-D5/D6 y uc-view-domain-alignment. Reemplaza la
     transmision oral de la norma con un artefacto
     consultable.
