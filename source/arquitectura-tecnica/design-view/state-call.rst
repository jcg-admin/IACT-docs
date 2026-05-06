.. meta::
 :artefacto: AT_DESIGN_STATE_CALL
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: Call
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_design_state_call:

============================================================
Design View — Ciclo de Vida: Call
============================================================

Maquina de estados de la entidad ``Call``. Representa el ciclo
completo de una llamada desde que ingresa al sistema (initiated)
hasta su cierre (closed) o fallo (failed).

Cubre la operacion de modulos MOD_Caller, MOD_Operator,
MOD_Supervision.

.. uml::
 :caption: Call FSM — 10 estados con transiciones disparadas por eventos.

 @startuml

 [*] --> initiated : Caller.invoke()

 initiated --> in_menu : Menu.load()
 in_menu --> in_menu : NavDomain.record(option)
 in_menu --> queued : transfer_to_operator
 in_menu --> self_service : self_service_path
 in_menu --> abandoned : caller_hangup

 queued --> ringing : Operator.assign()
 queued --> abandoned : caller_hangup
 queued --> failed : timeout

 ringing --> answered : Operator.answer()
 ringing --> missed : Operator.no_answer

 answered --> on_hold : Operator.hold()
 on_hold --> answered : Operator.unhold()

 answered --> transferred : Operator.transfer()
 answered --> wrap : Operator.disposition()

 transferred --> answered : NewOperator.answer()

 wrap --> closed : disposition_recorded

 self_service --> closed : caller_hangup
 abandoned --> closed : timeout_cleanup
 missed --> closed : moved_to_voicemail
 failed --> closed : error_logged

 closed --> [*]

 note right of answered
   estado activo: el agente esta
   conversando. AHT counter activo.
 end note

 note right of wrap
   ACW (After Call Work):
   agente registra disposition.
   No puede recibir nueva llamada.
 end note

 @enduml

----

Notas de diseno
================

- **AHT**: Average Handle Time se calcula desde ``answered``
  hasta ``wrap`` (incluye ``on_hold`` time).
- **ACW**: After Call Work mide tiempo en ``wrap``.
- **abandoned**: caller cuelga antes de ser asignado a operador.
- **missed**: el operador estaba disponible pero no contesto
  (timer expira).
- **transferred**: relacion 1:1 con un nuevo Call hijo del
  primero.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/seq-caller`
 - :doc:`/arquitectura-tecnica/design-view/seq-operator`
 - :doc:`/arquitectura-tecnica/design-view/class-caller`
 - :doc:`/arquitectura-tecnica/design-view/class-operator`
 - :doc:`/arquitectura-tecnica/use-case-view/operator/index`
 - :doc:`/arquitectura-tecnica/domain-model/call`
