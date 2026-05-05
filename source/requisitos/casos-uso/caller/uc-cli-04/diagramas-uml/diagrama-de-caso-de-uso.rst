8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_CLI_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "Caller (cliente externo)" as CALLER <<externo>>
 actor "Call" as CALL <<sistema>>
 actor "Session" as SESSION <<sistema>>

 rectangle "MOD_Caller" {
   usecase "UC_CLI_04\nSolicitar Callback" as UC_CLI_04
   usecase "Confirmar numero\nde retorno" as CONFIRM_NUM
   usecase "Confirmar ventana\nhoraria" as CONFIRM_WINDOW
   usecase "Crear CallbackEntry\n(Call con type=callback)" as CREATE_CB
   usecase "Hangup voluntario\n(release linea)" as HANGUP
 }

 CALLER --> UC_CLI_04

 UC_CLI_04 ..> CONFIRM_NUM : <<include>>
 UC_CLI_04 ..> CONFIRM_WINDOW : <<include>>
 UC_CLI_04 ..> CREATE_CB : <<include>>
 UC_CLI_04 ..> HANGUP : <<include>>

 CREATE_CB --> CALL
 HANGUP --> SESSION

 note bottom of CONFIRM_NUM
   Numero de retorno puede ser
   caller_id (default) o un numero
   alterno indicado por el caller.
 end note

 note right of CALLER
   Disparado desde UC_CLI_02
   (auto-servicio) o UC_CLI_03
   (espera en cola exhausto SLA).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/call` —
   Call con type=callback persistido para retry async.
 - :doc:`/arquitectura-tecnica/domain-model/session` —
   Session terminada tras hangup voluntario.
