.. _uc-alr-05-parte-08-diagrama-estados-subscription:

8.3 Diagrama de estados — Subscription
=======================================

.. uml::
 :caption: Subscription — ciclo de vida.

 @startuml

 [*] --> active : crear (UC_ALR_05)
 active --> paused : mute manual /\nrevocar segmento
 paused --> active : unmute /\nrestaurar segmento
 active --> deleted : delete (BR-009)
 paused --> deleted : delete (BR-009)
 deleted --> [*]

 note right of active
   Suscripcion entrega notificaciones
   al user via el canal configurado
   cuando dispara la AlertRule asociada.
 end note

 note right of paused
   Suscripcion preservada pero no
   entrega notificaciones. Causa:
   mute manual o revocacion del
   segmento (SegmentChangeListener).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/subscription`.
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`.
