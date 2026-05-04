.. meta::
 :artefacto: AT_UC_USR_02_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_usr_02_domain:

=====================================================
UC_USR_02 — Consultar Usuarios: Domain Model
=====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/users/uc-usr-02/index`.

.. uml::
 :caption: UC_USR_02 — Domain Model

 @startuml

 left to right direction

 class User
 class AccessGroup
 class User

 User --> AccessGroup
 AccessGroup --> User

 @enduml


.. uml::
 :caption: UC_USR_02 — Consultar Usuarios — Estado de User

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
 :doc:`/requisitos/casos-uso/users/uc-usr-02/index`
