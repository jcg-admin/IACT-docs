.. meta::
 :artefacto: AT_UC_ACC_09_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_acc_09_domain_estado:

=================================================================
UC_ACC_09 — Auditar Cambios de Acceso — Estado de FuncionAsignada
=================================================================

.. uml::
 :caption: UC_ACC_09 — Auditar Cambios de Acceso — Estado de FuncionAsignada

 @startuml
 hide empty description

 [*] --> Pendiente : solicitar asignacion
 Pendiente --> Asignada : aprobar asignacion
 Asignada --> Activa : activar
 Activa --> Revocada : revocar funcion
 Pendiente --> [*] : rechazar solicitud
 Revocada --> [*] : eliminar registro

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/access/uc-acc-09/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/access/uc-acc-09/index`
