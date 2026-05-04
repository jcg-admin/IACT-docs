.. meta::
 :artefacto: AT_UC_PERM_08_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_08_design_secuencia:

====================================
UC_PERM_08 — Design View (secuencia)
====================================

UC_PERM_08 — Generar Menu Dinamico: Design View
========================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_PERM_08 tecnicamente.

.. uml::
 :caption: UC_PERM_08 — Design View (secuencia)

 @startuml

 actor "view_assignments" as view_assignments
 participant "Interfaz de Permisos" as Iface <<frontend>>
 participant "Servicio de Permisos" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 view_assignments -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_assignments : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/permissions/uc-perm-08/diagramas-uml`
