.. meta::
 :artefacto: UC_ADM_04_IMPL
 :tipo: Caso de Uso (implementacion tecnica)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

================================
11. Implementacion Tecnica
================================

.. note::

   Esta seccion es **libre de STD-010** — puede mencionar
   tecnologias concretas. Las secciones anteriores usan
   vocabulario canonico.

11.1 Stack
==========

- Backend: Django 5.0+ con Django REST Framework.
- Almacen de Datos: PostgreSQL 14+.
- Servicio de Cache: Redis 7.x con ``django-redis``.
- Audit log: tabla dedicada ``audit_events`` (append-only).
- Tests: pytest + pytest-django.

11.2 Endpoints DRF
==================

.. code-block:: python

   # apps/access/urls.py
   from rest_framework.routers import DefaultRouter
   from .views import MenuItemAdminEndpoints, MenuItemBulkReorderView

   router = DefaultRouter()
   router.register(r"admin/menu-items", MenuItemAdminEndpoints,
                   basename="admin-menu-items")

   urlpatterns = router.urls + [
       path("admin/menu-items/bulk-reorder/",
            MenuItemBulkReorderView.as_view(),
            name="admin-menu-items-bulk-reorder"),
   ]

11.3 ViewSet
============

.. code-block:: python

   # apps/access/views.py
   from rest_framework.viewsets import ModelViewSet
   from rest_framework.permissions import IsAuthenticated

   from .models import MenuItem
   from .serializers import MenuItemAdminSerializer
   from .permissions import HasCriticalCapability


   class MenuItemAdminEndpoints(ModelViewSet):
       queryset = MenuItem.objects.select_related("function", "parent")
       serializer_class = MenuItemAdminSerializer
       permission_classes = [IsAuthenticated,
                             HasCriticalCapability("manage_menu_catalog")]
       filterset_fields = ["status", "function__module"]
       ordering_fields = ["display_order", "created_at"]
       pagination_class = StandardResultsSetPagination

       def perform_create(self, serializer):
           with transaction.atomic():
               instance = serializer.save(created_by=self.request.user)
               record_audit_event(
                   "MENU_ITEM_CREATED",
                   actor=self.request.user,
                   menu_item=instance,
                   snapshot=serializer.data,
               )
               transaction.on_commit(
                   lambda: invalidate_menu_for_function(instance.function_id)
               )

11.4 Permission class custom
============================

.. code-block:: python

   # apps/access/permissions.py
   from rest_framework.permissions import BasePermission

   from .resolvers import UserCapabilityResolver


   class HasCriticalCapability(BasePermission):
       """Verifica capability con bypass de cache (AP-2b)."""
       def __init__(self, codename: str):
           self.codename = codename

       def has_permission(self, request, view):
           if not request.user.is_authenticated:
               return False
           return UserCapabilityResolver.has_capability(
               request.user, self.codename,
           )

11.5 Helper de invalidacion
===========================

.. code-block:: python

   # apps/access/cache.py
   from django.contrib.auth import get_user_model

   def invalidate_menu_for_function(function_id: int) -> None:
       """Invalida cache de menu para users con la Function."""
       User = get_user_model()
       user_ids = (
           User.objects
           .filter(useraccessgroupassignment__group__functiongroupmembership__function_id=function_id)
           .values_list("id", flat=True)
           .distinct()
       )
       for uid in user_ids:
           try:
               cache.delete(f"menu:user:{uid}")
               cache.delete(f"caps:user:{uid}")
           except CacheError as exc:
               logger.error("cache_invalidation_failed",
                              extra={"user_id": uid, "exc": str(exc)})

11.6 Bulk reorder
=================

.. code-block:: python

   from django.db.models import Case, When, Value, IntegerField

   class MenuItemBulkReorderView(APIView):
       permission_classes = [IsAuthenticated,
                             HasCriticalCapability("manage_menu_catalog")]

       def patch(self, request):
           items = request.data  # [{"id": 12, "display_order": 10}, ...]
           ids = [it["id"] for it in items]
           with transaction.atomic():
               existing = set(MenuItem.objects.filter(id__in=ids)
                                              .values_list("id", flat=True))
               if set(ids) - existing:
                   return Response(status=422)
               cases = Case(*[
                   When(id=it["id"], then=Value(it["display_order"]))
                   for it in items
               ], output_field=IntegerField())
               MenuItem.objects.filter(id__in=ids).update(
                   display_order=cases
               )
               record_audit_event(
                   "MENU_ITEM_BULK_REORDERED",
                   actor=request.user, changes=items,
               )
               transaction.on_commit(
                   lambda: invalidate_menu_for_items(ids)
               )
           return Response({"updated": len(items)})

11.7 Audit event
================

.. code-block:: python

   # apps/access/audit.py
   def record_audit_event(event_type, actor, **payload):
       AuditEvent.objects.create(
           event_type=event_type,
           actor=actor,
           timestamp=timezone.now(),
           payload=payload,  # JSONField
       )

11.8 Migracion Django
=====================

.. code-block:: python

   # apps/access/migrations/0XXX_create_menuitem.py
   class Migration(migrations.Migration):
       dependencies = [("access", "0XX_function_is_critical")]
       operations = [
           migrations.CreateModel(
               name="MenuItem",
               fields=[
                   ("id", models.BigAutoField(primary_key=True)),
                   ("function", models.OneToOneField(
                       to="access.Function",
                       on_delete=models.PROTECT,
                       related_name="menu_item")),
                   # ... resto de campos ...
               ],
               options={
                   "db_table": "menu_items",
                   "ordering": ("display_order",),
               },
           ),
           migrations.AddIndex(model_name="MenuItem",
               index=models.Index(fields=["status"],
                                    name="menu_items_status_idx")),
           migrations.AddIndex(model_name="MenuItem",
               index=models.Index(fields=["status", "display_order"],
                                    name="menu_items_status_order_idx")),
           migrations.AddIndex(model_name="MenuItem",
               index=models.Index(fields=["deprecated_at"],
                                    name="menu_items_deprec_idx")),
       ]
