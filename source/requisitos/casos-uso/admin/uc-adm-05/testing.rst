.. meta::
 :artefacto: UC_ADM_05_TEST
 :tipo: Caso de Uso (testing)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

============================
12. Testing
============================

12.1 Tests de transiciones (CA-01..CA-05)
=========================================

.. code-block:: python

   # apps/access/tests/test_uc_adm_05.py
   import pytest
   from datetime import timedelta
   from django.utils import timezone
   from rest_framework import status

   from apps.access.models import MenuItem, AuditEvent


   @pytest.mark.django_db
   def test_ca_01_publish(api_client_admin, menu_item_factory):
       mi = menu_item_factory(status="DRAFT")
       resp = api_client_admin.post(
           f"/api/v1/admin/menu-items/{mi.id}/publish/"
       )
       assert resp.status_code == 200
       mi.refresh_from_db()
       assert mi.status == "ACTIVE"
       assert mi.deprecated_at is None
       assert AuditEvent.objects.filter(
           event_type="MENU_ITEM_LIFECYCLE_TRANSITION",
       ).exists()


   @pytest.mark.django_db
   def test_ca_02_deprecate_sets_timestamp(
       api_client_admin, menu_item_factory,
   ):
       mi = menu_item_factory(status="ACTIVE")
       resp = api_client_admin.post(
           f"/api/v1/admin/menu-items/{mi.id}/deprecate/"
       )
       assert resp.status_code == 200
       mi.refresh_from_db()
       assert mi.status == "DEPRECATED"
       assert mi.deprecated_at is not None


   @pytest.mark.django_db
   def test_ca_03_reactivate_clears_fields(
       api_client_admin, menu_item_factory,
   ):
       mi = menu_item_factory(
           status="DEPRECATED",
           deprecated_at=timezone.now(),
           block_auto_archive=True,
           block_reason="X" * 25,
       )
       resp = api_client_admin.post(
           f"/api/v1/admin/menu-items/{mi.id}/reactivate/"
       )
       assert resp.status_code == 200
       mi.refresh_from_db()
       assert mi.status == "ACTIVE"
       assert mi.deprecated_at is None
       assert mi.block_auto_archive is False
       assert mi.block_reason == ""


   @pytest.mark.django_db
   def test_ca_04_archive_preserves_deprecated_at(
       api_client_admin, menu_item_factory,
   ):
       deprecated_when = timezone.now() - timedelta(days=10)
       mi = menu_item_factory(
           status="DEPRECATED",
           deprecated_at=deprecated_when,
       )
       resp = api_client_admin.post(
           f"/api/v1/admin/menu-items/{mi.id}/archive/"
       )
       assert resp.status_code == 200
       mi.refresh_from_db()
       assert mi.status == "ARCHIVED"
       assert mi.archived_at is not None
       assert mi.deprecated_at == deprecated_when


   @pytest.mark.django_db
   def test_ca_05_invalid_transition(
       api_client_admin, menu_item_factory,
   ):
       mi = menu_item_factory(status="DRAFT")
       resp = api_client_admin.post(
           f"/api/v1/admin/menu-items/{mi.id}/deprecate/"
       )
       assert resp.status_code == 409
       assert resp.data["error"] == "invalid_transition"

12.2 Tests de validacion (CA-06, CA-07)
=======================================

.. code-block:: python

   @pytest.mark.django_db
   def test_ca_06_publish_rejects_inactive_function(
       api_client_admin, menu_item_factory, function_factory,
   ):
       fn = function_factory(is_active=False)
       mi = menu_item_factory(status="DRAFT", function=fn)
       resp = api_client_admin.post(
           f"/api/v1/admin/menu-items/{mi.id}/publish/"
       )
       assert resp.status_code == 422
       assert resp.data["error"] == "function_inactive"


   @pytest.mark.django_db
   def test_ca_07_block_reason_too_short(
       api_client_admin, menu_item_factory,
   ):
       mi = menu_item_factory(status="DEPRECATED")
       resp = api_client_admin.post(
           f"/api/v1/admin/menu-items/{mi.id}/block-archive/",
           {"block_reason": "X"},  # < 20 chars
           format="json",
       )
       assert resp.status_code == 422

12.3 Tests del job (CA-08, CA-09, CA-10, CA-12)
===============================================

.. code-block:: python

   from freezegun import freeze_time

   from apps.access.tasks import auto_archive_menu_items


   @pytest.mark.django_db
   def test_ca_08_auto_archive_at_90d(menu_item_factory):
       with freeze_time("2026-08-01 02:00"):
           old = timezone.now() - timedelta(days=91)
           mi = menu_item_factory(status="DEPRECATED",
                                    deprecated_at=old)
           result = auto_archive_menu_items()
           assert result["archived"] == 1
           mi.refresh_from_db()
           assert mi.status == "ARCHIVED"
           assert AuditEvent.objects.filter(
               event_type="LIFECYCLE_AUTO_ARCHIVED",
               actor__username="system",
           ).exists()


   @pytest.mark.django_db
   def test_ca_09_block_prevents_auto_archive(
       menu_item_factory, mocker,
   ):
       notify = mocker.patch("apps.access.tasks.notify_admins")
       with freeze_time("2026-08-01 02:00"):
           old = timezone.now() - timedelta(days=91)
           mi = menu_item_factory(
               status="DEPRECATED",
               deprecated_at=old,
               block_auto_archive=True,
               block_reason="Auditoria pendiente Q3 trimestre",
           )
           result = auto_archive_menu_items()
           assert result["archived"] == 0
           mi.refresh_from_db()
           assert mi.status == "DEPRECATED"
           # Critical alert emitida
           call_args = [c.kwargs for c in notify.call_args_list]
           assert any(c["level"] == "CRITICAL" for c in call_args)


   @pytest.mark.django_db
   def test_ca_10_pre_archive_notification(
       menu_item_factory, mocker,
   ):
       notify = mocker.patch("apps.access.tasks.notify_admins")
       with freeze_time("2026-08-01 02:00"):
           when = timezone.now() - timedelta(days=82)
           menu_item_factory(status="DEPRECATED", deprecated_at=when)
           auto_archive_menu_items()
           call_args = [c.kwargs for c in notify.call_args_list]
           assert any(
               c["level"] == "WARNING"
               and "auto-archive en" in c["subject"]
               for c in call_args
           )


   @pytest.mark.django_db
   def test_ca_12_idempotency(menu_item_factory):
       with freeze_time("2026-08-01 02:00"):
           old = timezone.now() - timedelta(days=91)
           menu_item_factory(status="DEPRECATED", deprecated_at=old)
           r1 = auto_archive_menu_items()
           r2 = auto_archive_menu_items()
           assert r1["archived"] == 1
           assert r2["archived"] == 0  # ya esta ARCHIVED

12.4 Tests de visibilidad (CA-11)
=================================

.. code-block:: python

   @pytest.mark.django_db
   def test_ca_11_archived_invisible_in_endpoint(
       api_client_user_with_capability, menu_item_factory,
   ):
       mi = menu_item_factory(status="ARCHIVED",
                                function__codename="view_x")
       resp = api_client_user_with_capability("view_x").get(
           "/api/v1/menu/"
       )
       assert resp.status_code == 200
       codenames_in_items = [
           it["codename"] for it in resp.data["menu_items"]
       ]
       assert "view_x" not in codenames_in_items
       assert "view_x" in resp.data["capabilities"]
