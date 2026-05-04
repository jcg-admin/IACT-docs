.. meta::
 :artefacto: AT_RBAC_DIAG_CICLO_VIDA
 :tipo: Diagrama Arquitectonico — Modelo RBAC
 :dominio: arquitectura_tecnica
 :subdominio: rbac/modelo-rbac-iact/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _rbac_ciclo_vida_asignacion:

===============================
Ciclo de Vida de una Asignacion
===============================

.. uml::
 :caption: Estados de una asignacion de funcion — incluye expiracion automatica.

 @startuml

 [*] --> PENDING_VALIDATION : assign_functions invocado

 PENDING_VALIDATION --> ACTIVE : SoD ok + registrar exitoso
 PENDING_VALIDATION --> REJECTED : viola SoD (EX-07)

 ACTIVE --> EXPIRED : expires_at alcanzado\n(job nocturno)
 ACTIVE --> REVOKED : revoke_functions invocado\n(UC_ACC_02)
 ACTIVE --> ACTIVE : re-asignacion\n(idempotente — 200)

 EXPIRED --> [*]
 REVOKED --> [*]
 REJECTED --> [*]

 note right of ACTIVE
   Cache de permisos invalidado
   en cada transicion.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
