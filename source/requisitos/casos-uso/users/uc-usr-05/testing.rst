.. _uc-usr-05-parte-11:

==========================================
Parte 11 — Testing
==========================================

11.1 Cobertura
===============

UC_USR_05 requiere cobertura sobre:

- Flujo nominal completo (CA-01)
- Idempotencia logica (CA-02)
- Estados origen permitidos (CA-03 INACTIVE)
- Excepciones cada una (CA-04..CA-08)
- Atomicidad ante fallo (CA-09)
- Override de razon (CA-10)

Total: 10 escenarios minimum, ~15 con variaciones.

11.2 Estrategia por capa
=========================

Unit (BlockUserCommand)
------------------------

Pure unit tests sobre ``BlockUserCommand.execute()`` con
mocks de ``User``, ``Session``, ``BlacklistedToken``,
``AuditService``. Verifica logica de transicion sin BD
real.

Integration (DB)
----------------

Tests con BD sqlite efimera. Verifica que la transaccion
atomica funciona end-to-end: state escrito, sesiones
cerradas, tokens blacklistados, AuditEvent persistido.

E2E (HTTP)
----------

Tests via Django test client invocando
``POST /users/{id}/block`` con JWT valido. Verifica
respuesta HTTP, status code, body y side-effects en BD.

11.3 Casos de test detallados
==============================

T-USR-05-01: Bloqueo nominal
-----------------------------

::

  def test_block_active_user_with_sessions_and_tokens():
      admin = UserTestData.create_admin(['block_users'])
      target = UserTestData.create(state='ACTIVE')
      sessions = SessionTestData.create_batch(target, 2)
      tokens = TokenTestData.create_refresh_batch(target, 3)

      response = client.post(
          f'/api/v1/users/{target.user_id}/block',
          {'reason': 'investigacion ABC-123'},
          headers={'Authorization': f'Bearer {admin.jwt()}'},
      )

      assert response.status_code == 200
      target.refresh_from_db()
      assert target.state == 'BLOCKED'
      assert Session.objects.filter(
          user_id=target.user_id, state='CLOSED'
      ).count() == 2
      assert BlacklistedToken.objects.filter(
          user_id=target.user_id
      ).count() == 3
      assert AuditEvent.objects.filter(
          event_type='USER_BLOCKED',
          target_user_id=target.user_id
      ).exists()

T-USR-05-02: Idempotencia
--------------------------

::

  def test_block_already_blocked_user():
      target = UserTestData.create(state='BLOCKED')
      ...
      assert response.status_code == 200
      assert response.data['already_blocked'] == True
      assert AuditEvent.objects.filter(
          event_type='USER_BLOCKED',
          target_user_id=target.user_id
      ).count() == 0  # no nuevo evento

T-USR-05-03: Permission denied
-------------------------------

::

  def test_block_without_function_returns_403():
      admin_no_func = UserTestData.create_admin(['view_users'])
      target = UserTestData.create()
      response = client.post(
          f'/api/v1/users/{target.user_id}/block',
          ...
      )
      assert response.status_code == 403
      assert AuditEvent.objects.filter(
          event_type='ACCESS_DENIED'
      ).exists()

T-USR-05-04: Auto-bloqueo
--------------------------

::

  def test_self_block_forbidden():
      admin = UserTestData.create_admin(['block_users'])
      response = client.post(
          f'/api/v1/users/{admin.user_id}/block',
          ...
      )
      assert response.status_code == 409
      assert response.data['error'] == 'SELF_BLOCK_FORBIDDEN'

T-USR-05-05: User ELIMINATED prohibido
---------------------------------------

::

  def test_block_eliminated_user_returns_409():
      target = UserTestData.create(state='ELIMINATED')
      ...
      assert response.status_code == 409
      assert response.data['error'] == 'USER_ELIMINATED'

T-USR-05-06: Atomicidad de fallo
---------------------------------

::

  def test_block_rollback_on_audit_failure(monkeypatch):
      target = UserTestData.create(state='ACTIVE')
      monkeypatch.setattr(
          AuditService, 'emit',
          lambda *a,**kw: raise_audit_failure()
      )
      response = client.post(...)
      assert response.status_code == 500
      target.refresh_from_db()
      assert target.state == 'ACTIVE'  # rollback

11.4 Coverage objetivo
=======================

- ``BlockUserEndpoint``: ≥ 95%.
- ``BlockUserCommand``: 100%.
- Lineas de transicion atomica: 100%.
