8.3 Pipeline PII
================

.. uml::

 @startuml
 component "Caller phone" as CallerPhone
 component "Telephony" as Telephony
 component "PIIHasher" as Piihasher
 component "CallSession" as Callsession
 CallerPhone --> Telephony
 Telephony --> Piihasher
 Piihasher --> Callsession
 note right of Piihasher
   Hash con tenant_salt.
   Phone NUNCA llega a Callsession raw.
 end note
 @enduml

