Ejemplo IACT — snapshot pre-refactor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Snapshot de ``ExportarReporteFacade`` y sus
dependencias antes de un hipotético refactor:

.. uml::

   @startuml
   title Snapshot pre-refactor — ExportarReporteFacade

   class ExportarReporteFacade {
     - _perm : SecRules
     - _rpt : Reporte
     - _worker : Worker
     - _audit : Bus
     - _notify : Buzon
     --
     + __init__(perm : SecRules, rpt : Reporte, \
       worker : Worker, audit : Bus, notify : Buzon)
     + ejecutar(user : Usuario, cfg : ConfigExport) : TareaId
     - _validar_filtros(cfg : ConfigExport) : bool
     - _disparar_audit(user : Usuario, tarea : TareaId)
     - _disparar_notify(cfg : ConfigExport, tarea : TareaId)
   }

   class SecRules {
     + verificar(user : Usuario, fn_id : str) : bool
   }

   class Reporte {
     - _filtros : List<Filtro>
     --
     + cuota_disponible(user : Usuario) : bool
     + validar_filtro(f : Filtro) : bool
   }

   class Worker {
     + encolar_tarea(cfg : ConfigExport) : TareaId
   }

   class Bus {
     {static} + publicar(evento : Evento)
   }

   class Buzon {
     + notificar_buzon(destinatarios : List<UserId>, \
       mensaje : str)
   }

   ExportarReporteFacade --> SecRules
   ExportarReporteFacade --> Reporte
   ExportarReporteFacade --> Worker
   ExportarReporteFacade --> Bus
   ExportarReporteFacade --> Buzon
   @enduml
