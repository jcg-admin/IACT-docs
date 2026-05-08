.. _uc-usr-05-parte-10:

==========================================
Parte 10 — Implementacion tecnica
==========================================

10.1 Endpoint
==============

::

  POST /api/v1/users/{user_id}/block

  Authorization: Bearer <jwt>
  Content-Type: application/json

  body: { reason: string (1..500) }

10.2 Componentes
=================

Endpoint (DRF view class)
--------------------------

``BlockUserEndpoint(APIView)``: orquesta la operacion.

::

  class BlockUserEndpoint(APIView):
      permission_classes = [IsAuthenticated, RequireFunctionPolicy]
      required_function = 'block_users'

      def post(self, request, user_id):
          serializer = BlockUserRequestContract(data=request.data)
          serializer.is_valid(raise_exception=True)
          result = BlockUserCommand(
              actor_id=request.user.id,
              target_user_id=user_id,
              reason=serializer.validated_data['reason'],
          ).execute()
          return Response(result.to_dict(), status=200)

10.3 Comando
=============

``BlockUserCommand`` encapsula la transaccion atomica:

::

  class BlockUserCommand:
      def execute(self) -> BlockResult:
          with transaction.atomic():
              user = User.objects.select_for_update().get(
                  user_id=self.target_user_id
              )
              self._validate_state(user)
              if user.state == 'BLOCKED':
                  return BlockResult(already_blocked=True, ...)
              if user.state == 'ELIMINATED':
                  raise UserEliminatedError()
              if user.user_id == self.actor_id:
                  raise SelfBlockForbiddenError()

              from_state = user.state
              user.state = 'BLOCKED'
              user.save()

              sessions_closed = Session.objects.filter(
                  user_id=user.user_id, state='ACTIVE'
              ).update(
                  state='CLOSED',
                  close_reason='USER_BLOCKED',
                  closed_at=now(),
              )
              tokens_blacklisted = self._blacklist_tokens(user)

              AuditService.emit(
                  event_type='USER_BLOCKED',
                  actor_id=self.actor_id,
                  target_user_id=user.user_id,
                  payload={
                      'reason': self.reason,
                      'from_state': from_state,
                      'sessions_closed_count': sessions_closed,
                      'tokens_blacklisted_count': tokens_blacklisted,
                  },
              )
              return BlockResult(
                  user_id=user.user_id,
                  state='BLOCKED',
                  blocked_at=user.updated_at,
                  sessions_closed_count=sessions_closed,
                  tokens_blacklisted_count=tokens_blacklisted,
              )

10.4 Estandares aplicables
===========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Estandar
   - Aplicacion
 * - CNST-009
   - Endpoint detras de IsAuthenticated; JWT obligatorio.
 * - CNST-013
   - Excepciones canonicas mapeadas:
     ``UserEliminatedError → 409``,
     ``SelfBlockForbiddenError → 409``,
     ``UserNotFoundError → 404``,
     ``PermissionDeniedError → 403``.
 * - CNST-025
   - AuditEvent dentro de la misma transaccion atomica.
     Si AuditService.emit falla, rollback.
 * - CNST-026
   - payload de AuditEvent NO incluye email ni full_name.
 * - STD-013
   - URL canonica: sustantivo + sub-accion ``/users/{id}/block``.
 * - STD-008
   - identifier ``BlockUserEndpoint``, ``BlockUserCommand``,
     ``RequireFunctionPolicy``.

10.5 Componentes domain-model invocados
========================================

- ``User`` — read state, write state.
- ``Session`` — bulk update.
- ``BlacklistedToken`` — bulk insert.
- ``AuditEvent`` (via ``AuditService.emit``) — append.
- ``RequireFunctionPolicy`` — verificacion RBAC.
