.. meta::
 :artefacto: AT_DM_CLASS_INTERNAL_MAILBOX
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_internal_mailbox:

===============
InternalMailbox
===============

Canal de notificacion interno por usuario. Por CNST-001 el sistema
IACT no tiene canal de email externo; todas las notificaciones al
usuario pasan por este buzon interno.

.. uml::
 :caption: Clase InternalMailbox — buzon interno de notificaciones.

 @startuml

 class InternalMailbox {
   + mailbox_id : UUID
   + owner_user_id : UUID
   + last_read_at : DateTime
   --
   + deliver_message()
   + view_messages()
   + mark_read()
 }

 note bottom of InternalMailbox
   CNST-001: buzon interno unicamente,
   sin canal de email externo.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/user`
