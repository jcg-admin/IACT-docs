.. meta::
 :artefacto: UC_ADM_04_EXC
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==================
5. Excepciones
==================

5.1 EX-01: Capability ausente o revocada
========================================

**Trigger:** PASO 7 detecta que el invoker NO tiene
``manage_menu_catalog`` (revocada o nunca asignada).

**Respuesta:** 403 Forbidden.

**Audit:** evento ``CAPABILITY_DENIED`` con
``actor_id``, ``capability="manage_menu_catalog"``,
``timestamp``, ``ip``.

**Notas:** la verificacion bypassa cache (AP-2b), por lo
cual no hay window de stale.

5.2 EX-02: Function no existe o esta inactiva
=============================================

**Trigger:** PASO 8 — la ``Function`` referenciada en
``function_id`` del payload no existe o tiene
``is_active=False``.

**Respuesta:** 422 Unprocessable Entity con
``{"errors": [{"field": "function", "code": "not_found_or_inactive"}]}``.

**Audit:** sin evento (rechazo de input antes de operacion).

5.3 EX-03: Parent ARCHIVED
==========================

**Trigger:** PASO 10 — el ``parent`` referenciado existe
pero esta ARCHIVED.

**Respuesta:** 422 Unprocessable Entity con
``{"errors": [{"field": "parent_id", "code": "parent_archived"}]}``.

**Justificacion:** un ``MenuItem`` activo bajo un parent
archivado quedaria visualmente huerfano (el parent no
renderiza).

5.4 EX-04: Ciclo en jerarquia
=============================

**Trigger:** FA-03 PASO 5 detecta que el cambio de
``parent`` introduce un ciclo (A → B → A).

**Respuesta:** 422 Unprocessable Entity con
``{"errors": [{"field": "parent_id", "code": "cycle_detected"}]}``.

**Audit:** sin evento.

5.5 EX-05: Falla del Almacen de Datos
=====================================

**Trigger:** error de integridad o conexion durante
INSERT / UPDATE / COMMIT.

**Respuesta:** 503 Service Unavailable con
``{"error": "transient_error", "retry_after": 5}``.

**Postcondiciones:**

- Transaccion rollback.
- Sin audit event (la transaccion no commiteo).
- Sin invalidacion de cache.

5.6 EX-06: Falla del Servicio de Cache (degraded mode)
======================================================

**Trigger:** PASO 16 falla al invalidar el servicio de
cache.

**Respuesta:** **Operacion exitosa** (200/201) — el UC
**no** rollback. El estado en el Almacen de Datos es la
fuente de verdad.

**Audit:** evento ``CACHE_INVALIDATION_FAILED`` con
``user_ids_affected``, ``cache_key_pattern``, ``error``,
``timestamp``.

**Telemetria:** metric ``rbac.cache.invalidation_failed``
incrementa.

**Trade-off:** users con la capability subyacente pueden
ver el menu cacheado por hasta 300s antes de que el TTL
expire. Aceptado por defense-in-depth (CNST-032 v2.0.0
§3.2 — el frontend igual filtra por capabilities).

5.7 EX-07: Validacion de invariantes (I-1..I-3)
===============================================

**Trigger:** PASO 11 detecta violacion de algun invariante
que no fue capturado por validaciones previas (e.g., race
condition entre validacion y INSERT).

**Respuesta:** 409 Conflict con codigo de invariante
violado.

**Audit:** evento ``INVARIANT_VIOLATION`` con
``invariant_id`` (I-1, I-2 o I-3) + contexto.

**Notas:** dado el lock optimista del modelo, este caso
deberia ser raro. Si recurre, indicar problema de
concurrencia que requiere investigacion.
