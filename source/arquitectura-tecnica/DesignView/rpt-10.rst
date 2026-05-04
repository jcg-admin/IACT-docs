.. meta::
 :artefacto: AT_UC_RPT_10_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_rpt_10_design:

===============================================
UC_RPT_10 — Guardar Vista: Design View
===============================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_RPT_10 tecnicamente.

.. uml::
 :caption: UC_RPT_10 — Design View (secuencia)

 @startuml

 actor "save_view" as save_view
 participant "React Frontend" as Frontend <<frontend>>
 participant "Django API" as APIServer <<api>>
 database "MariaDB (base_ivr_*)" as BaseDatos <<sql>>

 save_view -> Frontend : solicitar
 activate Frontend

 Frontend -> APIServer : POST/GET endpoint
 activate APIServer

 APIServer -> BaseDatos : query / SP
 activate BaseDatos
 BaseDatos --> APIServer : resultado
 deactivate BaseDatos

 APIServer --> Frontend : respuesta JSON
 deactivate APIServer

 Frontend --> save_view : renderizar vista
 deactivate Frontend

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml`
