.. meta::
 :artefacto: AT_UC_ALR_04_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_alr_04_domain_estado:

=======================================================
UC_ALR_04 — Ver Historial de Alertas — Estado de Alerta
=======================================================

.. uml::
 :caption: UC_ALR_04 — Ver Historial de Alertas — Estado de Alerta

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
 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/alerts/uc-alr-04/index`
