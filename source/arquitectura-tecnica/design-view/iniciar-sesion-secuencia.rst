.. meta::
 :artefacto: AT_UC_AUTH_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_01_design_secuencia:

====================================
UC_AUTH_01 — Design View (secuencia)
====================================

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

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-01/diagramas-uml`
