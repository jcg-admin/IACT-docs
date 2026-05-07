.. meta::
 :artefacto: AT_DM_CLASS_RESUMEN_SALUD
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_resumen_salud:

=============
ResumenSalud
=============

DTO inmutable que agrega el estado de salud del pipeline
ETL de supervision en un instante: runs activos, errores
recientes, lag temporal, ultimo exito y un estado general
discreto (verde/amarillo/rojo).

Aplica vocabulario STD-010 — termino canonico "Resumen de
Salud" en lugar de "Health Summary". Es producido por
``ResumenSaludBuilder`` y consumido por ``uc-pip-01``.

.. uml::
 :caption: ResumenSalud — DTO de estado de salud del
           pipeline ETL.

 @startuml

 class ResumenSalud {
   + estado_general : EstadoSalud
   + ultima_ejecucion : DateTime
   + ultimo_exito : DateTime
   + total_exitosas : Integer
   + total_fallidas : Integer
   + runs_activos : Integer
   + errores_recientes : Integer
   + lag_segundos : Integer
   + computed_at : DateTime
 }

 enum EstadoSalud {
   VERDE
   AMARILLO
   ROJO
 }

 ResumenSalud ..> EstadoSalud

 @enduml

Atributos
=========

- ``estado_general : EstadoSalud`` — discreto: VERDE
  (saludable), AMARILLO (degradado), ROJO (critico).
- ``ultima_ejecucion : DateTime`` — fin del ultimo run
  (exitoso o fallido).
- ``ultimo_exito : DateTime`` — fin del ultimo run
  exitoso.
- ``total_exitosas / total_fallidas`` — contadores en la
  ventana de calculo.
- ``runs_activos : Integer`` — runs en estado RUNNING.
- ``errores_recientes : Integer`` — errores ETL en la
  ventana.
- ``lag_segundos : Integer`` — diferencia entre ahora y
  ``ultimo_exito``.
- ``computed_at : DateTime`` — momento del calculo
  (inmutabilidad).

Restricciones aplicables
========================

- Inmutable — no tiene setters.
- ``estado_general`` se deriva por reglas configurables del
  builder, no se asigna externamente.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index` —
  consulta del estado de salud.

Relaciones
==========

- Producido por ``ResumenSaludBuilder.build``.
- Devuelto por ``SupervisionETLService.supervisar``.
- Consumido por la UI de uc-pip-01.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
