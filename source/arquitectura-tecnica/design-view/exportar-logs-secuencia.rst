.. meta::
 :artefacto: AT_UC_LOG_04_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_log_04_design_secuencia:

===================================
UC_LOG_04 — Design View (secuencia)
===================================

UC_LOG_04 — Exportar Logs: Design View
===============================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_LOG_04 tecnicamente.

.. uml::
 :caption: UC_LOG_04 — Design View (secuencia)

 @startuml

 actor "export_logs" as export_logs
 participant "Interfaz de Logs" as Iface <<frontend>>
 participant "Servicio de Logs" as SvcNode <<api>>
 database "Almacen de datos" as Store <<sql>>

 export_logs -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> export_logs : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/logs/uc-log-04/diagramas-uml`
