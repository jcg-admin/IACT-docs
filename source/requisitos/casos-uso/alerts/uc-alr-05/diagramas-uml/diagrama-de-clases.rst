.. _uc-alr-05-parte-08-diagrama-clases:

8.4 Diagrama de clases
=======================

.. uml::
 :caption: UC_ALR_05 — clases de Subscription.

 @startuml

 class Subscription {
   + id : UUID
   + user : User
   + rule : AlertRule
   + channel : NotificationChannel
   + scope : SegmentScope
   + state : SubscriptionState
 }

 class SubscriptionRepo {
   + create(sub) : Subscription
   + by_user(user) : List
 }

 class SegmentChangeListener {
   + on_segment_change(user, segments) : void
 }

 SubscriptionRepo "1" --> "*" Subscription : manages
 SegmentChangeListener --> SubscriptionRepo : pauses on revoke

 note right of SegmentChangeListener
   Cuando un user pierde acceso a
   un segmento, las suscripciones
   con ese scope pasan a paused
   automaticamente.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/subscription`.
