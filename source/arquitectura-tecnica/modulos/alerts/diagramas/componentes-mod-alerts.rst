.. meta::
 :artefacto: ARQ_MOD_006_DIAG_COMPONENTES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/alerts/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_006_componentes_mod_alerts:

=================================
Componentes del modulo de Alertas
=================================

.. uml::
 :caption: Componentes de MOD_Alerts y sus dependencias.

 @startuml

 component "AlertEvaluator\n(evaluacion periodica)" as Alertevaluator
 component "configure_team_alerts\n(configuracion)" as configure_team_alerts
 component "view_alerts\n(consulta)" as CONSULTA_ALERTAS
 component "acknowledge_alert\n(reconocimiento)" as acknowledge_alert
 component "InternalMailbox\n(notificacion)" as Internalmailbox

 database "AlertThreshold\n(umbrales configurados)" as Alertthreshold
 database "AlertEvent\n(historico alertas)" as HISTORICO_IVR

 configure_team_alerts --> Alertthreshold : CRUD umbrales
 Alertevaluator --> Alertthreshold : leer umbrales
 Alertevaluator --> HISTORICO_IVR : registrar nueva alerta
 Alertevaluator --> Internalmailbox : notificar suscriptores
 CONSULTA_ALERTAS --> HISTORICO_IVR : consultar alertas activas
 acknowledge_alert --> HISTORICO_IVR : actualizar estado reconocida

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/alerts/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
