.. meta::
 :artefacto: UC_ADM_04_TEST
 :tipo: Caso de Uso (testing)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

============================
12. Testing
============================

Mapeo CA → test (pytest + pytest-django).

12.1 Tests unitarios y de integracion
=====================================

.. code-block:: python

   # apps/access/tests/test_uc_adm_04.py
   import pytest
   from django.urls import reverse
   from rest_framework import status
   from rest_framework.test import APIClient
   from django.core.cache import cache, CacheError

   from apps.access.models import MenuItem, Function, AuditEvent


   @pytest.mark.django_db
   def test_ca_01_create_with_defaults(api_client_admin, function_factory):
       """CA-01: CREATE exitoso con defaults."""
       fn = function_factory(codename="view_reports", is_active=True)
       resp = api_client_admin.post(
           "/api/v1/admin/menu-items/",
           {"function_id": fn.id,
            "display_label": "Mis Reportes",
            "icon": "BarChartIcon",
            "route_path": "/reports"},
           format="json",
       )
       assert resp.status_code == status.HTTP_201_CREATED
       assert resp.data["status"] == "DRAFT"
       assert resp.data["deprecated_at"] is None
       assert AuditEvent.objects.filter(
           event_type="MENU_ITEM_CREATED").exists()


   @pytest.mark.django_db
   def test_ca_02_create_rejected_without_capability(api_client_user, function_factory):
       """CA-02: CREATE rechazo por capability ausente."""
       fn = function_factory(codename="view_reports")
       resp = api_client_user.post(
           "/api/v1/admin/menu-items/",
           {"function_id": fn.id,
            "display_label": "X", "route_path": "/x"},
           format="json",
       )
       assert resp.status_code == status.HTTP_403_FORBIDDEN
       assert AuditEvent.objects.filter(
           event_type="CAPABILITY_DENIED").exists()


   @pytest.mark.django_db
   def test_ca_03_create_rejected_inactive_function(api_client_admin, function_factory):
       """CA-03: rechazo por Function inactiva."""
       fn = function_factory(codename="view_x", is_active=False)
       resp = api_client_admin.post(
           "/api/v1/admin/menu-items/",
           {"function_id": fn.id,
            "display_label": "X", "route_path": "/x"},
           format="json",
       )
       assert resp.status_code == 422


   @pytest.mark.django_db
   def test_ca_04_i1_violation(api_client_admin, function_factory, menu_item_factory):
       """CA-04: I-1 violation — Function ya con MenuItem."""
       fn = function_factory(codename="view_x")
       menu_item_factory(function=fn)
       resp = api_client_admin.post(
           "/api/v1/admin/menu-items/",
           {"function_id": fn.id,
            "display_label": "Otro", "route_path": "/x"},
           format="json",
       )
       assert resp.status_code == status.HTTP_409_CONFLICT
       assert "existing_menu_item_id" in resp.data


   @pytest.mark.django_db
   def test_ca_05_update_display_label(api_client_admin, menu_item_factory):
       """CA-05: UPDATE de display_label con audit."""
       mi = menu_item_factory(display_label="Antes", status="ACTIVE")
       resp = api_client_admin.patch(
           f"/api/v1/admin/menu-items/{mi.id}/",
           {"display_label": "Despues"},
           format="json",
       )
       assert resp.status_code == 200
       mi.refresh_from_db()
       assert mi.display_label == "Despues"
       audit = AuditEvent.objects.get(event_type="MENU_ITEM_UPDATED")
       assert audit.payload["before_state"]["display_label"] == "Antes"
       assert audit.payload["after_state"]["display_label"] == "Despues"


   @pytest.mark.django_db
   def test_ca_06_update_blocked_in_archived(api_client_admin, menu_item_factory):
       """CA-06: UPDATE bloqueado en ARCHIVED."""
       mi = menu_item_factory(status="ARCHIVED")
       resp = api_client_admin.patch(
           f"/api/v1/admin/menu-items/{mi.id}/",
           {"display_label": "X"}, format="json",
       )
       assert resp.status_code == 409


   @pytest.mark.django_db
   def test_ca_07_list_with_filters(api_client_admin, menu_item_factory):
       """CA-07: LIST con filtros status + module."""
       menu_item_factory(status="DRAFT", function__module="ADM")
       menu_item_factory(status="ACTIVE", function__module="ADM")
       menu_item_factory(status="DRAFT", function__module="RPT")
       resp = api_client_admin.get(
           "/api/v1/admin/menu-items/?status=DRAFT&function__module=ADM"
       )
       assert resp.status_code == 200
       assert resp.data["count"] == 1


   @pytest.mark.django_db
   def test_ca_08_bulk_reorder_atomic(api_client_admin, menu_item_factory):
       """CA-08: bulk reorder atomico."""
       items = [menu_item_factory(display_order=i) for i in range(5)]
       payload = [{"id": items[i].id,
                   "display_order": (i + 1) * 100}
                  for i in range(5)]
       resp = api_client_admin.patch(
           "/api/v1/admin/menu-items/bulk-reorder/",
           payload, format="json",
       )
       assert resp.status_code == 200
       for i, mi in enumerate(items):
           mi.refresh_from_db()
           assert mi.display_order == (i + 1) * 100
       assert AuditEvent.objects.filter(
           event_type="MENU_ITEM_BULK_REORDERED").count() == 1


   @pytest.mark.django_db
   def test_ca_09_cache_fail_does_not_block(api_client_admin, function_factory, mocker):
       """CA-09: cache fail no bloquea operacion."""
       fn = function_factory(codename="view_x", is_active=True)
       mocker.patch.object(cache, "delete", side_effect=CacheError)
       resp = api_client_admin.post(
           "/api/v1/admin/menu-items/",
           {"function_id": fn.id,
            "display_label": "X", "route_path": "/x"},
           format="json",
       )
       assert resp.status_code == 201
       assert AuditEvent.objects.filter(
           event_type="CACHE_INVALIDATION_FAILED").exists()


   @pytest.mark.django_db
   def test_ca_10_capability_bypass_real(api_client_admin, function_factory, user_admin):
       """CA-10: bypass real, no stale tras revocar."""
       cache.set(f"caps:user:{user_admin.id}",
                 {"manage_menu_catalog"}, timeout=300)
       UserAccessGroupAssignment.objects.filter(
           user=user_admin).delete()
       fn = function_factory(codename="view_x", is_active=True)
       resp = api_client_admin.post(
           "/api/v1/admin/menu-items/",
           {"function_id": fn.id,
            "display_label": "X", "route_path": "/x"},
           format="json",
       )
       # Capability revocada → bypass detecta sin esperar TTL
       assert resp.status_code == 403

12.2 Tests de invariantes (I-1..I-4)
====================================

Heredados de ``test_menu_item.py`` (definidos en
ADR-BACK-008 §6.2). UC_ADM_04 NO duplica esos tests, pero
los referencia como prerequisito de aceptacion.

12.3 Tests de performance
=========================

.. code-block:: python

   @pytest.mark.django_db
   def test_create_p50_under_200ms(api_client_admin, function_factory,
                                       benchmark):
       fn = function_factory(codename="view_x", is_active=True)
       def create():
           return api_client_admin.post(
               "/api/v1/admin/menu-items/",
               {"function_id": fn.id,
                "display_label": "X", "route_path": "/x"},
               format="json",
           )
       result = benchmark(create)
       assert benchmark.stats["median"] < 0.2  # 200ms
