.. meta::
 :artefacto: AT_UC_PERM_07_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_07_domain:

================================================================
UC_PERM_07 — Verificar Permiso de Usuario: Domain Model
================================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index`.

.. uml::
 :caption: UC_PERM_07 — Domain Model

 @startuml

 left to right direction

 class UserFunction
 class User
 class AccessGroup

 UserFunction --> User
 User --> AccessGroup

 @enduml


.. uml::
 :caption: UC_PERM_07 — Verificar Permiso de Usuario — Estado de Permiso

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
 :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index`
