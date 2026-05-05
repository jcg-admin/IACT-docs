.. meta::
 :artefacto: ARQ_MOD_011_DIAG_PIPELINE_DATOS
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/caller/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_011_pipeline_datos_ivr_caller:

==========================================
Pipeline de Datos IVR — Caller a Analitica
==========================================

Flujo completo desde la llamada del ciudadano hasta la Base Analitica IVR:
captura en PBX, almacenamiento en tablas historico (solo lectura para IACT),
extraccion nocturna via ETL y evaluacion de alertas sobre los datos cargados.

.. uml::
 :caption: Componentes de MOD_Caller — desde la llamada hasta la Base Analitica.

 @startuml

 actor "Caller\n(externo)" as CALLER

 component "PBX / PbxIvr\n(Asterisk/Genesys)" as PbxIvr
 database "tbl_historico_detalle\ntbl_historico_clientes\n(Repositorio PbxIvr — solo lectura para IACT)" as HISTORICO_IVR

 component "sp_etl_maestro\n(sp_etl_maestro nocturno)" as sp_etl_maestro
 database "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as BASE_ANALITICA

 component "sp_rpt_llamadas_abandonadas\nsp_rpt_clientes\n(Reportes PbxIvr)" as sp_rpt_llamadas_abandonadas
 component "AlertEvaluator\n(BR-016 tasa abandono)" as EVALUADOR_ALERTAS

 CALLER --> PbxIvr : llamada telefonica
 PbxIvr --> HISTORICO_IVR : registrar/actualizar registros PbxIvr
 sp_etl_maestro --> HISTORICO_IVR : consultar (ventana nocturna)
 sp_etl_maestro --> BASE_ANALITICA : TRUNCATE + registrar
 sp_rpt_llamadas_abandonadas --> BASE_ANALITICA : consultar (cursor.callproc)
 EVALUADOR_ALERTAS --> BASE_ANALITICA : evaluar tasa abandono > 30%%

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/caller/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
