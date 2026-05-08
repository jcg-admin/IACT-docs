.. meta::
 :artefacto: AT_DESIGN_STATE_EXPORT_JOB
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: ExportJob
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_state_export_job:

============================================================
Design View — Ciclo de Vida: ExportJob
============================================================

Maquina de estados de la entidad ``ExportJob``. Cubre el ciclo
de un export asincrono desde el enqueue (pending) hasta ready
(disponible para descarga) o failed/expired.

.. uml::
 :caption: ExportJob FSM — pending -> processing -> ready | failed.

 @startuml

 [*] --> pending : User.enqueue()

 pending --> processing : Worker.dequeue()
 pending --> cancelled : User.cancel()

 processing --> ready : success
 processing --> failed : error

 ready --> downloaded : User.download()
 ready --> expired : ttl_reached

 downloaded --> expired : ttl_reached

 expired --> [*]
 failed --> [*]
 cancelled --> [*]

 note right of pending
   En cola del ExportWorker.
   Si scheduler periodico cancela
   por antiguedad -> cancelled.
 end note

 note right of ready
   download_url disponible.
   ttl tipico 24h. Tras download
   o ttl, queda expired.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/reports/sequence`
 - :doc:`/arquitectura-tecnica/design-view/reports/activity`
 - :doc:`/arquitectura-tecnica/design-view/reports/class`
 - :doc:`/arquitectura-tecnica/use-case-view/reports/uc-rpt-04-exportar-reporte`
 - :doc:`/arquitectura-tecnica/domain-model/export-job`
 - :doc:`/arquitectura-tecnica/domain-model/export-worker`
