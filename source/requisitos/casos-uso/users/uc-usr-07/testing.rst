.. _uc-usr-07-parte-11:

==========================================
Parte 11 — Testing
==========================================

11.1 Cobertura
===============

Cubre los 13 criterios de aceptacion (CA-01..CA-13).

11.2 Estrategia por capa
=========================

Unit
-----

Pure unit tests sobre ``UpdateOwnProfileCommand`` y
``EmailValidator``.

Integration
-----------

Tests con BD efimera. Verifica que UPDATE + AuditEvent
ocurren atomicamente.

E2E
---

Tests via test client invocando ``PATCH /users/me``.

11.3 Casos de test detallados
==============================

T-USR-07-01: Edicion completa
------------------------------

::

  def test_update_profile_full_name_and_email():
      user = UserTestData.create(
          state='ACTIVE',
          full_name='Old Name',
          email='old@example.com',
      )
      response = client.patch(
          '/api/v1/users/me',
          {'full_name': 'New Name', 'email': 'new@example.com'},
          headers={'Authorization': user.jwt()},
      )
      assert response.status_code == 200
      user.refresh_from_db()
      assert user.full_name == 'New Name'
      assert user.email == 'new@example.com'
      audit = AuditEvent.objects.filter(
          event_type='PROFILE_UPDATED',
          actor_id=user.user_id,
      ).first()
      assert sorted(audit.payload['fields_changed']) == \
          ['email', 'full_name']
      assert 'New Name' not in audit.payload  # no PII
      assert 'new@example.com' not in audit.payload

T-USR-07-02: Edicion parcial — solo full_name
-----------------------------------------------

::

  def test_update_only_full_name_preserves_email():
      user = UserTestData.create(
          full_name='Old', email='preserved@x.com',
      )
      response = client.patch(
          '/api/v1/users/me', {'full_name': 'New'}, ...
      )
      assert response.status_code == 200
      user.refresh_from_db()
      assert user.email == 'preserved@x.com'
      audit = AuditEvent.objects.filter(...).first()
      assert audit.payload['fields_changed'] == ['full_name']

T-USR-07-03: Idempotencia — payload identico
----------------------------------------------

::

  def test_no_op_when_payload_matches_current():
      user = UserTestData.create(full_name='X')
      response = client.patch(
          '/api/v1/users/me', {'full_name': 'X'}, ...
      )
      assert response.status_code == 200
      assert response.data['no_changes'] == True
      assert AuditEvent.objects.filter(
          event_type='PROFILE_UPDATED',
          actor_id=user.user_id,
      ).count() == 0

T-USR-07-04: Email duplicado
-----------------------------

::

  def test_email_unique_constraint():
      other = UserTestData.create(email='other@x.com')
      user = UserTestData.create(email='mine@x.com')
      response = client.patch(
          '/api/v1/users/me',
          {'email': 'other@x.com'}, ...
      )
      assert response.status_code == 409
      assert response.data['error'] == 'EMAIL_ALREADY_TAKEN'

T-USR-07-05: Email formato invalido
-------------------------------------

::

  def test_email_format_validation():
      response = client.patch(
          '/api/v1/users/me',
          {'email': 'no-at-sign'}, ...
      )
      assert response.status_code == 400
      assert response.data['error'] == 'INVALID_EMAIL_FORMAT'

T-USR-07-06: Campo prohibido (escalation attempt)
---------------------------------------------------

::

  def test_forbidden_field_blocks_escalation():
      user = UserTestData.create()
      response = client.patch(
          '/api/v1/users/me',
          {'primary_access_group_id': 'admin-group-uuid'}, ...
      )
      assert response.status_code == 400
      assert response.data['error'] == 'FORBIDDEN_FIELD'
      user.refresh_from_db()
      assert user.primary_access_group_id != 'admin-group-uuid'

T-USR-07-07: Cannot edit other user
-------------------------------------

::

  def test_cannot_edit_other_user():
      attacker = UserTestData.create()
      victim = UserTestData.create(full_name='Victim')
      # there is no /users/{victim_id} endpoint for self-edit
      # assert no route exists OR returns 404
      response = client.patch(
          f'/api/v1/users/{victim.user_id}',
          {'full_name': 'Hacked'},
          headers={'Authorization': attacker.jwt()},
      )
      assert response.status_code in (403, 404)
      victim.refresh_from_db()
      assert victim.full_name == 'Victim'

T-USR-07-08: Sesion permanece vigente
---------------------------------------

::

  def test_session_persists_after_update():
      user = UserTestData.create(state='ACTIVE')
      session = SessionTestData.create_active(user)
      client.patch(
          '/api/v1/users/me',
          {'full_name': 'X'},
          headers={'Authorization': user.jwt()},
      )
      session.refresh_from_db()
      assert session.state == 'ACTIVE'

11.4 Coverage objetivo
=======================

- ``UpdateOwnProfileEndpoint``: ≥ 95%.
- ``UpdateOwnProfileCommand``: 100%.
- ``EmailValidator``: 100%.
