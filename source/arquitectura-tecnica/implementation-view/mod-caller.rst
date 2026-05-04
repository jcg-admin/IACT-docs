.. meta::
 :artefacto: AT_IMPL_MOD_CALLER
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_caller:

==========================================
Implementation View — MOD_Caller
==========================================

Componentes y paquetes de codigo del modulo de datos del llamante IVR.
IACT accede a los datos de llamadas (``Call``, ``Campaign``) en modo solo
lectura via el pipeline ETL — nunca directamente desde la aplicacion web
(P-01, CNST-007).

.. uml::
 :caption: Implementation View MOD_Caller — componentes de acceso a datos del IVR.

 @startuml

 package "MOD_ETL (acceso a datos Caller)" {
   component "ETLExtractor\nextract_calls()\nextract_campaigns()" as ETLExtractor <<service>>
   component "IVRRepository\nCallRepository\nCampaignRepository" as IVRRepo <<repository>>
   component "CallORM\nCampaignORM" as CallerORM <<orm>>
 }

 package "MOD_Caller (consulta interna)" {
   component "CallView\nCampaignView" as CallerView <<api>>
   component "CallSerializer\nCampaignSerializer" as CallerSerializer <<serializer>>
   component "CallerService\nconsultar datos cargados por ETL" as CallerService <<service>>
 }

 database "BDOperativa\n(MariaDB, readonly)" as BDOperativa
 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 ETLExtractor --> IVRRepo : delega extraccion
 IVRRepo --> CallerORM : mapea
 CallerORM --> BDOperativa : SELECT tbl_historico_*\n<<CNST-007: readonly, P-01>>

 ETLExtractor --> AlmacenDatos : INSERT base_ivr_detalle\nbase_ivr_clientes

 CallerView --> CallerSerializer : valida
 CallerView --> CallerService : invoca
 CallerService --> AlmacenDatos : SELECT base_ivr_*\n(datos ya cargados por ETL)

 note right of BDOperativa
   CNST-007: solo GRANT SELECT.
   P-01: IACT nunca escribe en BDOperativa.
   El acceso a BDOperativa ocurre
   unicamente durante la ventana ETL
   (CNST-008: 6-12h).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/use-case-view/mod-caller`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/call`
 :doc:`/arquitectura-tecnica/domain-model/campaign`
 :doc:`/arquitectura-tecnica/process-view/proc-etl-pipeline`
