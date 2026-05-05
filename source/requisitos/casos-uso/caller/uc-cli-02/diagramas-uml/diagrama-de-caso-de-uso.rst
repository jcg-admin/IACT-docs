8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_CLI_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "Caller (cliente externo)" as CALLER <<externo>>
 actor "IVRRunner" as IVR <<sistema>>
 actor "IVRDefinition" as IVRDEF <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_02\nNavegar IVR" as UC_CLI_02
   usecase "Cargar arbol IVR\n(IVRDefinition)" as CARGAR
   usecase "Capturar input\n(audio / DTMF)" as CAPTURAR
   usecase "Enrutar a cola\n(UC_CLI_03)" as ROUTE_QUEUE <<extend>>
   usecase "Auto-servicio\n(saldo, horario, ...)" as SELF_SERVICE <<extend>>
   usecase "Ofrecer callback\n(UC_CLI_04)" as ROUTE_CALLBACK <<extend>>
   usecase "Hangup voluntario" as HANGUP <<extend>>
 }

 CALLER --> UC_CLI_02
 IVR --> UC_CLI_02

 UC_CLI_02 ..> CARGAR : <<include>>
 UC_CLI_02 ..> CAPTURAR : <<include>>
 ROUTE_QUEUE ..> UC_CLI_02 : <<extend>>
 SELF_SERVICE ..> UC_CLI_02 : <<extend>>
 ROUTE_CALLBACK ..> UC_CLI_02 : <<extend>>
 HANGUP ..> UC_CLI_02 : <<extend>>

 CARGAR --> IVRDEF

 note bottom of UC_CLI_02
   Sin entrada HTTP — input audio /
   DTMF directo. Salidas posibles:
   cola para agente, auto-servicio,
   callback (UC_CLI_04), hangup.
 end note

 @enduml
