5.2 ``INotificable`` — UC_ALR_02 / UC_ALR_05
--------------------------------------------

.. uml::

   @startuml
   allowmixing

   interface INotifiable <<interface>> {
     + deliver(user : User, message : Message) : Boolean
     + getDeliveryStatus() : DeliveryStatus
   }

   class InternalMailbox {
     + deliver(user, message) : Boolean
     + getDeliveryStatus() : DeliveryStatus
   }

   class PushNotification {
     + deliver(user, message) : Boolean
     + getDeliveryStatus() : DeliveryStatus
   }

   InternalMailbox ..|> INotifiable
   PushNotification ..|> INotifiable

   note right of INotifiable
     CNST_001 prohíbe email →
     IACT NO implementa EmailNotification.
     Las únicas implementaciones válidas son
     buzón interno y notificación push interna.
   end note
   @enduml
