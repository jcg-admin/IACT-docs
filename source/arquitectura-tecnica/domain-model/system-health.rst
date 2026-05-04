.. meta::
 :artefacto: AT_DM_CLASS_SYSTEM_HEALTH
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_system_health:

============
SystemHealth
============

Snapshot efimero del estado de salud del sistema. Por D-05 no es un
log en sentido estricto sino un snapshot de estado. Vive en el
bounded context Logs por cohesion con MOD_Logs y politica de
retencion CNST-024 compartida.

.. uml::
 :caption: Clase SystemHealth — snapshot de estado de salud del sistema.

 @startuml

 class SystemHealth {
   + snapshot_id : UUID
   + captured_at : DateTime
   + cpu_usage_pct : Double
   + memory_usage_pct : Double
   + disk_usage_pct : Double
   + services_status : Map<String,String>
   --
   + snapshot()           <<sistema>>
   + view()               <<view_system_health>>
 }

 note bottom of SystemHealth
   D-05: NO es un log; snapshot efimero de estado.
   Retencion per CNST-024.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/bc-logs`
