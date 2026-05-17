.. meta::
 :artefacto: UC_ADM_05_NFR
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
 :widths: 30 25 45
 :header-rows: 1

 * - Operacion
   - P50 / P95
   - Notas
 * - Transicion individual
   - 150 / 400 ms
   - Bypass cache + UPDATE + audit + invalidacion
 * - Activar block flag
   - 150 / 400 ms
   - UPDATE + audit
 * - Job auto-archive (1000 items)
   - < 30 s
   - Procesado uno a uno con batch size 100
 * - Pre-archive notification job
   - < 5 s
   - Solo lectura + envio de notificaciones

6.2 Disponibilidad
==================

- 99.5% en horario habil para operaciones manuales.
- Job del Planificador de Tareas: ejecucion una vez por
  dia (UTC 02:00 sugerido); si falla, el siguiente dia
  recoge los items pendientes (idempotente).

6.3 Auditabilidad
=================

- 100% de transiciones registradas en audit log.
- Audit incluye ``before_status``, ``after_status``,
  ``deprecated_at``, ``archived_at``, ``actor_id``
  (system para auto-archive).
- Cambios al flag ``block_auto_archive`` registrados como
  evento separado con ``block_reason`` completo.

6.4 Seguridad
=============

- Capability ``manage_menu_lifecycle`` con
  ``is_critical=True`` — bypass de cache obligatorio.
- HTTPS exclusivo.
- CSRF en operaciones manuales.
- Identidad del Planificador de Tareas: certificada por
  service account dedicado, no reutilizado para otras
  operaciones.

6.5 Resiliencia
===============

- Transiciones atomicas: rollback ante cualquier error.
- Lock optimista para evitar race conditions.
- Job idempotente: ejecutarse dos veces el mismo dia
  produce el mismo resultado (no duplica audit ni
  notificaciones).

6.6 Observabilidad
==================

Metricas:

- ``rbac.menu.lifecycle.transition_count{from, to}``
  (counter por transicion).
- ``rbac.menu.lifecycle.auto_archive_count`` (counter
  diario).
- ``rbac.menu.lifecycle.block_flag_set_count`` (counter
  con ``block_reason`` redactado).
- ``rbac.menu.lifecycle.deprecated_age_p50`` (histogram
  — distribucion de cuanto tiempo viven los items en
  DEPRECATED).
