.. meta::
 :artefacto: AT_UC_PERM_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_01_design_secuencia:

====================================
UC_PERM_01 — Design View (secuencia)
====================================

UC_PERM_01 — Asignar Grupo a Usuario: Design View
==========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_01 tecnicamente.

.. uml::
 :caption: UC_PERM_01 — Design View (secuencia)

 @startuml

 actor "assign_function_groups" as assign_function_groups
 participant "Interfaz de Permisos" as Iface <<frontend>>
 participant "Servicio de Permisos" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 assign_function_groups -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> assign_function_groups : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-01/diagramas-uml`
