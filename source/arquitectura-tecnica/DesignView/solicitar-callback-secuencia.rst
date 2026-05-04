.. meta::
 :artefacto: AT_UC_CLI_04_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_cli_04_design_secuencia:

===================================
UC_CLI_04 — Design View (secuencia)
===================================

UC_CLI_04 — Solicitar Callback: Design View
====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_CLI_04 tecnicamente.

.. uml::
 :caption: UC_CLI_04 — Design View (secuencia)

 @startuml

 actor "CallerExterno" as CallerExterno
 participant "Interfaz de Llamadas" as Iface <<frontend>>
 participant "Servicio de Llamadas" as SvcNode <<api>>
 database "Almacen de datos (tbl_historico_*)" as Store <<sql>>

 CallerExterno -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> CallerExterno : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/caller/uc-cli-04/diagramas-uml`
