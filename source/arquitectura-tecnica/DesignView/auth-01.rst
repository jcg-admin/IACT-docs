.. meta::
 :artefacto: AT_UC_AUTH_01_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_01_design:

=================================================
UC_AUTH_01 — Iniciar Sesion: Design View
=================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUTH_01 tecnicamente.

.. uml::
 :caption: UC_AUTH_01 — Design View (secuencia)

 @startuml

 actor "Usuario" as Usuario
 participant "Interfaz de Acceso" as Iface <<frontend>>
 participant "Servicio de Autenticacion" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 Usuario -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> Usuario : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_AUTH_01 — Iniciar Sesion — Comunicacion entre Objetos

 @startuml

 object ":Usuario" as Actor
 object ":Interfaz de Acceso" as Iface
 object ":Servicio de Autenticacion" as Svc
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

 :doc:`/requisitos/casos-uso/auth/uc-auth-01/diagramas-uml`
