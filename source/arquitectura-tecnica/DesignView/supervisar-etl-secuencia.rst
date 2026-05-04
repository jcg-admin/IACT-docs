.. meta::
 :artefacto: AT_UC_PIP_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_01_design_secuencia:

===================================
UC_PIP_01 — Design View (secuencia)
===================================

UC_PIP_01 — Supervisar ETL: Design View
================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PIP_01 tecnicamente.

.. uml::
 :caption: UC_PIP_01 — Design View (secuencia)

 @startuml

 actor "view_pipeline_status" as view_pipeline_status
 participant "Interfaz de Pipeline" as Iface <<frontend>>
 participant "Servicio de Pipeline" as SvcNode <<api>>
 database "Almacen de datos (sp_etl_*)" as Store <<sql>>

 view_pipeline_status -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_pipeline_status : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml`
