8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_SUP_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "broadcast_team_messages" as INVOKER
 actor "MailboxService" as MAILBOX <<sistema>>
 actor "SSEPushChannel" as SSE <<sistema>>
 actor "Operators (target)" as TARGETS <<beneficiario>>

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_03\nMensaje Broadcast\nal Equipo" as UC_SUP_03
   usecase "Validar target\n(team_id | segment_codes)" as VALIDAR_TARGET
   usecase "Validar urgency\n(info | warning | urgente)" as VALIDAR_URGENCY
   usecase "Encolar en\nInternalMailbox" as ENCOLAR
   usecase "Push SSE\n(si urgente)" as PUSH <<extend>>
 }

 INVOKER --> UC_SUP_03
 UC_SUP_03 ..> VALIDAR_TARGET : <<include>>
 UC_SUP_03 ..> VALIDAR_URGENCY : <<include>>
 UC_SUP_03 ..> ENCOLAR : <<include>>
 PUSH ..> UC_SUP_03 : <<extend>>

 ENCOLAR --> MAILBOX
 PUSH --> SSE
 MAILBOX --> TARGETS
 SSE --> TARGETS

 note bottom of VALIDAR_TARGET
   CNST-008 isolation: target_team
   o segment_codes deben estar en
   los segmentos del Supervisor.
 end note

 note bottom of PUSH
   urgency=urgente dispara push
   SSE en tiempo real ademas del
   buzon. info/warning solo
   mailbox.
 end note

 @enduml
