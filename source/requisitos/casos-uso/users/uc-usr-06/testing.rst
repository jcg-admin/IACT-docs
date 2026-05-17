.. _uc-usr-06-parte-11:

==========================================
Parte 11 — Testing
==========================================

11.1 Cobertura
===============

Cubre los 12 criterios de aceptacion (CA-01..CA-12).

11.2 Estrategia por capa
=========================

Unit (UnblockUserCommand)
--------------------------

Pure unit tests sobre ``UnblockUserCommand.execute()``
con mocks de ``User`` y ``AuditService``.

Integration
-----------

Tests con BD efimera. Verifica cadena bloqueo→desbloqueo
end-to-end (UC_USR_05 + UC_USR_06).

E2E
---

Tests via test client invocando ``POST /users/{id}/unblock``.

11.3 Casos de test detallados
==============================

T-USR-06-01: Unblock nominal tras USER_BLOCKED previo
------------------------------------------------------

::

  def test_unblock_after_user_blocked():
      admin_blocker = UserTestData.create_admin(['block_users'])
      admin_unblocker = UserTestData.create_admin(['unblock_users'])
      target = UserTestData.create(state='ACTIVE')

      # block first
      block_resp = client.post(
          f'/users/{target.user_id}/block',
          {'reason': 'investigacion'},
          headers={'Authorization': admin_blocker.jwt()},
      )
      block_event_id = AuditEvent.objects.filter(
          event_type='USER_BLOCKED',
          target_user_id=target.user_id,
      ).first().event_id

      # then unblock
      unblock_resp = client.post(
          f'/users/{target.user_id}/unblock',
          {'reason': 'concluida sin sancion'},
          headers={'Authorization': admin_unblocker.jwt()},
      )

      assert unblock_resp.status_code == 200
      target.refresh_from_db()
      assert target.state == 'ACTIVE'
      unblock_event = AuditEvent.objects.filter(
          event_type='USER_UNBLOCKED',
          target_user_id=target.user_id,
      ).first()
      assert unblock_event.payload['original_block_event_id'] == \
          str(block_event_id)
      assert unblock_event.payload['original_block_type'] == \
          'USER_BLOCKED'

T-USR-06-02: Unblock tras ACCOUNT_LOCKED automatico
-----------------------------------------------------

::

  def test_unblock_after_account_locked():
      target = UserTestData.create(state='BLOCKED')
      AuditEventTestData.create(
          event_type='ACCOUNT_LOCKED',
          target_user_id=target.user_id,
      )
      ...
      assert unblock_event.payload['original_block_type'] == \
          'ACCOUNT_LOCKED'

T-USR-06-03: Idempotencia con User ACTIVE
------------------------------------------

::

  def test_unblock_already_active():
      target = UserTestData.create(state='ACTIVE')
      ...
      assert response.data['already_unblocked'] == True
      assert AuditEvent.objects.filter(
          event_type='USER_UNBLOCKED',
          target_user_id=target.user_id,
      ).count() == 0

T-USR-06-04: User ELIMINATED rechaza desbloqueo
-------------------------------------------------

::

  def test_unblock_eliminated_returns_409():
      target = UserTestData.create(state='ELIMINATED')
      ...
      assert response.status_code == 409
      assert response.data['error'] == 'USER_ELIMINATED'

T-USR-06-05: User INACTIVE rechaza con guidance
-------------------------------------------------

::

  def test_unblock_inactive_returns_409_invalid_transition():
      target = UserTestData.create(state='INACTIVE')
      ...
      assert response.status_code == 409
      assert response.data['error'] == 'INVALID_STATE_TRANSITION'
      assert response.data['use'] == 'UC_USR_03'

T-USR-06-06: Estado inconsistente sin block previo
----------------------------------------------------

::

  def test_unblock_blocked_state_without_audit_history():
      target = UserTestData.create(state='BLOCKED')
      # no AuditEvent USER_BLOCKED ni ACCOUNT_LOCKED previos
      ...
      assert response.status_code == 200
      assert AuditEvent.objects.filter(
          event_type='USER_STATE_INCONSISTENCY',
          target_user_id=target.user_id,
      ).exists()
      assert AuditEvent.objects.filter(
          event_type='USER_UNBLOCKED',
          target_user_id=target.user_id,
      ).first().payload['original_block_event_id'] is None

T-USR-06-07: Login post-unblock funciona
------------------------------------------

::

  def test_login_after_unblock():
      target = UserTestData.create(state='BLOCKED')
      # unblock first
      client.post(f'/users/{target.user_id}/unblock', ...)
      # login
      login = client.post(
          '/auth/login',
          {'username': target.username, 'password': '...'},
      )
      assert login.status_code == 200
      assert Session.objects.filter(
          user_id=target.user_id, state='ACTIVE'
      ).exists()

11.4 Coverage objetivo
=======================

- ``UnblockUserEndpoint``: ≥ 95%.
- ``UnblockUserCommand``: 100%.
