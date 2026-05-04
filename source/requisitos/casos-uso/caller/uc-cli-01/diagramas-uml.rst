.. _uc-cli-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 actor "Telephony" as Telephony
 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nIniciar llamada" as UcCli01
   usecase "UC_CLI_02\nNavegar IVR" as IVR
 }
 Caller --> UcCli01
 UcCli01 --> Telephony
 UcCli01 ..> IVR : <<include>>
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Llamada al DID;
 :Telephony acepta;
 :Capturar caller_id;
 :Hash caller_id;
 :INSERT CallSession;
 :Reproducir greeting;
 :Audit CALL_STARTED;
 :Pasar a IVR;
 stop
 @enduml

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
 Telephony -> Callrepo: INSERT session
 Telephony -> Auditsvc: emit CALL_STARTED
 Telephony -> Caller: greeting audio
 @enduml
