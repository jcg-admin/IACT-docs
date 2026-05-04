.. meta::
 :artefacto: AT_UC_AUD_01_DESIGN_SECUENCIA
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_01_design_secuencia:

===================================
UC_AUD_01 — Design View (secuencia)
===================================

UC_AUD_01 — Consultar Auditoria General: Design View
=============================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUD_01 tecnicamente.

.. uml::
 :caption: UC_AUD_01 — Design View (secuencia)

 @startuml

 actor "view_audit_log" as view_audit_log
 participant "Interfaz de Auditoria" as Iface <<frontend>>
 participant "Servicio de Auditoria" as SvcNode <<api>>
 database "Almacen de datos (audit_log)" as Store <<sql>>

 view_audit_log -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> view_audit_log : renderizar vista
 deactivate Iface

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/audit/uc-aud-01/diagramas-uml`
