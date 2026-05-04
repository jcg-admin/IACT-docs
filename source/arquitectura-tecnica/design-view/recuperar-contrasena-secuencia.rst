.. meta::
 :artefacto: AT_UC_AUTH_03_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_03_design_secuencia:

====================================
UC_AUTH_03 — Design View (secuencia)
====================================

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

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-03/diagramas-uml`
