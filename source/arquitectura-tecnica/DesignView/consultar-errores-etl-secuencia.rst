.. meta::
 :artefacto: AT_UC_PIP_02_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_02_design_secuencia:

===================================
UC_PIP_02 — Design View (secuencia)
===================================

UC_PIP_02 — Consultar Errores ETL: Design View
=======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PIP_02 tecnicamente.

.. uml::
 :caption: UC_PIP_02 — Design View (secuencia)

 @startuml

 actor "view_pipeline_errors" as view_pipeline_errors
 participant "Interfaz de Pipeline" as Iface <<frontend>>
 participant "Servicio de Pipeline" as SvcNode <<api>>
 database "MariaDB (sp_etl_*)" as Store <<sql>>

 view_pipeline_errors -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_pipeline_errors : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml`
