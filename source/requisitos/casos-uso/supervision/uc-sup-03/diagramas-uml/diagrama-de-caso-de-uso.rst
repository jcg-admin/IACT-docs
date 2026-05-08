8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_SUP_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "broadcast_team_messages" as INVOKER
 actor "InternalMailbox" as MB <<sistema>>
 actor "Operators (target)" as TARGETS <<beneficiario>>
 actor "SegmentResolver" as SR <<sistema>>

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_03\nMensaje Broadcast\nal Equipo" as UC_SUP_03
   usecase "Validar target\n(team_id | segment_codes)" as VALIDAR_TARGET
   usecase "Validar urgency\n(info | warning | urgente)" as VALIDAR_URGENCY
   usecase "Resolver destinatarios\n(segmentos del Supervisor)" as RESOLVER
   usecase "Encolar en\nInternalMailbox" as ENCOLAR
   usecase "Push real-time\n(si urgente)" as PUSH <<extend>>
 }

 INVOKER --> UC_SUP_03
 UC_SUP_03 ..> VALIDAR_TARGET : <<include>>
 UC_SUP_03 ..> VALIDAR_URGENCY : <<include>>
 UC_SUP_03 ..> RESOLVER : <<include>>
 UC_SUP_03 ..> ENCOLAR : <<include>>
 PUSH ..> UC_SUP_03 : <<extend>>

 RESOLVER --> SR
 ENCOLAR --> MB
 MB --> TARGETS

 note bottom of VALIDAR_TARGET
   CNST-008 isolation: target_team
   o segment_codes deben estar en
   los segmentos del Supervisor.
 end note

 note bottom of PUSH
   urgency=urgente dispara push
   en tiempo real ademas del
   buzon. info/warning solo
   mailbox.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   InternalMailbox donde se encola el broadcast (CNST-002).
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   resuelve segmentos accesibles del Supervisor (CNST-008).
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   Users destinatarios del broadcast.
