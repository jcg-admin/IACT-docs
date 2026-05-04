.. meta::
 :artefacto: AT_UC_SUP_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_sup_01_domain:

=====================================================
UC_SUP_01 — Monitorear Llamada: Domain Model
=====================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/supervision/uc-sup-01/index`.

.. uml::
 :caption: UC_SUP_01 — Domain Model

 @startuml

 left to right direction

 class Call
 class AgentSession
 class SupervisionChannel

 Call --> AgentSession
 AgentSession --> SupervisionChannel

 @enduml


.. uml::
 :caption: UC_SUP_01 — Monitorear Llamada — Estado de SesionSupervision

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
 :doc:`/requisitos/casos-uso/supervision/uc-sup-01/index`
