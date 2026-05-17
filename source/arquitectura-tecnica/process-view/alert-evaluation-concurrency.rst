.. meta::
 :artefacto: AT_PROC_ALERTAS_PARALELAS
 :tipo: Diagrama Arquitectonico — Process View
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_proc_alertas_paralelas:

======================================================
Process View — Evaluacion Paralela de Alertas
======================================================

Patron de concurrencia para evaluacion paralela de ``Threshold`` y
gestion del ciclo de vida de ``Alert`` (ACTIVE→ACKNOWLEDGED, D-02).
Incluye deduplicacion para evitar alertas duplicadas.

.. uml::
 :caption: Process View — evaluacion paralela de umbrales y deduplicacion de alertas.

 @startuml

 participant EvaluadorAlertas <<scheduler>>
 participant EvaluadorWorker_1 <<worker>>
 participant EvaluadorWorker_2 <<worker>>
 participant AlertService       <<service>>
 database    AlmacenDatos       <<postgresql>>

 EvaluadorAlertas -> EvaluadorWorker_1 : evaluar(threshold_A)
 EvaluadorAlertas -> EvaluadorWorker_2 : evaluar(threshold_B)
 activate EvaluadorWorker_1
 activate EvaluadorWorker_2

 EvaluadorWorker_1 -> AlmacenDatos : SELECT metricas\nWHERE threshold_id=A
 AlmacenDatos --> EvaluadorWorker_1 : valor actual

 EvaluadorWorker_2 -> AlmacenDatos : SELECT metricas\nWHERE threshold_id=B
 AlmacenDatos --> EvaluadorWorker_2 : valor actual

 EvaluadorWorker_1 -> AlertService : notificarSupera(threshold_A)
 deactivate EvaluadorWorker_1

 EvaluadorWorker_2 -> AlertService : notificarSupera(threshold_B)
 deactivate EvaluadorWorker_2

 activate AlertService

 AlertService -> AlmacenDatos : SELECT alerts\nWHERE threshold_id=A\nAND state=ACTIVE
 AlmacenDatos --> AlertService : alerta existente?

 alt no existe alerta activa (deduplicacion)
   AlertService -> AlmacenDatos : INSERT alerts\n{state:ACTIVE, threshold_id:A}
   AlertService -> AlmacenDatos : notificar Subscriptions
 else alerta ya existe en state=ACTIVE
   AlertService -> AlertService : descartar (duplicado)
 end

 AlertService -> AlmacenDatos : INSERT alerts\n{state:ACTIVE, threshold_id:B}
 deactivate AlertService

 note over AlertService
   D-02: Alert transicion ACTIVE → ACKNOWLEDGED.
   ACKNOWLEDGED = supervisor reconocio la alerta.
   No existe transicion ACTIVE → CLOSED directa.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/alert`
 :doc:`/arquitectura-tecnica/domain-model/threshold`
 :doc:`/arquitectura-tecnica/domain-model/subscription`
