.. meta::
 :artefacto: AT_UC_SUP_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: supervision
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_sup_03_mensaje_broadcast_al_equipo:

============================================================
UC_SUP_03 — Mensaje Broadcast al Equipo
============================================================

Supervisor envia ``InternalMessage`` masivo al equipo (target=team_id
o segment_codes). Tipos: info, warning, urgente. Urgente dispara push
real-time ademas del mailbox. ``broadcast_team_messages``. CNST-008
isolation por scope del Supervisor.

.. uml::
 :caption: UC_SUP_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "broadcast_team_messages" as broadcast_team_messages
 actor "Operators" as Operators <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "InternalMessage" as InternalMessage <<sistema>>

 rectangle "MOD_Supervision" {
   usecase "UC_SUP_03\nMensaje Broadcast\nal Equipo\n.. extension points ..\nPushUrgente" as UC_SUP_03
   usecase "Verificar\nbroadcast_team_messages" as VERIFICAR_AGR
   usecase "Validar target\n(team_id | segment_codes)" as VALIDAR_TARGET
   usecase "Validar urgency\n(info | warning | urgente)" as VALIDAR_URGENCY
   usecase "Resolver destinatarios\n(segmentos del Supervisor)" as RESOLVER
   usecase "Encolar en\nInternalMailbox" as ENCOLAR
   usecase "Push real-time\n(si urgente)" as PUSH
 }

 broadcast_team_messages --> UC_SUP_03

 UC_SUP_03 ..> VERIFICAR_AGR : <<include>>
 UC_SUP_03 ..> VALIDAR_TARGET : <<include>>
 UC_SUP_03 ..> VALIDAR_URGENCY : <<include>>
 UC_SUP_03 ..> RESOLVER : <<include>>
 UC_SUP_03 ..> ENCOLAR : <<include>>
 PUSH ..> UC_SUP_03 : <<extend>> (PushUrgente)

 VERIFICAR_AGR --> AuthorizationGuard
 RESOLVER --> SegmentResolver
 ENCOLAR --> InternalMailbox
 ENCOLAR --> InternalMessage
 InternalMailbox --> Operators

 note bottom of VALIDAR_TARGET
   CNST-008 isolation: target_team
   o segment_codes deben estar
   en los segmentos del Supervisor.
 end note

 note bottom of PUSH
   urgency=URGENT dispara push
   real-time ademas del buzon.
   info/warning solo mailbox.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   InternalMailbox del User (CNST-002).
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   item del broadcast.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   CNST-008.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   destinatarios.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index` —
   spec textual.
