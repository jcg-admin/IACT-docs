.. meta::
 :artefacto: ADR-BACK-009
 :tipo: ADR
 :dominio: backend
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno

.. _adr-back-009:

============================================================================
ADR-BACK-009: Cache de capabilities con degraded mode ante falla
============================================================================

Estado y metadata
=================

- **Estado:** Aprobada.
- **Fecha:** 2026-05-07.
- **Decisores:** NestorMonroy (ejecutor) + analisis documentado en WP
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``.
- **Contexto tecnico:** Backend — capa de cache para
  resolucion de capabilities por usuario.
- **Relacionados:**

  - :doc:`/backend/adr-back-007-rbac-custom-vs-auth-group`
    (modelo RBAC custom).
  - :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
    (consumidor del cache).
  - :doc:`/backend/adr-back-010-function-is-critical-governance`
    (capabilities que bypassean el cache — AP-2b).

- **Refs WP discover:**

  - ``discover/menuitem-design-corrections-v2.md`` G-1, G-3.
  - ``discover/final-decisions-p1-p4-and-pending-items.md`` §3.

----

1. Contexto y Problema
======================

Cada request autenticado ejecuta el ``FunctionAuthBackend`` que
resuelve las capabilities del usuario. Sin cache, la query
canonica es:

.. code-block:: sql

   SELECT DISTINCT f.codename
     FROM functions f
     JOIN function_group_membership fgm
       ON fgm.function_id = f.id
     JOIN access_groups ag
       ON ag.id = fgm.group_id
     JOIN user_access_group_assignment uaga
       ON uaga.group_id = ag.id
    WHERE uaga.user_id = ?
      AND f.is_active = TRUE
      AND (uaga.expires_at IS NULL OR uaga.expires_at > NOW());

Con indices apropiados (P3 del WP — 13 indices definidos), P95
de la query es ≤ 20ms en cache MISS. Aceptable individualmente,
pero el endpoint ``GET /api/v1/menu/`` y cada request protegido
ejecuta esta resolucion — el costo agregado bajo carga es alto.

**Pregunta arquitectonica:**

¿Como cachear las capabilities de manera que (a) reduzca latencia
en hot path, (b) mantenga consistency suficiente ante revocacion,
y (c) tolere fallas del servicio de cache sin degradar
disponibilidad del UC?

----

2. Factores de Decision
=======================

- **Latencia de hot path** (cache HIT debe ser ≤ 5ms).
- **Consistency tras revocacion** — un user revocado no deberia
  retener acceso indefinidamente.
- **Disponibilidad del UC ante falla del servicio de cache** —
  no bloquear UCs criticos por una caida del cache.
- **Simplicidad del modelo de invalidacion** — preferir
  invalidacion explicita en UCs transaccionales sobre signals.
- **Telemetria obligatoria** — no aceptar fallas silenciosas.

----

3. Decision
===========

3.1 Politica de cache
---------------------

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Item
   - Decision
 * - TTL
   - 300s (5 minutos)
 * - Key pattern
   - ``caps:user:{user_id}``
 * - Valor
   - Set de codenames serializado
 * - Invalidacion
   - **Explicita** dentro del UC transaccional (post-COMMIT).
     **No** signals.
 * - Falla del servicio de cache
   - **Degraded mode** — UC continua, log obligatorio + telemetria
 * - Race condition (TTL stale)
   - Aceptado (defense-in-depth en endpoint absorbe)
 * - Bypass selectivo
   - ``Function.is_critical=True`` → consulta DB sin pasar cache
     (AP-2b — ver ADR-BACK-010)

3.2 Por que invalidacion explicita y no signals
-----------------------------------------------

- **Bulk operations no disparan signals** — un
  ``UserAccessGroupAssignment.objects.update(...)`` que cambia
  10000 asignaciones no dispara post_save.
- **Transaccionalidad explicita** — la invalidacion ocurre tras
  COMMIT exitoso, no antes (evitamos invalidar y luego rollback).
