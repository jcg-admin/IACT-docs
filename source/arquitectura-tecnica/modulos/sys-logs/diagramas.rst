.. _arq-mod-008-diagramas:

================================================
ARQ_MOD_008 — Diagramas de Comportamiento
================================================


Flujo del Health Check
=======================

.. uml::
 :caption: Flujo del health check del sistema — recoleccion de metricas y evaluacion de umbrales.

 @startuml

 start

 :Inicio de ciclo de health check\n(APScheduler — intervalo periodico);

 :Recolectar metricas del sistema\n(CPU, memoria, disco, conexiones BD);

 :Recolectar estado de servicios\n(MariaDB, PostgreSQL, ETL, cola async);

 :Comparar valores contra umbrales\nconfigurables (view_system_status);

 if (Algun umbral violado?) then (si)
   :Registrar SystemHealth\ncon estado DEGRADADO;
   :Notificar a modulo de alertas\n(generar alerta automatica);
   stop
 else (todos OK)
   :Registrar SystemHealth\ncon estado OK;
   stop
 endif

 @enduml

----

Secuencia de Consulta de Logs del Sistema
==========================================

.. uml::
 :caption: Secuencia view_system_logs — consulta filtrada con tail SSE opcional.

 @startuml

 actor "view_system_logs" as U
 participant "LogEndpoint\n(/logs/system/)" as EP
 database "LogStore\n(PostgreSQL)" as LS

 U -> EP : GET /logs/system/?range=1h&level=ERROR
 EP -> EP : JWT + RBAC (view_system_logs)
 alt sin permiso
   EP --> U : 403 Forbidden
 else con permiso
   EP -> LS : SELECT WHERE level=ERROR AND ts > now()-1h
   LS --> EP : entries
   EP -> EP : sanitizar (eliminar PII)
   EP --> U : 200 + entries JSON
   opt tail SSE
     loop nuevas entradas
       LS -> EP : new entry
       EP -> U : SSE data
     end
   end
 end

 @enduml

----

Diagrama de componentes — MOD_Logs
=====================================

.. uml::
 :caption: Componentes de MOD_Logs y pipeline de recoleccion de logs.

 @startuml

 component "Apps Django\n(stdout/stderr)" as APP
 component "fluent-bit\n(shipper)" as FB
 database "LogStore\n(PostgreSQL)" as LS
 database "etl_runs\n(MariaDB)" as ETL_LOG

 component "view_system_logs" as VSL
 component "view_etl_logs" as VEL
 component "search_logs" as SL
 component "export_logs" as EL
 component "InternalMailbox" as MB

 APP --> FB : stdout logs estructurados
 FB --> LS : INSERT logs

 VSL --> LS : SELECT sistema
 VEL --> ETL_LOG : SELECT etl_runs
 SL --> LS : SELECT con filtros
 EL --> LS : SELECT rango + generar CSV
 EL --> MB : notificar via buzon

 @enduml
