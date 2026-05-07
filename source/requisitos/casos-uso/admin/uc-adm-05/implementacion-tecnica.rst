.. meta::
 :artefacto: UC_ADM_05_IMPL
 :tipo: Caso de Uso (implementacion tecnica)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

================================
11. Implementacion Tecnica
================================

.. note::

   Esta seccion es libre de STD-010 — puede mencionar
   tecnologias concretas. La narrativa anterior usa
   vocabulario canonico.

11.1 Stack
==========

- Backend: Django 5.0+ con DRF.
- Almacen de Datos: PostgreSQL 14+.
- Servicio de Cache: Redis 7.x con django-redis.
- Planificador de Tareas: Celery beat (motor concreto —
  ver :doc:`/arquitectura-tecnica/scheduled-tasks`).
- Servicio de Notificacion: ``InternalMailbox`` del
  proyecto (mailbox interno del system_admin).
- Tests: pytest + pytest-django + freezegun.

11.2 Endpoints DRF
==================

.. code-block:: python

   # apps/access/urls.py
   path("admin/menu-items/<int:pk>/publish/",
        MenuItemPublishView.as_view()),
   path("admin/menu-items/<int:pk>/deprecate/",
        MenuItemDeprecateView.as_view()),
   path("admin/menu-items/<int:pk>/reactivate/",
        MenuItemReactivateView.as_view()),
   path("admin/menu-items/<int:pk>/archive/",
        MenuItemArchiveView.as_view()),
   path("admin/menu-items/<int:pk>/block-archive/",
        MenuItemBlockArchiveView.as_view()),

11.3 State machine
==================

.. code-block:: python

   # apps/access/services/menu_lifecycle.py
   VALID_TRANSITIONS = {
       ("DRAFT", "ACTIVE"),
       ("ACTIVE", "DEPRECATED"),
       ("DEPRECATED", "ACTIVE"),
       ("DEPRECATED", "ARCHIVED"),
       ("ARCHIVED", "ACTIVE"),
   }


   class InvalidTransitionError(Exception):
       def __init__(self, current, requested):
           self.current = current
           self.requested = requested
           super().__init__(f"Invalid: {current} -> {requested}")


   class MenuLifecycleService:

       @staticmethod
       def transition(menu_item, target_status, actor):
           current = menu_item.status
           if (current, target_status) not in VALID_TRANSITIONS:
               raise InvalidTransitionError(current, target_status)

           if target_status == "ACTIVE" and not menu_item.function.is_active:
               raise FunctionInactiveError(menu_item.function.codename)

           with transaction.atomic():
               # Snapshot para audit
               before = serialize_menu_item(menu_item)

               menu_item.status = target_status
               now = timezone.now()

               if target_status == "DEPRECATED":
                   menu_item.deprecated_at = now
               elif target_status == "ARCHIVED":
                   menu_item.archived_at = now
                   # block_* preservados durante DEPRECATED -> ARCHIVED
                   # se limpian solo en transicion -> ACTIVE
                   if current == "DEPRECATED":
                       menu_item.block_auto_archive = False
                       menu_item.block_reason = ""
                       menu_item.block_set_by = None
                       menu_item.block_set_at = None
               elif target_status == "ACTIVE":
                   menu_item.deprecated_at = None
                   menu_item.archived_at = None
                   menu_item.block_auto_archive = False
                   menu_item.block_reason = ""
                   menu_item.block_set_by = None
                   menu_item.block_set_at = None

               menu_item.save()
               record_audit_event(
                   "MENU_ITEM_LIFECYCLE_TRANSITION",
                   actor=actor,
                   menu_item_id=menu_item.id,
                   before_state=before,
                   after_state=serialize_menu_item(menu_item),
               )
               transaction.on_commit(
                   lambda: invalidate_menu_for_function(
                       menu_item.function_id,
                   )
               )

11.4 Block flag
===============

