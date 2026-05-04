.. meta::
 :artefacto: AT_UC_RPT_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: uc/DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_02_design:

=============================================================
UC_RPT_02 — Ver Metricas en Tiempo Real: Design View
=============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_02 tecnicamente.

.. uml::
 :caption: UC_RPT_02 — Design View (secuencia)

 @startuml

 actor "view_kpis" as view_kpis
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (base_ivr_*)" as BaseDatos <<sql>>

 view_kpis -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> view_kpis : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-02/diagramas-uml`
