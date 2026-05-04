.. meta::
 :artefacto: AT_DESIGN_MOD_SUPERVISION
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_supervision:

=====================================================
Design View — MOD_Supervision: Supervision en Tiempo Real
=====================================================

Patron de interaccion del modulo de supervision en tiempo real.
Muestra el monitoreo de llamadas activas, barge-in del supervisor
a una ``Call`` en curso y envio de mensaje broadcast al equipo de
agentes.

.. uml::
 :caption: Design View MOD_Supervision — monitoreo, barge-in y broadcast.

 @startuml

 actor AGR_SUPERVISOR

 participant InterfazSupervision <<frontend>>
 participant ServicioSupervision <<api>>
 participant ServicioLlamadas    <<api>>
 participant RepositorioCall     <<repository>>
 database    BDOperativa         <<mariadb, readonly>>
 database    AlmacenDatos        <<postgresql>>

 AGR_SUPERVISOR -> InterfazSupervision : GET /supervision/calls/active
 activate InterfazSupervision

 InterfazSupervision -> ServicioSupervision : listarLlamadasActivas()
 activate ServicioSupervision

 ServicioSupervision -> RepositorioCall : findActive()
 activate RepositorioCall
 RepositorioCall -> BDOperativa : SELECT call_id, agent_id,\n  campaign_id, started_at\nFROM tbl_llamadas\nWHERE estado=ACTIVA\n<<CNST-007: readonly>>
 BDOperativa --> RepositorioCall : List<Call>
 RepositorioCall --> ServicioSupervision : llamadas activas
 deactivate RepositorioCall

 ServicioSupervision --> InterfazSupervision : dashboard en tiempo real
 deactivate ServicioSupervision
 InterfazSupervision --> AGR_SUPERVISOR : lista de llamadas
 deactivate InterfazSupervision

 AGR_SUPERVISOR -> InterfazSupervision : POST /supervision/calls/{call_id}/barge-in
 activate InterfazSupervision

 InterfazSupervision -> ServicioSupervision : bargeIn(call_id, supervisor_id)
 activate ServicioSupervision

 ServicioSupervision -> ServicioLlamadas : unirseALlamada(call_id)
 activate ServicioLlamadas
 ServicioLlamadas --> ServicioSupervision : canal abierto
 deactivate ServicioLlamadas

 ServicioSupervision -> AlmacenDatos : INSERT audit_events\n{event_type:CONFIG_CHANGED,\n details:{barge_in:call_id}}
 AlmacenDatos --> ServicioSupervision : AuditEvent registrado

 ServicioSupervision --> InterfazSupervision : 200 OK conectado
 deactivate ServicioSupervision

 AGR_SUPERVISOR -> InterfazSupervision : POST /supervision/broadcast\n{message, team_id}
 InterfazSupervision -> ServicioSupervision : enviarBroadcast(message, agentes)
 activate ServicioSupervision
 ServicioSupervision -> AlmacenDatos : INSERT internal_mailbox_messages\n(por cada agente del equipo)
 AlmacenDatos --> ServicioSupervision : mensajes entregados
 ServicioSupervision --> InterfazSupervision : 200 OK
 deactivate ServicioSupervision
 InterfazSupervision --> AGR_SUPERVISOR : confirmacion
 deactivate InterfazSupervision

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/call`
 :doc:`/arquitectura-tecnica/domain-model/internal-mailbox`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`
