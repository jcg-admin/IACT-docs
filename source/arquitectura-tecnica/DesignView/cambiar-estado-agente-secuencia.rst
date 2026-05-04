.. meta::
 :artefacto: AT_UC_OPR_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_01_design_secuencia:

===================================
UC_OPR_01 — Design View (secuencia)
===================================

UC_OPR_01 — Cambiar Estado del Agente: Design View
===========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_OPR_01 tecnicamente.

.. uml::
 :caption: UC_OPR_01 — Design View (secuencia)

 @startuml

 actor "manage_own_agent_state" as manage_own_agent_state
 participant "Interfaz de Operador" as Iface <<frontend>>
 participant "Servicio de Operador" as SvcNode <<api>>
 database "MariaDB (tbl_historico_*)" as Store <<sql>>

 manage_own_agent_state -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> manage_own_agent_state : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/operator/uc-opr-01/diagramas-uml`
