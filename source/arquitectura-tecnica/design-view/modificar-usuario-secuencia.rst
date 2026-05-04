.. meta::
 :artefacto: AT_UC_USR_03_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_03_design_secuencia:

===================================
UC_USR_03 — Design View (secuencia)
===================================

UC_USR_03 — Modificar Usuario: Design View
===================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_USR_03 tecnicamente.

.. uml::
 :caption: UC_USR_03 — Design View (secuencia)

 @startuml

 actor "update_users" as update_users
 participant "Interfaz de Usuarios" as Iface <<frontend>>
 participant "Servicio de Usuarios" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 update_users -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> update_users : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-03/diagramas-uml`
