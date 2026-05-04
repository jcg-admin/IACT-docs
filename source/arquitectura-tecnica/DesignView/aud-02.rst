.. meta::
 :artefacto: AT_UC_AUD_02_DESIGN
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_aud_02_design:

==================================================
UC_AUD_02 — Buscar Auditoria: Design View
==================================================

Secuencia del flujo principal. Muestra como el sistema resuelve
UC_AUD_02 tecnicamente.

.. uml::
 :caption: UC_AUD_02 — Design View (secuencia)

 @startuml

 actor "search_audit_log" as search_audit_log
 participant "Interfaz de Auditoria" as Iface <<frontend>>
 participant "Servicio de Auditoria" as SvcNode <<api>>
 database "MariaDB (audit_log)" as Store <<sql>>

 search_audit_log -> Iface : solicitar
 activate Iface

 Iface -> SvcNode : POST/GET endpoint
 activate SvcNode

 SvcNode -> Store : query / SP
 activate Store
 Store --> SvcNode : resultado
 deactivate Store

 SvcNode --> Iface : respuesta JSON
 deactivate SvcNode

 Iface --> search_audit_log : renderizar vista
 deactivate Iface

 @enduml


.. uml::
 :caption: UC_AUD_02 — Buscar Auditoria — Comunicacion entre Objetos

 @startuml

 object ":search_audit_log" as Actor
 object ":Interfaz de Auditoria" as Iface
 object ":Servicio de Auditoria" as Svc
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

 :doc:`/requisitos/casos-uso/audit/uc-aud-02/diagramas-uml`
