.. meta::
 :artefacto: AT_DESIGN_MOD_OPERATOR_CALLS
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_operator_calls:

=====================================================
Design View — MOD_Operator: Operacion del Agente
=====================================================

Patron de interaccion del modulo de operacion del agente. Muestra la
atencion de una llamada entrante: lectura de ``Call`` desde la BD
operativa (CNST-007: solo lectura), transferencia y ingreso de
disposition. La BD operativa MariaDB es de solo lectura para IACT.

.. uml::
 :caption: Design View MOD_Operator — flujo de atencion de llamada entrante.

 @startuml

 actor AGR_OPERADOR

 participant InterfazAgente   <<frontend>>
 participant ServicioLlamadas <<api>>
 participant RepositorioCall  <<repository>>
 database    BDOperativa      <<mariadb, readonly>>
 database    AlmacenDatos     <<postgresql>>

 AGR_OPERADOR -> InterfazAgente : recibir notificacion de llamada
 activate InterfazAgente

 InterfazAgente -> ServicioLlamadas : obtenerLlamada(call_id)
 activate ServicioLlamadas

 ServicioLlamadas -> RepositorioCall : buscar(call_id)
 activate RepositorioCall
 RepositorioCall -> BDOperativa : SELECT call_id, started_at,\n  duration_seconds, agent_id,\n  campaign_id, region\nFROM tbl_llamadas\nWHERE call_id=?\n<<CNST-007: readonly>>
 BDOperativa --> RepositorioCall : Call{call_id, campaign_id}
 RepositorioCall --> ServicioLlamadas : Call
 deactivate RepositorioCall

 ServicioLlamadas --> InterfazAgente : datos de la llamada
 deactivate ServicioLlamadas

 InterfazAgente --> AGR_OPERADOR : pantalla con Call + Campaign
 deactivate InterfazAgente

 AGR_OPERADOR -> InterfazAgente : ingresar disposition + transferir
 activate InterfazAgente

 InterfazAgente -> ServicioLlamadas : registrarDisposition(call_id, disposition)
 activate ServicioLlamadas

 ServicioLlamadas -> AlmacenDatos : INSERT call_dispositions{\n  call_id, disposition,\n  agent_id, registered_at\n}
 AlmacenDatos --> ServicioLlamadas : OK

 ServicioLlamadas --> InterfazAgente : 200 OK
 deactivate ServicioLlamadas
 InterfazAgente --> AGR_OPERADOR : disposition guardada
 deactivate InterfazAgente

 note right of BDOperativa
   CNST-007: BD operativa solo lectura.
   IACT no escribe en tbl_llamadas.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/call`
 :doc:`/arquitectura-tecnica/domain-model/campaign`
 :doc:`/arquitectura-tecnica/deploy-view/deploy-etl`
