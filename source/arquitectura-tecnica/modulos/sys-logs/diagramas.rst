.. _arq-mod-008-diagramas:

================================================
ARQ_MOD_008 — Diagramas de Comportamiento
================================================


Flujo del Health Check
=======================

.. uml::
 :caption: Flujo del health check del sistema — recolección de métricas y evaluación de umbrales.

 @startuml

 start

 :Inicio de ciclo de health check\n(disparado por el Actor Tiempo\nen intervalo periódico);

 :Recolectar métricas del sistema\n(CPU, memoria, disco, conexiones BD);

 :Recolectar estado de servicios\n(BD, cola asíncrona, proceso ETL);

 :Comparar valores contra umbrales\nconfigurables;

 if (¿Algún umbral violado?) then (sí)
   :Registrar SystemHealth\ncon estado DEGRADADO;
   :Notificar a módulo de alertas\n(generar alerta automática);
   stop
 else (todos OK)
   :Registrar SystemHealth\ncon estado OK;
   stop
 endif

 @enduml
