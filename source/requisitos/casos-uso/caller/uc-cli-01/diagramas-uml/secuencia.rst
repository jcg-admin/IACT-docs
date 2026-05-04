8.4 Secuencia
=============

.. uml::

 @startuml
 actor "Caller" as Caller
 participant "Telephony" as Telephony
 participant "PIIHasher" as Piihasher
 participant "CallRepo" as Callrepo
 participant "AuditSvc" as Auditsvc
 Caller -> Telephony: dial DID
 Telephony -> Piihasher: caller_id
 Piihasher --> Telephony: hash
 Telephony -> Callrepo: registrar session
 Telephony -> Auditsvc: emit CALL_STARTED
 Telephony -> Caller: greeting audio
 @enduml
