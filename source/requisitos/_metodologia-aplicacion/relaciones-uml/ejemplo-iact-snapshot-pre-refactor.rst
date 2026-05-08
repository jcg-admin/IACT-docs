Ejemplo IACT — snapshot pre-refactor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Snapshot de ``ExportarReporteFacade`` y sus
dependencias antes de un hipotético refactor:

.. uml::

   @startuml
   title Snapshot pre-refactor — ExportReportFacade

   class ExportReportFacade {
     - _perm : SecRules
     - _rpt : Report
     - _worker : Worker
     - _audit : Bus
     - _notify : Mailbox
     --
     + __init__(perm : SecRules, rpt : Report, \
       worker : Worker, audit : Bus, notify : Mailbox)
     + execute(user : User, cfg : ExportConfig) : TaskId
     - _validate_filters(cfg : ExportConfig) : bool
     - _trigger_audit(user : User, task : TaskId)
     - _trigger_notify(cfg : ExportConfig, task : TaskId)
   }

   class SecRules {
     + verify(user : User, fn_id : str) : bool
   }

   class Report {
     - _filters : List<Filter>
     --
     + quota_available(user : User) : bool
     + validate_filter(f : Filter) : bool
   }

   class Worker {
     + enqueue_task(cfg : ExportConfig) : TaskId
   }

   class Bus {
     {static} + publish(event : Event)
   }

   class Mailbox {
     + notify_mailbox(recipients : List<UserId>, \
       message : str)
   }

   ExportReportFacade --> SecRules
   ExportReportFacade --> Report
   ExportReportFacade --> Worker
   ExportReportFacade --> Bus
   ExportReportFacade --> Mailbox
   @enduml
