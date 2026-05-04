.. meta::
 :artefacto: AT_UC_USR_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_01_design_secuencia:

===================================
UC_USR_01 — Design View (secuencia)
===================================

UC_USR_01 — Crear Usuario: Design View
===============================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_USR_01 tecnicamente.

.. uml::
 :caption: UC_USR_01 — Design View (secuencia)

 @startuml

 actor "create_users" as create_users
 participant "Interfaz de Usuarios" as Iface <<frontend>>
 participant "Servicio de Usuarios" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 create_users -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> create_users : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-01/diagramas-uml`
