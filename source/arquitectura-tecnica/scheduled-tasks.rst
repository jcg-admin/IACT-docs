.. meta::
 :artefacto: SCHEDULED_TASKS
 :tipo: Decision Tecnica
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno

==================================
Tareas Programadas (Scheduled)
==================================

Decisiones tecnicas concretas sobre el motor de tareas
programadas, su configuracion y los jobs registrados.

.. note::

   Este documento contiene decisiones de **implementacion
   tecnica**. La narrativa UC vive en
   ``source/requisitos/`` y usa los terminos canonicos
   STD-010 ("el Planificador de Tareas", no "Celery beat").

----

1. Motor del Planificador
==========================

**Decision:** Celery 5.x con Celery beat como scheduler.

**Razones:**

- Ecosystem estable en proyectos Django.
- Soporte nativo para retry, dead letter queue, periodic
  schedules.
- Worker / scheduler decoupled (escalabilidad
  independiente).

**Alternativas descartadas:**

- **APScheduler:** sin worker pool — todos los jobs en un
  proceso. Limitado para escalar.
- **Cron del SO:** sin observabilidad, sin retry, sin DLQ.
- **Django-Q:** menor adopcion; ecosistema mas chico.

----

2. Topologia
============

::

   ┌──────────────┐
   │ celery beat  │ produce schedules
   └──────┬───────┘
          │ enqueue
          v
   ┌──────────────┐    ┌─────────────┐
   │ message broker │ <- │ celery worker │ consume + ejecuta
   │ (Redis)        │    └─────────────┘
   └────────────────┘
          │
          v
   ┌──────────────┐
   │ result backend│ (Redis/DB)
   └──────────────┘

**Broker:** Redis (compartido con el servicio de cache —
ver :doc:`cache-strategy`).

**Result backend:** Redis para resultados temporales;
PostgreSQL via ``django-celery-results`` para resultados
persistentes (jobs criticos como auto-archive).

----

3. Jobs registrados
===================

3.1 ``auto_archive_menu_items``
-------------------------------

.. list-table::
 :widths: 30 70
 :header-rows: 0

 * - **Tarea**
   - ``apps.access.tasks.auto_archive_menu_items``
 * - **Schedule**
   - Diaria a las 02:00 UTC
 * - **Origen**
   - UC_ADM_05 (gestion de lifecycle de MenuItem)
 * - **Funcion**
   - Procesar items en DEPRECATED >90d sin
     ``block_auto_archive``; emitir warnings (30d, 80d)
     y critical alerts (>=90d con block=True)
 * - **Idempotente**
   - Si — re-ejecucion no duplica archives ni
     notificaciones
 * - **Retry policy**
   - Max 3 retries con backoff exponencial. Si falla
     completamente: critical alert al sistema de
     observabilidad
 * - **Telemetria**
   - ``rbac.menu.lifecycle.auto_archive_count`` (counter)

----

4. Configuracion canonica
=========================

4.1 settings.py
---------------

.. code-block:: python

   # config/celery.py
   from celery import Celery
   from celery.schedules import crontab

   app = Celery("iact")
   app.config_from_object("django.conf:settings", namespace="CELERY")
   app.autodiscover_tasks()

   CELERY_BROKER_URL = env("CELERY_BROKER_URL",
                            default="redis://redis:6379/2")
   CELERY_RESULT_BACKEND = "django-db"  # critico — persistente
   CELERY_TASK_TRACK_STARTED = True
   CELERY_TASK_TIME_LIMIT = 600     # 10 min hard limit
   CELERY_TASK_SOFT_TIME_LIMIT = 540  # 9 min warning
   CELERY_TASK_ACKS_LATE = True       # garantia at-least-once
   CELERY_WORKER_PREFETCH_MULTIPLIER = 1

   CELERY_BEAT_SCHEDULE = {
       "auto_archive_menu_items": {
           "task": "apps.access.tasks.auto_archive_menu_items",
           "schedule": crontab(hour=2, minute=0),
           "options": {"queue": "lifecycle"},
       },
   }

4.2 Queues
----------

- ``default``: jobs interactivos / triggered.
- ``lifecycle``: jobs periodicos de mantenimiento (incluido
  ``auto_archive_menu_items``).
- ``notifications``: envio de mensajes al
  ``InternalMailbox`` o servicios externos.

----

5. Identidad del worker
=======================

Los jobs se ejecutan con un **service account** dedicado
(``system_user``) creado en migration:

.. code-block:: python

   # apps/users/migrations/0YY_create_system_user.py
   def create_system_user(apps, schema_editor):
       User = apps.get_model("users", "User")
       User.objects.get_or_create(
           username="system",
           defaults={
               "is_active": True,
               "is_staff": False,    # no admin Django
               "is_superuser": False,
               "email": "system@iact.local",
           },
       )

**Importante:** ``system_user`` NO esta asignado a ningun
``AccessGroup`` — los jobs invocan directamente la capa de
servicios sin pasar por el ``FunctionAuthBackend``. Auditoria
trazable por el ``actor='system'`` en cada audit event.

----

6. Observabilidad
=================

Metricas obligatorias por job:

- ``celery.task.run_count{task=auto_archive_menu_items}``
- ``celery.task.duration_seconds{task=...}`` (histogram)
- ``celery.task.retry_count{task=...}``
- ``celery.task.failure_count{task=...}``

Logs estructurados con ``task_id``, ``task_name``,
``status``, ``runtime_ms``.

----

7. Operacion
============

7.1 Inicio en desarrollo
------------------------

::

   docker compose up -d redis
   celery -A config worker --loglevel=INFO --queue=default,lifecycle
   celery -A config beat --loglevel=INFO

7.2 Operacion en produccion
---------------------------

- 1 ``celery beat`` instance (singleton — schedule
  master).
- N workers escalables horizontalmente.
- Reinicio del beat preserva el estado del schedule
  (file-based o ``django-celery-beat`` para persistencia
  en DB).

7.3 Monitoreo
-------------

- Flower (UI de Celery) para visibilidad operacional.
- Metricas exportadas a Prometheus / Grafana.
- Critical alerts del job ``auto_archive_menu_items``
  enrutadas al equipo de plataforma.

----

8. Trazabilidad
===============

- :doc:`/requisitos/casos-uso/admin/uc-adm-05/index`
  (UC consumidor — lifecycle).
- :doc:`/backend/adr-back-008-menuitem-wrapper-ux-sobre-function`
  (modelo afectado).
- :doc:`/backend/adr-back-009-cache-capabilities-degraded-mode`
  (politica de invalidacion compartida).
- :doc:`cache-strategy` (broker compartido).
- WP origen
  ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``
  (gap #3 strategy addendum).
