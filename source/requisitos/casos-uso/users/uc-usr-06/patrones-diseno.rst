.. _uc-usr-06-parte-08:

==========================================
Parte 8 — Patrones de diseño
==========================================

8.1 Patrones GoF aplicados
===========================

Command (Unblock)
------------------

::

  class UnblockUserCommand:
      target_user_id: UUID
      actor_id: UUID
      reason: String

      execute() -> UnblockResult

Mismo patron que UC_USR_05 (BlockUserCommand). Permite
testing aislado y rollback explicito.

Memento (parcial — captura del estado de origen)
--------------------------------------------------

Antes de la transicion, el sistema captura el contexto
del bloqueo previo (lookup de AuditEvent original) para
incluir referencia en el evento USER_UNBLOCKED. No es
Memento puro (no se restaura un objeto previo) pero
preserva la cadena bloqueo→desbloqueo.

8.2 Patrones de Larman
=======================

Information Expert
------------------

La validacion ``state == BLOCKED`` y la transicion a
``ACTIVE`` viven en ``User``.

Controller
----------

``UnblockUserEndpoint`` orquesta verificacion de permisos,
lookup del bloqueo previo, transaccion y respuesta.

8.3 Patrones GRASP
===================

Pure Fabrication
----------------

``UnblockUserCommand`` es Pure Fabrication (no representa
concepto del dominio).

Polymorphism con UC_USR_05
---------------------------

``BlockUserCommand`` y ``UnblockUserCommand`` comparten
estructura (Command interface). La maquinaria de
verificacion de funcion RBAC, transaccion atomica, y
emision de AuditEvent es polimorfica entre ambos.

8.4 No aplican
===============

- **Singleton, Observer, Builder fluent**: por las mismas
  razones que en UC_USR_05.
- **Strategy**: a diferencia de UC_USR_05, UC_USR_06 NO
  tiene multiples close_reasons; es siempre una unica
  transicion ``BLOCKED → ACTIVE``.
