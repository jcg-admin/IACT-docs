.. meta::
 :artefacto: AT_UC_PERM_06_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_06_domain:

=============================================================
UC_PERM_06 — Asignar Funciones a Grupo: Domain Model
=============================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index`.

.. uml::
 :caption: UC_PERM_06 — Domain Model

 @startuml

 left to right direction

 class AccessGroup
 class Function
 class AuditEvent

 AccessGroup --> Function
 Function --> AuditEvent

 @enduml


.. uml::
 :caption: UC_PERM_06 — Asignar Funciones a Grupo — Estado de Permiso

 @startuml
 hide empty description

 [*] --> Solicitado : crear solicitud
 Solicitado --> EnRevision : iniciar revision
 EnRevision --> Aprobado : aprobar
 EnRevision --> Denegado : denegar
 Aprobado --> Activo : activar permiso
 Activo --> Revocado : revocar
 Denegado --> [*] : cerrar solicitud
 Revocado --> [*] : archivar

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index`
