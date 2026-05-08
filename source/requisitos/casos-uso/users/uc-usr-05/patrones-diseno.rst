.. _uc-usr-05-parte-08:

==========================================
Parte 8 — Patrones de diseño
==========================================

8.1 Patrones GoF aplicados
===========================

Strategy (close-reason)
-----------------------

El cierre de Sessions admite multiples close_reason
codificadas como Strategy: ``USER_BLOCKED``,
``USER_ELIMINATED`` (UC_USR_04), ``ADMIN_REVOKE`` (UC_AUTH_05).
Cada close_reason puede tener side-effects distintos en
emision de AuditEvent y en notificacion al User.

UC_USR_05 utiliza la strategy ``USER_BLOCKED`` que:

- Cierra sesiones sin notificacion al User (el User no
  esta en sesion para recibirla, y cuando intente
  reconectar recibira ``401 ACCOUNT_BLOCKED``).
- Emite AuditEvent ``USER_BLOCKED``.

Command (Block)
----------------

La operacion de bloqueo se modela como un Command
encapsulado:

::

  class BlockUserCommand:
      target_user_id: UUID
      actor_id: UUID
      reason: String

      execute() -> BlockResult

Permite testing aislado del comando, retry/rollback
explicito, y trazabilidad estructurada.

8.2 Patrones de Larman
=======================

Information Expert
------------------

La validacion ``state == ACTIVE`` y la transicion a
``BLOCKED`` viven en la clase ``User`` (information
expert de su propio estado), no en una capa de servicio
generica.

Controller
----------

El endpoint ``BlockUserEndpoint`` (o equivalente) es el
``Controller`` (Larman): orquesta la verificacion de
permisos, carga del User, validaciones, transaccion y
respuesta.

8.3 Patrones GRASP
===================

Pure Fabrication
----------------

``BlockUserCommand`` es un Pure Fabrication: no
representa ningun concepto del dominio, pero centraliza
la cohesion de la operacion. Su unico proposito es
encapsular el "como" del bloqueo.

Polymorphism
------------

El sistema reconoce 3 mecanismos de bloqueo
(``USER_BLOCKED`` admin, ``ACCOUNT_LOCKED`` BR-015
automatico, ``USER_ELIMINATED`` baja logica) que
comparten la transicion ``state → estado-restrictivo``
pero difieren en actor y motivo. Polymorphism via
``BlockingMechanism`` interface permite extender sin
modificar el flujo principal.

8.4 No aplican
===============

- **Singleton**: no hay estado global compartido.
- **Observer**: el AuditEvent es sincrono dentro de la
  misma transaccion, no via observers asincronos.
- **Builder fluent**: el comando no tiene multi-paso
  configurable; sed plain assembler.
