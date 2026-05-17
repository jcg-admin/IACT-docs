.. meta::
 :artefacto: AT_DM_CLASS_INTERNAL_MESSAGE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Mailbox
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_internal_message:

===============
InternalMessage
===============

Item individual dentro de ``InternalMailbox``. Representa cada mensaje
con sender, target, subject, body, urgencia y estado de lectura.
Diferente del container (``InternalMailbox``) que es el buzon del User
— ``InternalMessage`` es cada item dentro de ese buzon.

Cumple CNST-001 (NO email externo) + CNST-002 (mailbox interno
obligatorio): toda notificacion entre Users del sistema viaja como
``InternalMessage``, nunca por email externo.

.. uml::
 :caption: Clase InternalMessage — item individual del mailbox.

 @startuml

 class InternalMessage {
   + message_id : UUID
   + sender_id : UUID
   + target_user_id : UUID
   + target_type : MessageTarget
   + subject : String
   + body : Text
   + urgency : Urgency
   + read_state : ReadState
   + created_at : DateTime
   + read_at : DateTime
   --
   + create(sender_id : UUID, target : Target, subject : String, body : Text, urgency : Urgency) : InternalMessage
   + mark_as_read(reader_id : UUID) : void
   + sanitize_pii() : InternalMessage
 }

 enum MessageTarget {
   USER
   AGR
   TEAM
   SEGMENT
 }

 enum Urgency {
   INFO
   WARNING
   URGENT
 }

 enum ReadState {
   UNREAD
   READ
   ARCHIVED
 }

 InternalMessage -- MessageTarget
 InternalMessage -- Urgency
 InternalMessage -- ReadState

 note bottom of InternalMessage
   CNST-001 NO email externo.
   CNST-002 mailbox interno.
   CNST-026 sin PII en body.
   urgency=URGENT dispara push real-time.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que crean InternalMessage:

- :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
  notificacion al destino del permiso excepcional (P-10 mailbox-or-abort).
- :doc:`/requisitos/casos-uso/audit/uc-aud-03/index` —
  notificacion al solicitante cuando export termina.
- :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index` —
  broadcast del Supervisor al equipo (target=TEAM o SEGMENT).
- :doc:`/requisitos/casos-uso/alerts/uc-alr-05/index` —
  invitacion a suscripcion de alerta.

UCs que leen InternalMessage:

- :doc:`/requisitos/casos-uso/operator/uc-opr-10/index` —
  Operator lee su buzon interno (lista + mark_as_read).

Relaciones
==========

- :doc:`internal-mailbox` — el container que agrupa los InternalMessage del User.
- :doc:`user` — sender y target del mensaje.
- :doc:`access-group` — target=AGR resuelve a Users con AGR asignado.
- :doc:`sanitizer` — sanitiza body antes de persist (CNST-026).
