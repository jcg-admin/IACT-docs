.. meta::
 :artefacto: AT_DM_CLASS_SAVED_VIEW
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_saved_view:

=========
SavedView
=========

Vista guardada de un reporte con filtros fijos. Permite al usuario
guardar una configuracion de filtros para reutilizarla. Se desactiva,
no se elimina (BR-009 v2.0.0).

.. uml::
 :caption: Clase SavedView — vista guardada de reporte con filtros.

 @startuml

 class SavedView {
   + view_id : UUID
   + owner_user_id : UUID
   + report_id : UUID
   + filters_snapshot : List<Filter>
   + name : String
   + state : ViewState
   --
   + save()               <<save_view>>
   + load()
   + deactivate()         <<BR-009>>
 }

 enum ViewState {
   ACTIVE
   INACTIVE
 }

 SavedView -- ViewState

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/report`
