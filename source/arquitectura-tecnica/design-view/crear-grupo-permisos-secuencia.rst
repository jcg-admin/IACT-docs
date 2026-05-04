.. meta::
 :artefacto: AT_UC_PERM_05_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_05_design_secuencia:

====================================
UC_PERM_05 — Design View (secuencia)
====================================

UC_PERM_05 — Crear Grupo de Permisos: Design View
==========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_05 tecnicamente.

.. uml::
 :caption: UC_PERM_05 — Design View (secuencia)

 @startuml

 actor "create_function_group" as create_function_group
 participant "Interfaz de Permisos" as Iface <<frontend>>
 participant "Servicio de Permisos" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 create_function_group -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> create_function_group : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml`
