.. meta::
 :artefacto: AT_UC_USR_04_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_04_domain_estado:

=============================================
UC_USR_04 — Eliminar Usuario — Estado de User
=============================================

.. uml::
 :caption: UC_USR_04 — Eliminar Usuario — Estado de User

 @startuml
 hide empty description

 [*] --> Creado : crear usuario
 Creado --> Activo : activar cuenta
 Activo --> Suspendido : suspender
 Suspendido --> Activo : reactivar
 Activo --> Desactivado : dar de baja
 Desactivado --> [*] : eliminar definitivo

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/users/uc-usr-04/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/users/uc-usr-04/index`
