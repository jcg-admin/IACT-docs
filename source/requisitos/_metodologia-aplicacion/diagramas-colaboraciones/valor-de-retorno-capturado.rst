14.10 Valor de retorno capturado
--------------------------------

.. uml::

   @startuml
   allowmixing

   object ":rpt_app" as Rpt
   object ":Reporte" as Reporte

   Rpt -> Reporte : "1: tarea_id := exportar(req)"
   @enduml
