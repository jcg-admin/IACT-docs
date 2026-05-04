.. meta::
 :artefacto: AT_UC_PERM_03_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_perm_03_domain_estado:

=============================================================
UC_PERM_03 — Conceder Permiso Excepcional — Estado de Permiso
=============================================================

.. uml::
 :caption: UC_PERM_03 — Conceder Permiso Excepcional — Estado de Permiso

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
 :doc:`/requisitos/casos-uso/permissions/uc-perm-03/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/permissions/uc-perm-03/index`
