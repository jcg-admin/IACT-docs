.. meta::
 :artefacto: AT_UC_SUP_03_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_03_domain_estado:

=====================================================================
UC_SUP_03 — Mensaje Broadcast al Equipo — Estado de SesionSupervision
=====================================================================

.. uml::
 :caption: UC_SUP_03 — Mensaje Broadcast al Equipo — Estado de SesionSupervision

 @startuml
 hide empty description

 [*] --> Abierta : supervisor ingresa
 Abierta --> Monitoreando : ver metricas activas
 Monitoreando --> Interviniendo : accion correctiva
 Interviniendo --> Monitoreando : accion completada
 Monitoreando --> Cerrada : supervisor sale
 Cerrada --> [*] : registrar sesion

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index`
