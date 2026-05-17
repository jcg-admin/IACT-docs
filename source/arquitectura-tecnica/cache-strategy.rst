.. meta::
 :artefacto: CACHE_STRATEGY
 :tipo: Decision Tecnica
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno

==============================================
Estrategia de Cache — Capabilities y MenuItems
==============================================

Decisiones tecnicas concretas sobre el motor de cache,
configuracion y operacion. Complementa
:doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
y :doc:`/backend/adr-back-010-function-is-critical-governance`.

.. note::

   Este documento contiene decisiones de **implementacion
   tecnica**. La narrativa UC vive en
   ``source/requisitos/`` y usa los terminos canonicos
   STD-010 ("el servicio de cache", no "Redis").

----

1. Motor de cache
=================

**Decision:** Redis 7.x como motor de cache distribuido.

**Razones:**

- Latencia P95 ≤ 5ms para GET en network local.
- Soporte nativo para TTL por key.
- Cluster mode disponible para HA.
- Soporte estable en ``django-redis`` (cliente canonico).

**Alternativas descartadas:**

- **Memcached:** sin persistencia opcional, sin tipos
  estructurados, ecosystem mas chico para Python/Django.
- **Cache de Django local (LocMem):** no comparte estado
  entre workers; invalidacion no propaga.

----

2. Configuracion canonica
=========================

2.1 settings.py
---------------

.. code-block:: python

   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": env("REDIS_URL", default="redis://redis:6379/1"),
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
               "SOCKET_CONNECT_TIMEOUT": 0.5,  # segundos
               "SOCKET_TIMEOUT": 0.5,
               "RETRY_ON_TIMEOUT": False,    # NO reintentar (degraded mode)
               "IGNORE_EXCEPTIONS": False,    # exponemos exception para log
           },
           "TIMEOUT": 300,  # default TTL — capabilities
           "KEY_PREFIX": env("CACHE_KEY_PREFIX", default="iact"),
       }
   }

2.2 Key namespace
-----------------

.. list-table::
 :widths: 35 30 35
 :header-rows: 1

 * - Key pattern
   - TTL
   - Owner
 * - ``caps:user:{user_id}``
   - 300s
   - ``UserCapabilityResolver``
 * - ``menu:user:{user_id}``
   - 300s
   - ``MenuRenderResolver`` (consumidor del endpoint)
 * - ``func:critical_set``
   - 60s
   - Cache del set de codenames con ``is_critical=True``

El prefijo ``KEY_PREFIX`` (``iact:``) se aplica
automaticamente por ``django-redis``.

----

3. Politica de TTL
==================

.. list-table::
 :widths: 30 15 55
 :header-rows: 1

 * - Datos
   - TTL
   - Justificacion
 * - Capabilities (no criticas)
   - 300s
   - Window de stale aceptable (defense-in-depth absorbe).
     Reduce carga DB.
 * - MenuItems renderizados
   - 300s
   - Lifecycle de items es lento (no cambia varias veces por
     hora).
 * - Set de codenames criticos
   - 60s
   - Cambia raramente (via migration). TTL bajo para que un
     deploy se refleje rapido en lectores.

**Invalidacion explicita** prevalece sobre TTL — los UCs
mutating de RBAC (``assign_functions``, ``revoke_function_group``,
``manage_menu_lifecycle``, etc.) invalidan ``caps:user:{id}``
en ``transaction.on_commit`` (ver ADR-BACK-009 §6.2).

----

4. Bypass para capabilities criticas
====================================

Las capabilities con ``Function.is_critical=True`` (ADR-BACK-010)
**no usan cache**. ``UserCapabilityResolver.has_capability``
consulta DB directamente para esas codenames.

Para evitar una query adicional al catalogo de Functions en
cada request, el set ``func:critical_set`` cachea el listado
de codenames criticos con TTL=60s:

.. code-block:: python

   def _critical_codenames() -> set[str]:
       cached = cache.get("func:critical_set")
       if cached is not None:
           return cached
       codenames = set(
           Function.objects
                   .filter(is_critical=True, is_active=True)
                   .values_list("codename", flat=True)
       )
       cache.set("func:critical_set", codenames, timeout=60)
       return codenames

----

5. Degraded mode operacional
============================

Cuando el motor de cache no esta disponible:

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Operacion
   - Comportamiento
   - Telemetria
 * - ``cache.get`` falla
   - Continua a query DB
   - ``rbac.cache.get_failed`` +1
 * - ``cache.set`` falla
   - Ignora silenciosamente
   - ``rbac.cache.set_failed`` +1
 * - ``cache.delete`` (invalidacion)
   - Ignora silenciosamente
   - ``rbac.cache.invalidation_failed`` +1
 * - UC transaccional
   - **Continua** (no rollback)
   - log nivel ERROR con contexto del UC

Ver thresholds de alerta en ADR-BACK-009 §6.3.

----

6. Topologia y HA
=================

**Recomendacion para produccion:**

- **Redis Sentinel** o**Redis Cluster** segun escala.
- Read replicas opcionales para reduccion de carga (cache
  de capabilities es read-heavy).
- Backup no critico — el cache es reconstruible desde DB.

**Recomendacion para desarrollo:**

- Container Docker single-instance (``redis:7-alpine``).
- Sin persistencia (``--save ""`` para evitar disk I/O en
  laptops).

----

7. Migracion desde sistema sin cache
====================================

Si el sistema actualmente NO tiene cache:

1. Deploy del codigo con ``UserCapabilityResolver`` en modo
   bypass (``CACHE_TTL=0``) — fuerza DB-direct, mismo
   comportamiento que hoy.
2. Verificar P95 con telemetria.
3. Deploy gradual de TTL a 60s, luego 300s.
4. Monitor ``rbac.cache.invalidation_failed`` — si es alto,
   investigar antes de subir TTL.

----

8. Referencias
==============

- :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
  (politica conceptual).
- :doc:`/backend/adr-back-010-function-is-critical-governance`
  (catalogo de capabilities criticas).
- :doc:`/backend/rbac-implementation-guide` §Q9 (codigo del
  resolver).
- ``django-redis`` `documentation
  <https://github.com/jazzband/django-redis>`_.
