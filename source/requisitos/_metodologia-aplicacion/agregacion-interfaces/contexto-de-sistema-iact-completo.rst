4.2 Contexto de sistema — IACT completo
---------------------------------------

.. uml::

   @startuml
   allowmixing

   package "IACT (contexto del sistema)" {
     class User
     class Session
     class Report
     class Metric
     class Alert
     class Subscription
     class ETLExecution
     class AuditEvent
     class IVR
     class InternalMailbox

     User --> Session         : opens
     User --> Report          : queries
     Report --> Metric        : aggregates
     Alert  --> Subscription  : notifies
     Subscription --> User    : belongs
     ETLExecution --> IVR     : reads (read-only)
     Alert --> InternalMailbox : notifies via (CNST_001)
     User --> AuditEvent      : generates
   }

   cloud "Stripe / SendGrid" as Externos
   note right of Externos
     NO aplica a IACT —
     sin pasarela de pago,
     sin email externo.
   end note
   @enduml
