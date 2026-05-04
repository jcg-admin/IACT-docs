.. _arq-mod-011-diagramas:

================================================
ARQ_MOD_011 — Diagramas de Comportamiento
================================================


Flujo del Llamante en el IVR
==============================

.. uml::
 :caption: Flujo del Caller — llamada entrante, navegacion, cola y CSAT.

 @startuml

 start

 :Caller marca numero IVR;
 :Sistema IVR contesta\n(UC_CLI_01 — tbl_historico_detalle INSERT);

 :Navegar menu IVR\n(UC_CLI_02 — tbl_historico_detalle UPDATE menu_seleccion);

 if (Agente disponible?) then (si)
   :Conectar con agente\n(answer_inbound_calls);
   :Atencion de llamada;
   :Ofrecer encuesta CSAT\n(UC_CLI_05);
   :Registrar respuesta CSAT\n(tbl_historico_detalle.csat);
   stop
 else (no disponible)
   :Encolar llamada\n(UC_CLI_03 — estado=en_cola);
   if (Tiempo espera > umbral?) then (si)
     :Caller cuelga\n(tasa abandono para BR-016);
     :INSERT abandon en tbl_historico_detalle;
     stop
   else (espera aceptable)
     :Ofrecer callback\n(UC_CLI_04);
     if (Caller acepta callback?) then (si)
       :Registrar callback pendiente;
       :Sistema devuelve llamada automaticamente;
       :Conectar con agente;
       stop
     else (no)
       :Continuar espera en cola;
       stop
     endif
   endif
 endif

 @enduml

----

Pipeline de Datos IVR — Caller a Analitica
============================================

.. uml::
 :caption: Componentes de MOD_Caller — desde la llamada hasta la Base Analitica.

 @startuml

 actor "Caller\n(externo)" as CALLER

 component "PBX / PbxIvr\n(Asterisk/Genesys)" as PbxIvr
 database "tbl_historico_detalle\ntbl_historico_clientes\n(Repositorio PbxIvr — solo lectura para IACT)" as HIST

 component "sp_etl_maestro\n(sp_etl_maestro nocturno)" as sp_etl_maestro
 database "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as ANAL

 component "sp_rpt_llamadas_abandonadas\nsp_rpt_clientes\n(Reportes PbxIvr)" as sp_rpt_llamadas_abandonadas
 component "AlertEvaluator\n(BR-016 tasa abandono)" as ALERT

 CALLER --> PbxIvr : llamada telefonica
 PbxIvr --> HIST : INSERT/UPDATE registros PbxIvr
 sp_etl_maestro --> HIST : SELECT (ventana nocturna)
 sp_etl_maestro --> ANAL : TRUNCATE + INSERT
 sp_rpt_llamadas_abandonadas --> ANAL : SELECT (cursor.callproc)
 ALERT --> ANAL : evaluar tasa abandono > 30%%

 @enduml
