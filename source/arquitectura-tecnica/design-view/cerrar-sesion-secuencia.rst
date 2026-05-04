.. meta::
 :artefacto: AT_UC_AUTH_02_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_auth_02_design_secuencia:

====================================
UC_AUTH_02 — Design View (secuencia)
====================================

UC_AUTH_02 — Cerrar Sesion: Design View
================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUTH_02 tecnicamente.

.. uml::
 :caption: UC_AUTH_02 — Design View (secuencia)

 @startuml

 actor "close_user_session" as close_user_session
 participant "Interfaz de Acceso" as Iface <<frontend>>
 participant "Servicio de Autenticacion" as SvcNode <<api>>
 database "Almacen de Datos" as Store <<sql>>

 close_user_session -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> close_user_session : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/auth/uc-auth-02/diagramas-uml`
