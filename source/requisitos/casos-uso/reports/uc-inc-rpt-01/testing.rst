.. _uc-inc-rpt-01-parte-12:

==============================
Parte 12 — Testing
==============================

Mapeo CA → test case (pytest + pytest-django).

12.1 Tests unitarios
====================

.. code-block:: python

   # apps/reports/tests/test_uc_inc_rpt_01.py
   import pytest
   from django.core.cache import cache, CacheError

   from apps.reports.services.segment_resolver import (
       SegmentResolver,
       NoSegmentAssignedError,
   )


   @pytest.mark.django_db
   def test_ca_01_user_with_one_segment(user_factory):
       """CA-01: resolucion para usuario con un segmento."""
       user = user_factory(segment_id=1)
       segments = SegmentResolver.resolve(user)
       assert segments == {1}
       assert SegmentResolver.is_global(user) is False


   @pytest.mark.django_db
   def test_ca_02_user_with_global_capability(user_factory):
       """CA-02: resolucion para usuario con view_all_segments."""
       user = user_factory(capabilities={"view_all_segments"})
       segments = SegmentResolver.resolve(user)
       assert segments == {1, 2, 3}
       assert SegmentResolver.is_global(user) is True


   @pytest.mark.django_db
   def test_ca_03_user_without_segment_no_capability(user_factory):
       """CA-03: rechazo de usuario sin segmento ni capability."""
       user = user_factory(segment_id=None, capabilities=set())
       with pytest.raises(NoSegmentAssignedError):
           SegmentResolver.resolve(user)


   @pytest.mark.django_db
   def test_ca_04_cache_hit_reduces_latency(user_factory, benchmark):
       """CA-04: cache HIT P50 <= 5ms."""
       user = user_factory(segment_id=1)
       SegmentResolver.resolve(user)  # warm cache
       result = benchmark(SegmentResolver.resolve, user)
       assert benchmark.stats["median"] < 0.005  # 5ms


   @pytest.mark.django_db
   def test_ca_05_cache_invalidation_on_rbac_change(user_factory):
       """CA-05: cache invalidado tras cambio de capabilities."""
       user = user_factory(segment_id=1)
       SegmentResolver.resolve(user)
       cache_key = f"segments:user:{user.id}"
       assert cache.get(cache_key) == {1}

       # Simular cambio RBAC via helper de invalidacion
       SegmentResolver.invalidate_cache(user.id)
       assert cache.get(cache_key) is None


   @pytest.mark.django_db
   def test_ca_06_repository_failure_no_cache_update(
       user_factory, mocker,
   ):
       """CA-06: falla del repositorio no contamina cache."""
       user = user_factory(segment_id=1)
       mocker.patch.object(
           SegmentResolver, "_query_db",
           side_effect=ConnectionError("timeout"),
       )
       with pytest.raises(ConnectionError):
           SegmentResolver.resolve(user)
       assert cache.get(f"segments:user:{user.id}") is None


   @pytest.mark.django_db
   def test_ca_07_br_012_segment_id_permanent(user_factory):
       """CA-07: BR-012 — segment_id permanente, no switchable."""
       user = user_factory(segment_id=1)
       segments_before = SegmentResolver.resolve(user)
       # No mecanismo runtime para cambiar segment_id
       # (preserved by FK NOT NULL + no UC de cambio).
       assert user.segment_id == 1
       assert segments_before == {1}


   @pytest.mark.django_db
   def test_ca_08_intra_request_memoization(user_factory, mocker):
       """CA-08: memoizacion intra-request."""
       user = user_factory(segment_id=1)
       spy = mocker.spy(SegmentResolver, "_query_db")
       # Simular varias invocaciones en el mismo request
       SegmentResolver.resolve(user, request_scope=True)
       SegmentResolver.resolve(user, request_scope=True)
       SegmentResolver.resolve(user, request_scope=True)
       assert spy.call_count == 1  # solo una vez

12.2 Tests de integracion con UC_RPT_xx
========================================

.. code-block:: python

   @pytest.mark.django_db
   def test_uc_rpt_14_includes_segment_resolution(api_client_user):
       """UC_RPT_14 invoca UC_INC_RPT_01 antes de la query."""
       resp = api_client_user.get("/api/v1/reports/abandono/")
       assert resp.status_code == 200
       # Datos solo del segmento del usuario
       segments_in_data = {row["segment_id"] for row in resp.data["rows"]}
       assert segments_in_data == {api_client_user.user.segment_id}


   @pytest.mark.django_db
   def test_uc_rpt_17_global_user_sees_all_segments(
       api_client_user_with_capability,
   ):
       """User con view_all_segments ve datos de todos los segmentos."""
       client = api_client_user_with_capability("view_all_segments")
       resp = client.get("/api/v1/reports/comparativo/")
       assert resp.status_code == 200
       segments_in_data = {row["segment_id"] for row in resp.data["rows"]}
       assert segments_in_data == {1, 2, 3}

12.3 Tests de performance
=========================

.. code-block:: python

   @pytest.mark.django_db
   def test_resolution_p50_under_50ms(user_factory, benchmark):
       """Cache MISS P50 <= 50ms."""
       user = user_factory(segment_id=1)
       cache.clear()
       result = benchmark(SegmentResolver.resolve, user)
       assert benchmark.stats["median"] < 0.050  # 50ms

12.4 Tests de auditabilidad
===========================

.. code-block:: python

   @pytest.mark.django_db
   def test_failure_emits_audit_event(user_factory, mocker):
       """CA-06: SEGMENT_RESOLUTION_FAILED en falla."""
       user = user_factory(segment_id=1)
       mocker.patch.object(
           SegmentResolver, "_query_db",
           side_effect=ConnectionError("timeout"),
       )
       with pytest.raises(ConnectionError):
           SegmentResolver.resolve(user)
       assert AuditEvent.objects.filter(
           event_type="SEGMENT_RESOLUTION_FAILED",
           actor=user,
       ).exists()
