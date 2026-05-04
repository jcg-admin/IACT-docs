.. meta::
 :artefacto: AT_UC_USR_01_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_01_domain_estado:

==========================================
UC_USR_01 — Crear Usuario — Estado de User
==========================================

.. uml::
 :caption: UC_USR_01 — Crear Usuario — Estado de User

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
 :doc:`/requisitos/casos-uso/users/uc-usr-01/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/users/uc-usr-01/index`
