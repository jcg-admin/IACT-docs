.. meta::
 :artefacto: AT_UC_USR_04_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_04_design_secuencia:

===================================
UC_USR_04 — Design View (secuencia)
===================================

UC_USR_04 — Eliminar Usuario: Design View
==================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_USR_04 tecnicamente.

.. uml::
 :caption: UC_USR_04 — Design View (secuencia)

 @startuml

 actor "deactivate_users" as deactivate_users
 participant "Interfaz de Usuarios" as Iface <<frontend>>
 participant "Servicio de Usuarios" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 deactivate_users -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> deactivate_users : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-04/diagramas-uml`
