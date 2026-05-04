.. meta::
 :artefacto: AT_UC_AUTH_03_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_03_design:

=======================================================
UC_AUTH_03 — Recuperar Contrasena: Design View
=======================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUTH_03 tecnicamente.

.. uml::
 :caption: UC_AUTH_03 — Design View (secuencia)

 @startuml

 actor "reset_password" as reset_password
 participant "Interfaz de Acceso" as Iface <<frontend>>
 participant "Servicio de Autenticacion" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 reset_password -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> reset_password : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_AUTH_03 — Recuperar Contrasena — Comunicacion entre Objetos

 @startuml

 object ":reset_password" as Actor
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

 :doc:`/requisitos/casos-uso/auth/uc-auth-03/diagramas-uml`
