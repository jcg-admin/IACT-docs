.. meta::
 :artefacto: UC_ADM_05_EXC
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

**Trigger:** PASO 5 detecta que invoker NO tiene
``manage_menu_lifecycle``.

**Respuesta:** 403 Forbidden + audit
``CAPABILITY_DENIED``. Sin window de stale (bypass cache).

5.2 EX-02: Transicion invalida
==============================

**Trigger:** PASO 7 detecta que el ``status`` actual no
permite la transicion solicitada (e.g., DRAFT → DEPRECATED
sin pasar por ACTIVE).

**Respuesta:** 409 Conflict con
``{"error": "invalid_transition", "current_status": "DRAFT", "requested": "DEPRECATED"}``.

**Tabla de transiciones VALIDAS:** ver flujo principal §3.1.

5.3 EX-03: MenuItem inexistente
===============================

**Trigger:** PASO 6 — ID no existe.

**Respuesta:** 404 Not Found.

5.4 EX-04: Function asociada inactiva (publish)
===============================================

**Trigger:** PASO 8 del flujo principal — al intentar
DRAFT → ACTIVE, la ``Function`` asociada esta
``is_active=False``.

**Respuesta:** 422 Unprocessable Entity con
``{"error": "function_inactive", "function_codename": "..."}``.

**Justificacion:** publicar un item cuya capability
subyacente no es accesible deja un item siempre invisible
(I-4) — error logico que el sistema rechaza.

5.5 EX-05: block_reason invalido
================================

**Trigger:** FA-05 detecta ``block_reason`` con menos de
20 caracteres o vacio.

**Respuesta:** 422 Unprocessable Entity con
``{"errors": [{"field": "block_reason", "code": "too_short", "min_length": 20}]}``.

5.6 EX-06: Activar block en estado != DEPRECATED
================================================

**Trigger:** FA-05 detecta que ``status`` no es
``DEPRECATED``.

**Respuesta:** 409 Conflict con
``{"error": "block_only_in_deprecated"}``.

**Justificacion:** el flag no aplica fuera de DEPRECATED.

5.7 EX-07: Falla del Almacen de Datos
=====================================

**Trigger:** error transient en UPDATE / COMMIT.

**Respuesta:** 503 con ``retry_after``. Transaccion
rollback. Sin audit, sin invalidacion.

5.8 EX-08: Falla del Servicio de Cache (degraded)
=================================================

**Trigger:** PASO 13 falla al invalidar.

**Respuesta:** **Operacion exitosa** (200). La transicion
NO se revierte. Audit ``CACHE_INVALIDATION_FAILED`` +
metric ``rbac.cache.invalidation_failed`` +1.

**Trade-off:** users pueden ver la version vieja del menu
hasta TTL=300s.

5.9 EX-09: Concurrencia en transicion
=====================================

**Trigger:** dos transiciones simultaneas sobre el mismo
item (e.g., admin manual y Planificador de Tareas).

**Respuesta:** la primera transaccion gana. La segunda
recibe 409 Conflict con
``{"error": "stale_status_state", "current_status": "<actual>"}`` y NO se aplica.

**Notas:** el modelo usa lock optimista basado en
``updated_at`` o version field. Lock transaccional a nivel
DB es opcional en items de baja frecuencia.

5.10 EX-10: Auto-archive falla parcialmente
===========================================

**Trigger:** FA-04 procesa N items, M de ellos fallan
(e.g., transient errors o EX-09).

**Comportamiento:** los exitos se commitean (atomicidad
por item, no por batch). El reporte de ejecucion del job
incluye ``success_count`` y ``failure_count`` con detalle.

**Notificacion al system_admin:** resumen del ejecutado
+ failures con razon.
