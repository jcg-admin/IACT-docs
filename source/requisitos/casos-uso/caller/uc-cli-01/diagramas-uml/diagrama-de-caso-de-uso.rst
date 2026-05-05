8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_CLI_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "Caller (cliente externo)" as CALLER <<externo>>
 actor "Trunk SIP" as TRUNK <<sistema>>
 actor "IVRRunner" as IVR <<sistema>>
 actor "CallSessionRepo" as REPO <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nIniciar Llamada\nal Call Center" as UC_CLI_01
   usecase "Reproducir\nwelcome / saludo" as WELCOME
   usecase "Hashear caller_id\n(CNST-026)" as HASH
   usecase "Crear CallSession\ncon caller_hash" as CREATE
   usecase "Transferir control\na IVRRunner (UC_CLI_02)" as HANDOFF
 }

 CALLER --> TRUNK
 TRUNK --> UC_CLI_01

 UC_CLI_01 ..> WELCOME : <<include>>
 UC_CLI_01 ..> HASH : <<include>>
 UC_CLI_01 ..> CREATE : <<include>>
 UC_CLI_01 ..> HANDOFF : <<include>>

 CREATE --> REPO
 HANDOFF --> IVR

 note bottom of HASH
   CNST-026: caller_hash desde
   primer momento. Nunca se
   persiste caller_id en limpio.
   Sin PII en logs.
 end note

 note right of CALLER
   BReq-007 — actor externo
   no autenticado en sistema.
   Trigger: numero externo
   marca DID del call center.
 end note

 @enduml
