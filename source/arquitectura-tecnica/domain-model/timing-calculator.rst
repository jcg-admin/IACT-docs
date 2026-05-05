.. meta::
 :artefacto: AT_DM_CLASS_TIMING_CALCULATOR
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Pendiente
 :version: 0.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_timing_calculator:

================
TimingCalculator
================

Calculadora de tiempos TTAK (time-to-acknowledge) y TTAR para historial de alertas.

.. TODO: Pendiente de desarrollo — agregar atributos canonicos, enums propios y
   relaciones completas.

.. uml::
 :caption: Clase TimingCalculator — stub pendiente de desarrollo.

 @startuml

 class TimingCalculator {
  + compute_ttak(alert)
  + compute_ttar(alert)
 }

 @enduml
