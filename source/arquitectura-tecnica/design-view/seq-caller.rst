.. meta::
 :artefacto: AT_DESIGN_MOD_CALLER
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_caller:

=========================================
Design View — MOD_Caller: Flujo IVR
=========================================

Patron de interaccion del modulo de experiencia del cliente IVR. Muestra
el flujo completo desde que el ciudadano llama hasta que el sistema registra
la llamada en la BD Operativa. IACT accede a estos datos en modo solo lectura
via ETL (CNST-007, P-01).

.. uml::
 :caption: Design View MOD_Caller — flujo de llamada del ciudadano al IVR.

 @startuml

 actor CALLER

 participant PbxIvr          <<pbx>>
 participant RepositorioIVR  <<repository>>
 database    BDOperativa     <<mariadb, readonly>>
 participant ServicioETL     <<etl>>
 database    AlmacenDatos    <<postgresql>>

 CALLER -> PbxIvr : llamada telefonica
 activate PbxIvr

 PbxIvr -> RepositorioIVR : registrar llamada
 activate RepositorioIVR
 RepositorioIVR -> BDOperativa : INSERT tbl_historico_detalle\n(started_at, duration, agent_id,\ncampaign_id, region)
 BDOperativa --> RepositorioIVR : OK
 RepositorioIVR --> PbxIvr : registrado
 deactivate RepositorioIVR

 PbxIvr --> CALLER : menu IVR / cola / respuesta
 deactivate PbxIvr

 note over ServicioETL
   ETL nocturno (CNST-008: ventana 6-12h).
   IACT lee BDOperativa solo en ventana ETL.
   P-01: IACT no escribe en BDOperativa.
 end note

 ServicioETL -> BDOperativa : SELECT tbl_historico_*\n<<CNST-007: readonly>>
 activate ServicioETL
 BDOperativa --> ServicioETL : registros de llamadas

 ServicioETL -> AlmacenDatos : INSERT / UPDATE\nbase_ivr_detalle\nbase_ivr_clientes
 AlmacenDatos --> ServicioETL : OK
 deactivate ServicioETL

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/use-case-view/uc-caller`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/call`
 :doc:`/arquitectura-tecnica/domain-model/campaign`
 :doc:`/arquitectura-tecnica/process-view/proc-etl-pipeline`
