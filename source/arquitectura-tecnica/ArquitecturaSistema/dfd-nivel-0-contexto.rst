.. meta::
 :artefacto: AT_ARQ_SISTEMA_02_DFD_NIVEL_0
 :tipo: Diagrama Arquitectonico — Arquitectura del Sistema
 :dominio: arquitectura_tecnica
 :subdominio: ArquitecturaSistema
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arquitectura_dfd_nivel_0:

==================================
DFD Nivel 0 — Diagrama de Contexto
==================================

3. DFD Nivel 0 — Diagrama de Contexto
========================================

El diagrama de contexto muestra el sistema IACT como una caja
negra con sus entidades externas. Las entidades son los
**Usuarios IACT** (consumidores de servicios), el
**Sistema IVR** (proveedor de datos de llamadas) y el
**APScheduler/Cron** (disparador automatico del ETL).

.. uml::
 :caption: Figura 2 — DFD Nivel 0: Sistema IACT como caja negra

 @startuml
 skinparam rectangle {
   BackgroundColor white
   BorderColor #333333
   RoundCorner 5
 }
 skinparam arrowColor #333333

 rectangle "Sistema IVR\n(Fuente de datos)" as IVR
 rectangle "view_pipeline_status\n/ view_alerts" as SUP
 rectangle "view_reports\n/ view_dashboard" as ANA
 rectangle "APScheduler\n/ Cron" as SCH

 rectangle "  1\n  Sistema IACT\n  (Analisis IVR Calls)  " as IACT

 IVR --> IACT : datos IVR raw
 SUP --> IACT : comandos ETL / alertas
 ANA --> IACT : solicitudes de reporte
 SCH --> IACT : disparo ETL automatico
 IACT --> SUP : estado pipeline / alertas
 IACT --> ANA : reportes IVR / dashboard

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
