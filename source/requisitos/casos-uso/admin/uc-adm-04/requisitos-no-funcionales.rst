.. meta::
 :artefacto: UC_ADM_04_NFR
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

================================
6. Requisitos No Funcionales
================================

6.1 Rendimiento
===============

.. list-table::
 :widths: 25 25 50
 :header-rows: 1

 * - Metrica
   - Target
   - Notas
 * - P50 CREATE
   - ≤ 200 ms
   - Incluye verificacion bypass de cache, INSERT,
     audit, invalidacion
 * - P95 CREATE
   - ≤ 500 ms
   - Bajo carga normal (≤ 10 ops/s en MOD_Admin)
 * - P50 UPDATE
   - ≤ 150 ms
   - Sin INSERT, solo UPDATE
 * - P50 LIST (paginado 50)
   - ≤ 100 ms
   - Con select_related + indices ``status``
     y ``(status, display_order)``
 * - Bulk reorder (50 items)
   - ≤ 1000 ms
   - UPDATE multi-row + invalidaciones

6.2 Disponibilidad
==================

- Identica a UC_PERM_06 / UC_PERM_07 (99.5% en horario
  habil).
- Operacion administrativa — no bloquea operacion de
  users finales.

6.3 Auditabilidad
=================

- Cada operacion mutating registra evento en audit log
  con before/after state.
- Audit log es append-only (no permite UPDATE ni DELETE).
- Retencion minima: 7 anos (compliance).

6.4 Seguridad
=============

- Capability ``manage_menu_catalog`` con
  ``is_critical=True`` — bypass de cache obligatorio en
  cada request (AP-2b).
- HTTPS exclusivo.
- CSRF token requerido en operaciones mutating.
- Rate limit: 60 ops/min por invoker (proteccion contra
  abuso administrativo).

6.5 Resiliencia
===============

- Falla del servicio de cache: degraded mode
  (ADR-BACK-009). UC continua, telemetria explicita.
- Falla del Almacen de Datos: 503 con retry_after, sin
  reintento automatico server-side.
- Race conditions: validaciones de invariantes en cada
  transaccion + UNIQUE constraint en
  ``MenuItem.function``.

6.6 Observabilidad
==================

Metricas obligatorias:

- ``rbac.menu.create_count`` (counter).
- ``rbac.menu.update_count`` (counter).
- ``rbac.menu.list_latency`` (histogram).
- ``rbac.cache.invalidation_failed`` (counter — compartida
  con UC_PERM_06).
- ``rbac.audit.event_count{type=MENU_ITEM_*}`` (counter).
