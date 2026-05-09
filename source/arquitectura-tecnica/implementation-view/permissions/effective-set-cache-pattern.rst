.. meta::
 :artefacto: AT_IMPL_PATTERN_EFFECTIVE_SET_CACHE
 :tipo: Diagrama Arquitectonico — Implementation View — Pattern
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_impl_pattern_effective_set_cache:

============================================================
Implementation View — Effective Set Cache (LRU + TTL)
============================================================

Patron de cache de permisos efectivos. Es transversal:
``HasFunctionPerm`` lo consume por **cada request DRF** (hot
path). Sin cache, el costo de resolver permisos en una
JOIN de ``assignment x group_function x function`` se paga
N veces por minuto. Con cache, se paga una vez por usuario
cada TTL.

Implementacion sin Redis (``ADR-BACK-012``).

Estructura del cache
=====================

.. code-block:: python

   # apps/permissions/services/effective_set_cache.py

   from cachetools import TTLCache
   from threading import RLock
   from typing import FrozenSet

   class EffectiveSetCache:
       """Cache thread-safe (LRU + TTL) per-process.

       maxsize=10000: ~10k usuarios concurrentes maximo.
       ttl=300: 5 min — suficientemente corto para que los
       cambios en asignaciones se reflejen pronto, suficientemente
       largo para que el hit-rate sea > 90%.
       """

       def __init__(self, maxsize: int = 10000, ttl: int = 300):
           self._cache: TTLCache = TTLCache(maxsize=maxsize, ttl=ttl)
           self._lock = RLock()

       def get_or_compute(self, user_id: int) -> FrozenSet[str]:
           with self._lock:
               cached = self._cache.get(user_id)
               if cached is not None:
                   return cached
           # compute fuera del lock para no bloquear lecturas
           computed = compute_effective_set(user_id)
           with self._lock:
               self._cache[user_id] = computed
           return computed

       def invalidate(self, user_id: int) -> None:
           with self._lock:
               self._cache.pop(user_id, None)

       def invalidate_all(self) -> None:
           with self._lock:
               self._cache.clear()

Invalidacion via Django signals
================================

.. uml::
 :caption: Cache invalidation — write en MOD_Access dispara signal.

 @startuml

 actor Caller
 participant "AccessService\n(MOD_Access)" as AS <<service>>
 participant "Django signal\nassignment_changed" as Sig <<signal>>
 participant "EffectiveSetCache\n(per worker)" as Cache <<cache>>

 Caller -> AS : assign(user_id, group_ref)
 activate AS
 AS -> AS : transaction.atomic block
 note right of AS
   1) INSERT assignment
   2) INSERT audit_event
   3) signal.send(user_id)
   La signal se procesa **dentro**
   del atomic — si falla, todo
   rollback.
 end note

 AS -> Sig : send(sender=AccessService,\nuser_id=user_id)
 activate Sig
 Sig -> Cache : invalidate(user_id)\n(receiver: invalidate_user_cache)
 Cache --> Sig : ok
 deactivate Sig

 AS --> Caller : Assignment
 deactivate AS

 @enduml

Politica de invalidacion
=========================

.. list-table::
 :widths: 35 65
 :header-rows: 1

 * - Trigger
   - Accion sobre cache
 * - ``Assignment`` create / revoke
   - ``invalidate(user_id)``
 * - ``GroupFunction`` change
     (catalogo de un grupo cambia)
   - ``invalidate_all()`` — afecta a todos los usuarios
     con asignacion a ese grupo
 * - ``Function`` deprecated / archived
   - ``invalidate_all()``
 * - User block
     (:doc:`/arquitectura-tecnica/design-view/users/user-lifecycle`)
   - ``invalidate(user_id)`` + revoke JWT (cross-modulo)

Restricciones de implementacion
================================

- **R-PERM-CACHE-01:** el cache es **per-process**. En un
  setup con N workers Gunicorn, hay N caches independientes.
  La signal Django se entrega **a todos los receivers en
  el mismo proceso** que la disparo — los otros workers
  reciben la signal por mecanismo cross-process via
  Django's signal infrastructure (in-process per worker
  con dispatcher local).
- **R-PERM-CACHE-02:** ``invalidate_all`` es la operacion
  mas costosa — se evita salvo cuando es necesaria. NO
  ejecutar en background loops.
- **R-PERM-CACHE-03:** TTL = 300s. Si un cambio no se
  invalida (e.g. write fuera de Django), el efecto demora
  como mucho 5 min en propagarse.
- **R-PERM-CACHE-04:** sin Redis. Si en el futuro se migra
  a multi-host, este patron necesita reemplazarse por
  Redis pub/sub o equivalente. Documentado como deuda
  tecnica en ``technical-debt.md``.

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Archivo
 * - EffectiveSetCache
   - ``apps/permissions/services/effective_set_cache.py``
 * - Compute function
   - ``apps/permissions/services/effective_set_compute.py``
 * - Signal definitions
   - ``apps/permissions/signals.py``
 * - Receivers
   - ``apps/permissions/apps.py: ready()`` registra receivers

----

.. seealso::

 - :doc:`interaction-pattern` — flow de consulta.
 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/implementation-view/access/rbac-enforcement-pattern` —
   consumidor del cache (hot path).
 - :doc:`/arquitectura-tecnica/design-view/permissions/effective-set-evaluation-flow` —
   logica en DesignView.
