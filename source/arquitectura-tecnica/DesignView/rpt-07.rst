.. meta::
 :artefacto: AT_UC_RPT_07_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_07_design:

===================================================
UC_RPT_07 — Programar Reporte: Design View
===================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_07 tecnicamente.

.. uml::
 :caption: UC_RPT_07 — Design View (secuencia)

 @startuml

 actor "schedule_report" as schedule_report
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (base_ivr_*)" as BaseDatos <<sql>>

 schedule_report -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> schedule_report : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-07/diagramas-uml`