- **Trazable en el UC** — al leer el UC, queda explicito que
  hay una invalidacion. Con signals, el efecto es invisible en
  el codigo del UC.

3.3 Degraded mode ante falla
----------------------------

Si el servicio de cache no esta disponible cuando se intenta
invalidar, el UC **continua** con telemetria obligatoria:

.. code-block:: python

   def invalidate_user_capabilities(user_id: int) -> None:
       try:
           cache.delete(f"caps:user:{user_id}")
       except CacheError as exc:
           logger.error(
               "cache_invalidation_failed",
               extra={
                   "user_id": user_id,
                   "exc": str(exc),
                   "uc": current_uc_context(),
               },
           )
           metrics.increment("rbac.cache.invalidation_failed")
           # NO re-raise — el UC continua

3.4 Comparacion: degraded mode vs strict mode
---------------------------------------------

.. list-table::
 :widths: 30 35 35
 :header-rows: 1

 * - Aspecto
   - Strict mode (rechazada)
   - Degraded mode (elegida)
 * - Comportamiento del UC ante fallo
   - UC falla, transaccion rollback
   - UC continua, log + metrica
 * - Consistency garantizada
   - Eventual con TTL
   - Eventual con TTL
 * - Availability del UC
   - Bloqueado si cache caido
   - UC sigue funcionando
 * - Window de stale data
   - 0 segundos (UC bloqueado)
   - Hasta TTL (300s) tras recovery
 * - Resiliencia
   - Baja (cache es SPOF)
   - Alta
 * - Telemetria
   - Implicita (UC fallido)
   - Explicita (log + metrica)

3.5 Por que degraded mode es seguro
-----------------------------------

(a) **Defense-in-depth absorbe el riesgo.** El endpoint protegido
    siempre verifica via DB en cache MISS (cache.get retorna None
    → query). Si el cache esta caido durante una invalidacion, el
    proximo request del user con el cache aun activo lee del
    cache stale por hasta TTL segundos; pero el cache MISS
    posterior consulta DB y refleja el estado real.

(b) **Bloquear UCs cuando el servicio de cache cae transforma el
    cache en un SPOF** — mas costoso que la window de stale.

(c) **Window de stale ≤ TTL** — 300s es aceptable para
    capabilities no criticas. Las criticas (``is_critical=True``)
    bypassean el cache (ADR-BACK-010).

(d) **Telemetria detecta el problema** — alertas configuradas
    sobre ``rbac.cache.invalidation_failed`` permiten
    intervencion oportuna.

----

4. Consecuencias
================

4.1 Positivas
-------------

- **Latencia P95 ≤ 5ms en cache HIT** — hot path optimizado.
- **Resiliencia** — UCs no se bloquean por caidas del cache.
- **Telemetria explicita** — los fallos de invalidacion son
  observables, no silenciosos.
- **Modelo de invalidacion simple** — solo UCs transaccionales
  invalidan; lectores nunca invalidan.
- **Compatible con bypass selectivo** (ADR-BACK-010).

4.2 Negativas (aceptadas)
-------------------------

- **Window de stale tras revocacion** — hasta 300s un user puede
  retener una capability revocada en cache. Mitigado por:
  capabilities criticas bypassean cache (``is_critical``);
  defense-in-depth en endpoint siempre verifica DB; admins
  criticos pueden forzar logout del user afectado (UC_AUTH_05
  si existe, o invalidacion manual).

- **Telemetria requiere infraestructura.** Asume que el sistema
  tiene log centralizado y metricas. Mitigado: ADR-BACK-009
  declara telemetria como **obligatoria**, no opcional.

- **Invalidacion explicita en cada UC** que modifica
  capabilities. Mitigado: helper ``invalidate_user_capabilities``
  centralizado, llamado desde cada UC mutating de RBAC.

----

5. Alternativas Consideradas
============================

5.1 Alternativa A — Strict mode (UC rollback ante fallo de cache)
------------------------------------------------------------------

