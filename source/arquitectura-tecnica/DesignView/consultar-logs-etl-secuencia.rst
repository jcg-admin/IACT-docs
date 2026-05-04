.. meta::
 :artefacto: AT_UC_LOG_02_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_02_design_secuencia:

===================================
UC_LOG_02 — Design View (secuencia)
===================================

UC_LOG_02 — Consultar Logs del ETL: Design View
========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_LOG_02 tecnicamente.

.. uml::
 :caption: UC_LOG_02 — Design View (secuencia)

 @startuml

 actor "view_etl_logs" as view_etl_logs
 participant "Interfaz de Logs" as Iface <<frontend>>
 participant "Servicio de Logs" as SvcNode <<api>>
 database "MariaDB / Sistema" as Store <<sql>>

 view_etl_logs -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_etl_logs : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-02/diagramas-uml`
