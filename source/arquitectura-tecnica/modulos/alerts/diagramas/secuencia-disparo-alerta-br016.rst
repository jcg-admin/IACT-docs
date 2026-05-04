.. meta::
 :artefacto: ARQ_MOD_006_DIAG_SECUENCIA_DISPARO
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/alerts/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_006_secuencia_disparo_alerta:

=====================================
Secuencia de Disparo de Alerta BR-016
=====================================

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
   Alertevaluator -> Internalmailbox : registrar notificacion\na suscriptores activos
   Internalmailbox --> view_alerts : mensaje en buzon
 else tasa <= 30%
   Alertevaluator -> Alertevaluator : no disparar alerta
 end

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/alerts/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
