.. meta::
 :artefacto: AT_UC_PERM_06_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_06_design_secuencia:

====================================
UC_PERM_06 — Design View (secuencia)
====================================

UC_PERM_06 — Asignar Funciones a Grupo: Design View
============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_06 tecnicamente.

.. uml::
 :caption: UC_PERM_06 — Design View (secuencia)

 @startuml

 actor "assign_functions_to_group" as assign_functions_to_group
 participant "Interfaz de Permisos" as Iface <<frontend>>
 participant "Servicio de Permisos" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 assign_functions_to_group -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> assign_functions_to_group : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-06/diagramas-uml`
