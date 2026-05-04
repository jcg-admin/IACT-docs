.. meta::
 :artefacto: AT_UC_AUTH_05_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_05_design_secuencia:

====================================
UC_AUTH_05 — Design View (secuencia)
====================================

UC_AUTH_05 — Gestionar Sesiones: Design View
=====================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUTH_05 tecnicamente.

.. uml::
 :caption: UC_AUTH_05 — Design View (secuencia)

 @startuml

 actor "view_own_sessions" as view_own_sessions
 participant "Interfaz de Acceso" as Iface <<frontend>>
 participant "Servicio de Autenticacion" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 view_own_sessions -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_own_sessions : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-05/diagramas-uml`
