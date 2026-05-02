.. _arq-mod-004-diagramas:

================================================
ARQ_MOD_004 — Diagramas de Comportamiento
================================================


Flujo ETL Nocturno (Solo Supervision)
======================================

.. uml::
 :caption: Flujo ETL nocturno — el Actor Tiempo dispara la ventana de carga (CNST-006/008).

 @startuml

 actor "Tiempo\n(ventana nocturna)" as T
 participant "BD Operativa\n(solo lectura)" as BDO
 participant "Proceso ETL\n(automático)" as ETL
 participant "BD Analítica\n(escribible)" as BDA
 participant "Módulo ETL\n(supervisión)" as MON

 T -> ETL : ventana de carga programada\n(CNST-006/008)
 ETL -> BDO : extraer desde vista de llamadas\n(SELECT — sin escritura)
 BDO --> ETL : registros del período
 ETL -> ETL : transformar y calcular métricas
 ETL -> BDA : cargar métricas calculadas\n(INSERT)
 ETL -> MON : registrar ejecución\n{estado, filas, duración}

 note over MON
   El módulo ETL solo supervisa.
   No interviene en el proceso —
   observa y reporta estado.
 end note

 @enduml
