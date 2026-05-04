.. meta::
 :artefacto: AT_UC_ALR_03_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_03_domain:

===================================================
UC_ALR_03 — Reconocer Alerta: Domain Model
===================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index`.

.. uml::
 :caption: UC_ALR_03 — Domain Model

 @startuml

 left to right direction

 class Alert
 class AuditEvent
 class Alert

 Alert --> AuditEvent
 AuditEvent --> Alert

 @enduml


.. uml::
 :caption: UC_ALR_03 — Reconocer Alerta — Estado de Alerta

 @startuml
 hide empty description

 [*] --> Disparada : condicion detectada
 Disparada --> Activa : notificar usuario
 Activa --> Reconocida : usuario reconoce
 Reconocida --> Resuelta : resolver causa
 Resuelta --> [*] : cerrar alerta
 Activa --> Escalada : timeout sin reconocer
 Escalada --> Reconocida : reconocer escalada

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index`