.. code-block:: python

   class MenuLifecycleService:

       @staticmethod
       def set_block_flag(menu_item, block_reason, actor):
           if menu_item.status != "DEPRECATED":
               raise BlockOnlyInDeprecatedError()
           if len(block_reason) < 20:
               raise ValidationError(
                   {"block_reason": "min_length=20"}
               )
           with transaction.atomic():
               menu_item.block_auto_archive = True
               menu_item.block_reason = block_reason
               menu_item.block_set_by = actor
               menu_item.block_set_at = timezone.now()
               menu_item.save()
               record_audit_event(
                   "MENU_ITEM_BLOCK_FLAG_SET",
                   actor=actor,
                   menu_item_id=menu_item.id,
                   block_reason=block_reason,
               )

       @staticmethod
       def clear_block_flag(menu_item, actor):
           with transaction.atomic():
               previous_reason = menu_item.block_reason
               menu_item.block_auto_archive = False
               menu_item.block_reason = ""
               menu_item.block_set_by = None
               menu_item.block_set_at = None
               menu_item.save()
               record_audit_event(
                   "MENU_ITEM_BLOCK_FLAG_CLEARED",
                   actor=actor,
                   menu_item_id=menu_item.id,
                   previous_block_reason=redact(previous_reason),
               )

11.5 Job del Planificador (Celery beat)
=======================================

.. code-block:: python

   # apps/access/tasks.py
   from celery import shared_task
   from datetime import timedelta

   DEPRECATED_WARNING_DAYS = 30
   DEPRECATED_PRE_ARCHIVE_DAYS = 80
   DEPRECATED_ARCHIVE_DAYS = 90


   @shared_task
   def auto_archive_menu_items():
       now = timezone.now()
       archive_threshold = now - timedelta(days=DEPRECATED_ARCHIVE_DAYS)
       pre_archive_threshold = now - timedelta(days=DEPRECATED_PRE_ARCHIVE_DAYS)
       warning_threshold = now - timedelta(days=DEPRECATED_WARNING_DAYS)

       # Auto-archive
       to_archive = MenuItem.objects.filter(
           status="DEPRECATED",
           deprecated_at__lt=archive_threshold,
           block_auto_archive=False,
       )
       results = {"archived": 0, "failed": 0}
       for item in to_archive:
           try:
               MenuLifecycleService.transition(
                   item, "ARCHIVED", actor=system_user(),
               )
               results["archived"] += 1
           except Exception as exc:
               logger.error("auto_archive_failed",
                              extra={"item_id": item.id, "exc": str(exc)})
               results["failed"] += 1

       # Critical alerts (>=90d con block=True)
       blocked_critical = MenuItem.objects.filter(
           status="DEPRECATED",
           deprecated_at__lt=archive_threshold,
           block_auto_archive=True,
       )
       if blocked_critical.exists():
           notify_admins(
               level="CRITICAL",
               subject=f"{blocked_critical.count()} MenuItems "
                       f"bloqueados >90d en DEPRECATED",
               items=list(blocked_critical.values(
                   "id", "display_label", "deprecated_at",
                   "block_reason", "block_set_by",
               )),
           )

       # Pre-archive notification (window 80-90d)
       pre_archive = MenuItem.objects.filter(
           status="DEPRECATED",
           deprecated_at__lt=pre_archive_threshold,
           deprecated_at__gte=archive_threshold,
           block_auto_archive=False,
       )
       if pre_archive.exists():
           notify_admins(
               level="WARNING",
               subject=f"{pre_archive.count()} MenuItems "
                       f"auto-archive en <=10 dias",
               items=list(pre_archive.values(
                   "id", "display_label", "deprecated_at",
               )),
           )

       # Warning a 30d (early)
       warning = MenuItem.objects.filter(
           status="DEPRECATED",
           deprecated_at__lt=warning_threshold,
           deprecated_at__gte=pre_archive_threshold,
       )
       if warning.exists():
           notify_admins(
               level="WARNING",
               subject=f"{warning.count()} MenuItems en DEPRECATED >30d",
               items=list(warning.values(
                   "id", "display_label", "deprecated_at",
               )),
           )

       return results

11.6 Schedule (celery beat)
===========================

.. code-block:: python

   # config/celery.py
   from celery.schedules import crontab

   CELERY_BEAT_SCHEDULE = {
       "auto_archive_menu_items": {
           "task": "apps.access.tasks.auto_archive_menu_items",
           "schedule": crontab(hour=2, minute=0),  # diario UTC
       },
   }

11.7 Migracion para campos del lifecycle
========================================

Los campos ``deprecated_at``, ``archived_at`` y el cuarteto
``block_*`` son agregados en la migration de creacion del
modelo (``apps/access/migrations/0XXX_create_menuitem.py``)
junto con ``status``. Ver UC_ADM_04 §11.8 (no se duplica
aqui).
