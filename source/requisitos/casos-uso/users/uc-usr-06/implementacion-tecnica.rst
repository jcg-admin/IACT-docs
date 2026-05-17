.. _uc-usr-06-parte-10:

==========================================
Parte 10 — Implementacion tecnica
==========================================

10.1 Endpoint
==============

::

  POST /api/v1/users/{user_id}/unblock

  Authorization: Bearer <jwt>
  Content-Type: application/json

  body: { reason: string (1..500) }

10.2 Componentes
=================

Endpoint
--------

::

  class UnblockUserEndpoint(APIView):
      permission_classes = [IsAuthenticated, RequireFunctionPolicy]
      required_function = 'unblock_users'

      def post(self, request, user_id):
          serializer = UnblockUserRequestContract(data=request.data)
          serializer.is_valid(raise_exception=True)
          result = UnblockUserCommand(
              actor_id=request.user.id,
              target_user_id=user_id,
              reason=serializer.validated_data['reason'],
          ).execute()
          return Response(result.to_dict(), status=200)

10.3 Comando
=============

::

  class UnblockUserCommand:
      def execute(self) -> UnblockResult:
          with transaction.atomic():
              user = User.objects.select_for_update().get(
                  user_id=self.target_user_id
              )
              if user.state == 'ACTIVE':
                  return UnblockResult(already_unblocked=True, ...)
              if user.state == 'ELIMINATED':
                  raise UserEliminatedError()
              if user.state == 'INACTIVE':
                  raise InvalidStateTransitionError(
                      from_state='INACTIVE', to='ACTIVE',
                      use='UC_USR_03'
                  )
              if user.user_id == self.actor_id:
                  raise SelfUnblockForbiddenError()

              # lookup del bloqueo previo
              block_event = AuditEvent.objects.filter(
                  target_user_id=user.user_id,
                  event_type__in=[
                      'USER_BLOCKED',
                      'ACCOUNT_LOCKED',
                      'USER_BLOCK_REASON_OVERRIDE',
                  ],
              ).order_by('-occurred_at').first()
              if block_event is None:
                  AuditService.emit(
                      'USER_STATE_INCONSISTENCY',
                      target_user_id=user.user_id,
                      payload={'detected_in': 'UC_USR_06'},
                  )

              user.state = 'ACTIVE'
              user.save()

              AuditService.emit(
                  event_type='USER_UNBLOCKED',
                  actor_id=self.actor_id,
                  target_user_id=user.user_id,
                  payload={
                      'reason': self.reason,
                      'original_block_event_id':
                          block_event.event_id if block_event else None,
                      'original_block_type':
                          block_event.event_type if block_event else 'UNKNOWN',
                      'from_state': 'BLOCKED',
                  },
              )
              return UnblockResult(
                  user_id=user.user_id,
                  state='ACTIVE',
                  unblocked_at=user.updated_at,
                  original_block_event_id=
                      block_event.event_id if block_event else None,
              )

10.4 Estandares aplicables
===========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Estandar
   - Aplicacion
 * - CNST-009
   - JWT obligatorio.
 * - CNST-013
   - Excepciones canonicas: ``InvalidStateTransitionError →
     409``, ``UserEliminatedError → 409``, etc.
 * - CNST-025
   - AuditEvent dentro de la transaccion atomica.
 * - CNST-026
   - payload sin PII.
 * - STD-013
   - URL canonica ``/users/{id}/unblock``.

10.5 Componentes domain-model invocados
========================================

- ``User`` — read state, write state.
- ``AuditEvent`` — query (lookup block previo) + append
  (USER_UNBLOCKED).
- ``RequireFunctionPolicy`` — verificacion RBAC.
