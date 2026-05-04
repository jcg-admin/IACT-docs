.. meta::
 :artefacto: AT_UC_RPT_13_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_13_design:

==================================================
UC_RPT_13 — Reporte de Colas: Design View
==================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_13 tecnicamente.

.. uml::
 :caption: UC_RPT_13 — Design View (secuencia)

 @startuml

 actor "view_reports" as view_reports
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (base_ivr_*)" as BaseDatos <<sql>>

 view_reports -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_reports : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml`
