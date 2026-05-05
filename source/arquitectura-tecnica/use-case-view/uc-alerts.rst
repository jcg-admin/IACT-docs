.. meta::
 :artefacto: AT_UC_MOD_ALERTS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_alerts:

====================================================
MOD_Alerts — Alertas y Notificaciones: UC por Modulo
====================================================

MOD_Alerts — Alertas y Notificaciones
========================================

Configuracion de umbrales criticos, recepcion y reconocimiento de
alertas del sistema IVR (BR-016: tasa de abandono >30%). Las alertas
se generan automaticamente por el motor de alertas y por el ETL.

.. uml::
 :caption: Figura 21 — MOD_Alerts: casos de uso

 @startuml
 left to right direction

 actor "configure_team_alerts" as configure_team_alerts
 actor "view_alerts" as view_alerts
 actor "acknowledge_alert" as acknowledge_alert
 actor "view_alert_history" as view_alert_history

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales\nde Alertas" as AL01
   usecase "UC_ALR_02\nVer Alertas Activas" as AL02
   usecase "UC_ALR_03\nReconocer Alerta" as AL03
   usecase "UC_ALR_04\nVer Historial\nde Alertas" as AL04
   usecase "UC_ALR_05\nNotificacion\nAutomatica ETL" as AL05
   usecase "Motor de Alertas\n(automatico)" as MOTOR_ALERTAS
 }

 configure_team_alerts --> AL01
 view_alerts --> AL02
 acknowledge_alert --> AL03
 view_alert_history --> AL04
 MOTOR_ALERTAS --> AL05

 AL02 ..> AL03 : <<extend>>
 AL05 ..> AL02 : <<extend>>
 AL01 ..> MOTOR_ALERTAS : <<include>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
