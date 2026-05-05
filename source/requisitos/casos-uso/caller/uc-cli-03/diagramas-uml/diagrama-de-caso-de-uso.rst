8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_CLI_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "Caller (cliente externo)" as CALLER <<externo>>
 actor "CallRouter" as ROUTER <<sistema>>
 actor "QueueDefinition" as QUEUE <<sistema>>
 actor "Operator" as OPERATOR <<beneficiario>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_03\nEsperar en Cola" as UC_CLI_03
   usecase "Aplicar reglas\nde routing (skill, queue)" as ROUTING
   usecase "Reproducir mensajes\nde espera + posicion" as MENSAJES
   usecase "Monitorear timeout\n(SLA max wait)" as TIMEOUT
   usecase "Ofrecer callback\n(UC_CLI_04)" as OFRECER_CB <<extend>>
   usecase "Conectar con\nOperator" as CONECTAR <<extend>>
 }

 CALLER --> UC_CLI_03
 ROUTER --> UC_CLI_03

 UC_CLI_03 ..> ROUTING : <<include>>
 UC_CLI_03 ..> MENSAJES : <<include>>
 UC_CLI_03 ..> TIMEOUT : <<include>>
 OFRECER_CB ..> UC_CLI_03 : <<extend>>
 CONECTAR ..> UC_CLI_03 : <<extend>>

 ROUTING --> QUEUE
 CONECTAR --> OPERATOR

 note bottom of TIMEOUT
   Restriccion: max wait time
   configurado por SLA.
   Tras X min ofrece callback
   (UC_CLI_04) automaticamente.
 end note

 note right of CALLER
   Trigger: UC_CLI_02 selecciono
   cola o flujo directo a cola.
 end note

 @enduml
