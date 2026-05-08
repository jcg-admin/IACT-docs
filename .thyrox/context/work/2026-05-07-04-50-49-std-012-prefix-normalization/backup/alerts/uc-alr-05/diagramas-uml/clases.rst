8.4 Clases
==========

.. uml::

 @startuml
 class Subscription
 class SubscriptionRepo
 class SegmentChangeListener
 SubscriptionRepo -- Subscription
 SegmentChangeListener -- SubscriptionRepo
 @enduml
