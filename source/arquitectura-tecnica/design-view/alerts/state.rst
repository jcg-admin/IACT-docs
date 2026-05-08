.. meta::
 :artefacto: AT_DESIGN_STATE_ALERT_EVENT
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: Alert
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_state_alert_event:

============================================================
Design View — Ciclo de Vida: Alert
============================================================

Maquina de estados de la entidad ``Alert``. El ciclo cubre
desde la deteccion (raised) por el evaluador, pasando por
acknowledge / silenciado / auto-resolve, hasta el cierre
(resolved).

.. uml::
 :caption: Alert FSM — raised -> ack -> resolved (o auto-resolve).

 @startuml

 [*] --> raised : evaluator.threshold_exceeded

 raised --> acknowledged : User.ack()
 raised --> resolved : evaluator.threshold_back_to_normal\n(auto-resolve)
 raised --> silenced : User.silence(duration)

 silenced --> acknowledged : User.ack()
 silenced --> resolved : evaluator.threshold_back_to_normal
 silenced --> raised : silence_period_expired

 acknowledged --> resolved : User.resolve()
 acknowledged --> raised : User.unack()
 acknowledged --> resolved : evaluator.threshold_back_to_normal

 resolved --> [*]

 note right of raised
   el evaluator NO crea Alert
   duplicado para una misma rule
   ya en estado raised|ack|silenced.
 end note

 note bottom of resolved
   resolved es terminal. Si el
   threshold se excede de nuevo
   se crea NUEVO Alert.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/alerts/sequence`
 - :doc:`/arquitectura-tecnica/design-view/alerts/activity`
 - :doc:`/arquitectura-tecnica/design-view/alerts/class`
 - :doc:`/arquitectura-tecnica/use-case-view/alerts/index`
 - :doc:`/arquitectura-tecnica/domain-model/alert`
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`
