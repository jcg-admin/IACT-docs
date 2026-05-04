.. meta::
 :artefacto: AT_UC_USR_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_02_design:

====================================================
UC_USR_02 — Consultar Usuarios: Design View
====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_USR_02 tecnicamente.

.. uml::
 :caption: UC_USR_02 — Design View (secuencia)

 @startuml

 actor "list_users" as list_users
 participant "Interfaz de Usuarios" as Iface <<frontend>>
 participant "Servicio de Usuarios" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 list_users -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> list_users : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_USR_02 — Consultar Usuarios — Comunicacion entre Objetos

 @startuml

 object ":list_users" as Actor
 object ":Interfaz de Usuarios" as Iface
 object ":Servicio de Usuarios" as Svc
 object ":Repositorio" as Repo
 object ":Almacen de Datos" as Store

 Actor -> Iface : 1: solicitar accion
 Iface -> Svc : 2: invocar endpoint
 Svc -> Svc : 3: validar RBAC
 Svc -> Repo : 4: ejecutar operacion
 Repo -> Store : 5: query / SP
 Store --> Repo : 6: resultado
 Repo --> Svc : 7: entidad
 Svc --> Iface : 8: respuesta
 Iface --> Actor : 9: renderizar

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/users/uc-usr-02/diagramas-uml`