UC falla con 503 si el servicio de cache no responde durante
invalidacion.

- **Pros:** consistency mas estricta — no hay window de stale.
- **Contras:** transforma el cache en SPOF; UCs criticos
  (e.g., revocar acceso de un atacante) se bloquean cuando se
  necesita disponibilidad maxima.
- **Veredicto:** rechazada. El cache es una optimizacion, no
  parte del contrato del UC.

5.2 Alternativa B — Cache aside con write-through
-------------------------------------------------

Escribir directamente al cache en cada UC (en vez de invalidar).

- **Pros:** sin window de stale tras invalidacion exitosa.
- **Contras:** requiere que cada UC sepa **calcular** las
  capabilities resultantes (no solo invalidar). Acopla logica
  de RBAC a cada UC mutating. Mas codigo, mas posibilidad de
  bugs.
- **Veredicto:** rechazada. Invalidacion + lazy load es mas
  simple y robusto.

5.3 Alternativa C — Sin cache (DB-direct siempre)
-------------------------------------------------

- **Pros:** strong consistency sin window de stale.
- **Contras:** P95 ≤ 20ms es aceptable individualmente pero el
  costo agregado bajo carga es prohibitivo. Cada request paga
  una query JOIN de 4 tablas.
- **Veredicto:** rechazada como politica general; aplicada
  selectivamente para ``is_critical=True`` (ADR-BACK-010).

----

6. Implementacion
=================

6.1 Resolver con cache (AP-2a)
------------------------------

.. code-block:: python

   class UserCapabilityResolver:
       CACHE_TTL = 300

       @staticmethod
       def resolve(user) -> set[str]:
           if not user or not user.is_authenticated:
               return set()
           key = f"caps:user:{user.id}"
           try:
               cached = cache.get(key)
               if cached is not None:
                   return cached
           except CacheError as exc:
               logger.warning(
                   "cache_get_failed", extra={"user_id": user.id,
                                                "exc": str(exc)})
               metrics.increment("rbac.cache.get_failed")
               # continua a DB
           codenames = UserCapabilityResolver._query_db(user)
           try:
               cache.set(key, codenames,
                         timeout=UserCapabilityResolver.CACHE_TTL)
           except CacheError:
               metrics.increment("rbac.cache.set_failed")
           return codenames

6.2 Invalidacion en UC (post-COMMIT)
------------------------------------

.. code-block:: python

   def invalidate_user_capabilities(user_id: int) -> None:
       try:
           cache.delete(f"caps:user:{user_id}")
       except CacheError as exc:
           logger.error("cache_invalidation_failed",
                          extra={"user_id": user_id, "exc": str(exc)})
           metrics.increment("rbac.cache.invalidation_failed")


   class AssignFunctionsUC:
       @transaction.atomic
       def execute(self, user_id, function_codes):
           # ... insert/update ...
           transaction.on_commit(
               lambda: invalidate_user_capabilities(user_id),
           )

6.3 Alertas operacionales
-------------------------

Configurar en sistema de monitoreo:

- Metric ``rbac.cache.invalidation_failed`` rate ≥ 1/min →
  WARNING (cache potencialmente degradado).
- Metric ``rbac.cache.invalidation_failed`` rate ≥ 10/min →
  CRITICAL (cache caido — investigar).
- Metric ``rbac.cache.get_failed`` rate ≥ 100/min →
  CRITICAL (cache caido afectando hot path).

----

7. Trazabilidad
===============

- Decision en strategy:
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs/strategy/menu-rbac-user-scope-solution-strategy.md``
  §3 P4.
- Resolucion del item pendiente #2:
  ``discover/final-decisions-p1-p4-and-pending-items.md`` §3.
- Bypass selectivo: ADR-BACK-010.
- Implementacion concreta del servicio de cache (Redis 7+):
  vive en ``arquitectura-tecnica/cache-strategy.rst`` (a producir
  en L2).
