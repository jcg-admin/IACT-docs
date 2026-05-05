8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_CLI_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "Caller (cliente externo)" as CALLER <<externo>>
 actor "Trunk SIP" as TRUNK <<sistema>>
 actor "Session" as SESSION <<sistema>>
 actor "Call" as CALL <<sistema>>
 actor "Sanitizer" as SAN <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_01\nIniciar Llamada\nal Call Center" as UC_CLI_01
   usecase "Reproducir\nwelcome / saludo" as WELCOME
   usecase "Hashear caller_id\n(CNST-026)" as HASH
   usecase "Crear Session\ncon caller_hash" as CREATE_SESSION
   usecase "Crear Call\nasociado a Session" as CREATE_CALL
   usecase "Transferir control\na IVR (UC_CLI_02)" as HANDOFF
 }

 CALLER --> TRUNK
 TRUNK --> UC_CLI_01

 UC_CLI_01 ..> WELCOME : <<include>>
 UC_CLI_01 ..> HASH : <<include>>
 UC_CLI_01 ..> CREATE_SESSION : <<include>>
 UC_CLI_01 ..> CREATE_CALL : <<include>>
 UC_CLI_01 ..> HANDOFF : <<include>>

 HASH --> SAN
 CREATE_SESSION --> SESSION
 CREATE_CALL --> CALL

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

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/session` —
   entidad Session creada con caller_hash.
 - :doc:`/arquitectura-tecnica/domain-model/call` —
   entidad Call asociada a la Session.
 - :doc:`/arquitectura-tecnica/domain-model/sanitizer` —
   componente que hashea caller_id (CNST-026).
