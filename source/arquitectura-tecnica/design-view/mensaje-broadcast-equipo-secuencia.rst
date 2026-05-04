.. meta::
 :artefacto: AT_UC_SUP_03_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_design_secuencia:

===================================
UC_SUP_03 — Design View (secuencia)
===================================

UC_SUP_03 — Mensaje Broadcast al Equipo: Design View
=============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_SUP_03 tecnicamente.

.. uml::
 :caption: UC_SUP_03 — Design View (secuencia)

 @startuml

 actor "broadcast_team_messages" as broadcast_team_messages
 participant "Interfaz de Supervision" as Iface <<frontend>>
 participant "Servicio de Supervision" as SvcNode <<api>>
 database "Almacen de datos (tbl_historico_*)" as Store <<sql>>

 broadcast_team_messages -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> broadcast_team_messages : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/diagramas-uml`
