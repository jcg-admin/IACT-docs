9.1 Suscripcion entre Usuario y Alerta (UC_ALR_05)
--------------------------------------------------

.. uml::

   @startuml

   class User
   class Alert

   class Subscription {
     - enrollment_date : DateTime
     - channel : Enum
     - min_severity : Enum
     - silenced_until : DateTime
     + update(channel, severity)
     + silence(until)
   }

   User "0..*" -- "0..*" Alert : subscribed_to
   (User, Alert) .. Subscription
   note right of Subscription
     Atributos propios de la
     suscripción: fecha, canal
     (sólo buzón interno per
     CNST_001), severidad mínima
     y silenciamiento temporal.
   end note
   @enduml
