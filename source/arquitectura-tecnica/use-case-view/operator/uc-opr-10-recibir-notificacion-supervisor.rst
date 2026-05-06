.. meta::
 :artefacto: AT_UC_OPR_10_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Reservado
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_opr_10_recibir_notificacion_supervisor:

==============================================
UC_OPR_10 — Leer Buzon Interno
==============================================

Agente lee buzon interno con notificaciones. Mensajes: broadcasts
(UC_SUP_03), individuales del supervisor, alertas operacionales
(export ready, schedule paused, etc.). ``read_own_mailbox``.
CNST-001 NO email externo + CNST-002 mailbox obligatorio.

.. uml::
 :caption: UC_OPR_10 — actores y casos asociados.

 @startuml

 left to right direction

 actor "read_own_mailbox" as read_own_mailbox
 actor "broadcast_team_messages" as Supervisor <<beneficiario>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>
 actor "InternalMessage" as InternalMessage <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_10\nLeer Buzon Interno\n.. extension points ..\nBroadcast\nAlertasOp" as UC_OPR_10
   usecase "Listar mensajes\n(unread first)" as LISTAR
   usecase "Marcar como leido" as MARCAR
   usecase "Broadcasts (UC_SUP_03)" as BROADCAST
   usecase "Alertas operacionales\n(export ready, schedule)" as ALERTAS_OP
 }

 read_own_mailbox --> UC_OPR_10

 UC_OPR_10 ..> LISTAR : <<include>>
 UC_OPR_10 ..> MARCAR : <<include>>
 BROADCAST ..> UC_OPR_10 : <<extend>> (Broadcast)
 ALERTAS_OP ..> UC_OPR_10 : <<extend>> (AlertasOp)

 LISTAR --> InternalMailbox
 LISTAR --> InternalMessage
 MARCAR --> InternalMessage
 BROADCAST --> Supervisor

 note bottom of UC_OPR_10
   CNST-001 NO email externo +
   CNST-002 mailbox interno
   obligatorio. Mensajes:
   broadcast (UC_SUP_03),
   individual del supervisor,
   alertas operacionales.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   InternalMailbox del User.
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   items individuales.
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   propietario del buzon.
 - :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index` —
   broadcast origen.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-10/index` —
   spec textual.
