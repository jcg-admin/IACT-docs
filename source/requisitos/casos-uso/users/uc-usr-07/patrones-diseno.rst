.. _uc-usr-07-parte-08:

==========================================
Parte 8 — Patrones de diseño
==========================================

8.1 Patrones GoF aplicados
===========================

Command (UpdateProfile)
------------------------

::

  class UpdateOwnProfileCommand:
      actor_id: UUID    # = target_user_id
      patch: Map<String, Any>

      execute() -> UpdateResult

8.2 Patrones de Larman
=======================

Information Expert
------------------

La validacion ``state == ACTIVE`` y la escritura de
campos viven en ``User``. La validacion de email
(formato + unicidad) vive en ``EmailValidator`` (Pure
Fabrication especializado).

Controller
----------

``UpdateOwnProfileEndpoint`` es el Controller (Larman).

8.3 Patrones GRASP
===================

Pure Fabrication
----------------

``UpdateOwnProfileCommand`` y ``EmailValidator`` son Pure
Fabrications.

Polymorphism
------------

UC_USR_07 (self-service) y UC_USR_03 (admin)
implementan operaciones diferentes pero comparten la
estructura ``UpdateUserCommand`` polimorfica con
strategy de validacion distinta:

- UC_USR_07: validacion restrictiva (solo ``full_name``,
  ``email``).
- UC_USR_03: validacion permisiva pero con autorizacion
  ``modify_users``.

Protected Variations
---------------------

El conjunto de campos editables esta encapsulado en una
constante ``EDITABLE_FIELDS_SELF = {'full_name',
'email'}`` separada de ``EDITABLE_FIELDS_ADMIN``. Cambiar
las reglas no requiere modificar el flujo principal.

8.4 No aplican
===============

- **Strategy en close-reason**: no aplica (UC_USR_07 no
  cierra sesiones).
- **Memento**: no aplica (no hay capture/restore de
  estado).
