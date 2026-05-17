.. meta::
 :artefacto: AT_IMPL_MOD_ALERTS
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_alerts:

==========================================
Implementation View — MOD_Alerts
==========================================

Componentes y paquetes de codigo del modulo de alertas.
Cubre evaluacion de ``Threshold``, ciclo de vida de ``Alert``
(ACTIVE→ACKNOWLEDGED, D-02) y ``Subscription`` de supervisores.

.. uml::
 :caption: Implementation View MOD_Alerts — componentes de gestion de alertas.

 @startuml

 package "MOD_Alerts" {
   component "AlertView\nAcknowledgeAlertView\nSubscriptionView" as AlertView <<api>>
   component "AlertSerializer\nSubscriptionSerializer" as AlertSerializer <<serializer>>
   component "AlertService\nevaluar Threshold\ngestionar ciclo de vida Alert" as AlertService <<service>>
   component "AlertRepository\nThresholdRepository\nSubscriptionRepository" as AlertRepo <<repository>>
   component "AlertORM\nThresholdORM\nSubscriptionORM" as AlertORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 AlertView --> AlertSerializer : valida
 AlertView --> AlertService : invoca
 AlertService --> AlertRepo : consulta / persiste
 AlertRepo --> AlertORM : mapea
 AlertORM --> AlmacenDatos : SQL

 note right of AlertService
   Alert{state:AlertState}: ACTIVE → ACKNOWLEDGED <<D-02>>.
   Threshold.evaluate() dispara Alert si se supera.
   Subscription notifica a supervisores registrados.
   AuditEvent{CONFIG_CHANGED} en acknowledge.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/alert`
 :doc:`/arquitectura-tecnica/domain-model/threshold`
 :doc:`/arquitectura-tecnica/domain-model/subscription`
