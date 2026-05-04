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

 :Comparar valores contra umbrales\nconfigurables (view_system_health);

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
 :caption: Secuencia view_application_logs — consulta filtrada con tail SSE opcional.

 @startuml

 actor "view_application_logs" as view_application_logs
 participant "LogEndpoint\n(/logs/system/)" as Logendpoint
 database "LogStore\n(PostgreSQL)" as Logstore

 view_application_logs -> Logendpoint : GET /logs/system/?range=1h&level=ERROR
 Logendpoint -> Logendpoint : JWT + RBAC (view_application_logs)
 alt sin permiso
   Logendpoint --> view_application_logs : 403 Forbidden
 else con permiso
   Logendpoint -> Logstore : SELECT WHERE level=ERROR AND ts > now()-1h
   Logstore --> Logendpoint : entries
   Logendpoint -> Logendpoint : sanitizar (eliminar PII)
   Logendpoint --> view_application_logs : 200 + entries JSON
   opt tail SSE
     loop nuevas entradas
       Logstore -> Logendpoint : new entry
       Logendpoint -> view_application_logs : SSE data
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

 component "Apps Django\n(stdout/stderr)" as AppsDjango
 component "fluent-bit\n(shipper)" as FluentBit
 database "LogStore\n(PostgreSQL)" as Logstore
 database "etl_runs\n(MariaDB)" as ETL_LOG

 component "view_application_logs" as view_application_logs
 component "view_etl_logs" as view_etl_logs
 component "search_logs" as search_logs
 component "export_logs" as export_logs
 component "InternalMailbox" as Internalmailbox

 AppsDjango --> FluentBit : stdout logs estructurados
 FluentBit --> Logstore : INSERT logs

 view_application_logs --> Logstore : SELECT sistema
 view_etl_logs --> ETL_LOG : SELECT etl_runs
 search_logs --> Logstore : SELECT con filtros
 export_logs --> Logstore : SELECT rango + generar CSV
 export_logs --> Internalmailbox : notificar via buzon

 @enduml
