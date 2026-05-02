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

 participant "ETLMonitor" as ETL
 participant "AlertEvaluator" as AE
 database "AlertThreshold\n(configure_team_alerts)" as TH
 participant "InternalMailbox" as MB
 actor "view_alerts" as USR

 ETL -> AE : notificar fin de ETL exitoso
 AE -> TH : consultar umbrales activos
 TH --> AE : umbral BR-016 (tasa_abandono > 30%)
 AE -> AE : calcular tasa actual de\nabandonos del trimestre
 alt tasa > 30%
   AE -> AE : crear alerta PENDIENTE
   AE -> AE : confirmar condicion persiste
   AE -> MB : INSERT notificacion\na suscriptores activos
   MB --> USR : mensaje en buzon
 else tasa <= 30%
   AE -> AE : no disparar alerta
 end

 @enduml

----

Componentes del modulo de Alertas
====================================

.. uml::
 :caption: Componentes de MOD_Alerts y sus dependencias.

 @startuml

 component "AlertEvaluator\n(evaluacion periodica)" as AE
 component "configure_team_alerts\n(configuracion)" as CFG
 component "view_alerts\n(consulta)" as VIEW
 component "acknowledge_alert\n(reconocimiento)" as ACK
 component "InternalMailbox\n(notificacion)" as MB

 database "AlertThreshold\n(umbrales configurados)" as TH
 database "AlertEvent\n(historico alertas)" as HIST

 CFG --> TH : CRUD umbrales
 AE --> TH : leer umbrales
 AE --> HIST : INSERT nueva alerta
 AE --> MB : notificar suscriptores
 VIEW --> HIST : SELECT alertas activas
 ACK --> HIST : UPDATE estado reconocida

 @enduml
