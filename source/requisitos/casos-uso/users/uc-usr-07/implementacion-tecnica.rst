.. _uc-usr-07-parte-10:

==========================================
Parte 10 — Implementacion tecnica
==========================================

10.1 Endpoint
==============

::

  PATCH /api/v1/users/me

  Authorization: Bearer <jwt>
  Content-Type: application/json

  body: { full_name?: string, email?: string }

URL canonica per STD-013: ``/users/me`` es el
"yo-recurso" del User autenticado; el endpoint NO usa
``user_id`` en URL para evitar confusion con UC_USR_03.

10.2 Componentes
=================

Endpoint
--------

::

  class UpdateOwnProfileEndpoint(APIView):
      permission_classes = [IsAuthenticated, RequireFunctionPolicy]
      required_function = 'edit_own_profile'

      EDITABLE_FIELDS = {'full_name', 'email'}

      def patch(self, request):
          serializer = UpdateOwnProfileRequestContract(data=request.data)
          serializer.is_valid(raise_exception=True)
          self._validate_no_forbidden_fields(request.data)
          result = UpdateOwnProfileCommand(
              actor_id=request.user.id,
              patch=serializer.validated_data,
          ).execute()
          return Response(result.to_dict(), status=200)

      def _validate_no_forbidden_fields(self, data):
          forbidden = set(data.keys()) - self.EDITABLE_FIELDS
          if forbidden:
              raise ForbiddenFieldError(forbidden)

10.3 Comando
=============

::

  class UpdateOwnProfileCommand:
      def execute(self) -> UpdateResult:
          if not self.patch:
              raise EmptyPayloadError()

          with transaction.atomic():
              user = User.objects.select_for_update().get(
                  user_id=self.actor_id
              )
              if user.state != 'ACTIVE':
                  raise InvalidStateError(state=user.state)

              # detect diff
              fields_changed = []
              for field, new_value in self.patch.items():
                  if getattr(user, field) != new_value:
                      fields_changed.append(field)

              if not fields_changed:
                  return UpdateResult(no_changes=True, ...)

              if 'email' in fields_changed:
                  EmailValidator.validate_format(self.patch['email'])
                  EmailValidator.validate_unique(
                      self.patch['email'],
                      exclude_user_id=user.user_id,
                  )

              for field in fields_changed:
                  setattr(user, field, self.patch[field])
              user.save()

              AuditService.emit(
                  event_type='PROFILE_UPDATED',
                  actor_id=user.user_id,
                  target_user_id=user.user_id,
                  payload={'fields_changed': fields_changed},
              )
              return UpdateResult(
                  user_id=user.user_id,
                  full_name=user.full_name,
                  email=user.email,
                  updated_at=user.updated_at,
              )

10.4 EmailValidator
====================

::

  class EmailValidator:
      EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

      @staticmethod
      def validate_format(email):
          if not re.match(EmailValidator.EMAIL_REGEX, email):
              raise InvalidEmailFormatError()

      @staticmethod
      def validate_unique(email, exclude_user_id):
          conflict = User.objects.filter(
              email__iexact=email
          ).exclude(user_id=exclude_user_id).exists()
          if conflict:
              raise EmailAlreadyTakenError()

10.5 Estandares aplicables
===========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Estandar
   - Aplicacion
 * - CNST-009
   - JWT obligatorio.
 * - CNST-013
   - Excepciones canonicas: ``InvalidEmailFormatError →
     400``, ``EmailAlreadyTakenError → 409``,
     ``ForbiddenFieldError → 400``,
     ``InvalidStateError → 409``.
 * - CNST-025
   - AuditEvent en transaccion atomica.
 * - CNST-026
   - payload contiene solo ``fields_changed`` (sin
     valores).
 * - STD-013
   - URL canonica ``PATCH /users/me``.
 * - STD-008
   - identifiers en ingles.

10.6 Componentes domain-model invocados
========================================

- ``User`` — read state, write full_name/email.
- ``AuditEvent`` (via AuditService) — append.
- ``RequireFunctionPolicy`` — verificacion RBAC.
