.. _arq-mod-006-diagramas:

================================================
ARQ_MOD_006 — Diagramas de Comportamiento
================================================


Ciclo de Vida de una Alerta
============================

.. uml::
 :caption: Estados de una alerta — desde el disparo hasta su resolucion.

 @startuml

 [*] --> PENDIENTE : condicion umbral detectada

 PENDIENTE --> ACTIVA : sistema confirma condicion\npersiste (evaluacion periodica)
 PENDIENTE --> [*] : condicion ya no se cumple\n(falsa alarma)

 ACTIVA --> RECONOCIDA : acknowledge_alert invoca UC_ALR_03
 ACTIVA --> ACTIVA : suscriptores notificados\nvia InternalMailbox (CNST-001)

 RECONOCIDA --> RESUELTA : operador marca como resuelta
 RESUELTA --> [*] : alerta archivada\n(inmutable, CNST-025)

 note right of ACTIVA
   Nunca por email (CNST-001).
   BR-016: tasa abandono >30%
   genera alerta automatica.
 end note

 @enduml

----

Secuencia de Disparo de Alerta BR-016
========================================

.. uml::
 :caption: Disparo automatico de alerta por tasa de abandono (BR-016 >30%).

 @startuml

 participant "ETLMonitor" as Etlmonitor
 participant "AlertEvaluator" as Alertevaluator
 database "AlertThreshold\n(configure_team_alerts)" as Alertthreshold
 participant "InternalMailbox" as Internalmailbox
 actor "view_alerts" as view_alerts

 Etlmonitor -> Alertevaluator : notificar fin de Etlmonitor exitoso
 Alertevaluator -> Alertthreshold : consultar umbrales activos
 Alertthreshold --> Alertevaluator : umbral BR-016 (tasa_abandono > 30%)
 Alertevaluator -> Alertevaluator : calcular tasa actual de\nabandonos del trimestre
 alt tasa > 30%
   Alertevaluator -> Alertevaluator : crear alerta PENDIENTE
   Alertevaluator -> Alertevaluator : confirmar condicion persiste
   Alertevaluator -> Internalmailbox : INSERT notificacion\na suscriptores activos
   Internalmailbox --> view_alerts : mensaje en buzon
 else tasa <= 30%
   Alertevaluator -> Alertevaluator : no disparar alerta
 end

 @enduml

----

Componentes del modulo de Alertas
====================================

.. uml::
 :caption: Componentes de MOD_Alerts y sus dependencias.

 @startuml

 component "AlertEvaluator\n(evaluacion periodica)" as Alertevaluator
 component "configure_team_alerts\n(configuracion)" as configure_team_alerts
 component "view_alerts\n(consulta)" as VIEW
 component "acknowledge_alert\n(reconocimiento)" as acknowledge_alert
 component "InternalMailbox\n(notificacion)" as Internalmailbox

 database "AlertThreshold\n(umbrales configurados)" as Alertthreshold
 database "AlertEvent\n(historico alertas)" as HIST

 configure_team_alerts --> Alertthreshold : CRUD umbrales
 Alertevaluator --> Alertthreshold : leer umbrales
 Alertevaluator --> HIST : INSERT nueva alerta
 Alertevaluator --> Internalmailbox : notificar suscriptores
 VIEW --> HIST : SELECT alertas activas
 acknowledge_alert --> HIST : UPDATE estado reconocida

 @enduml
