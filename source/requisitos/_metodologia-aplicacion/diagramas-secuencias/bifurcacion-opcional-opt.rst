17.13 Bifurcación opcional ``opt``
----------------------------------

.. uml::

   @startuml
   participant "rpt_app" as Rpt
   participant "log_app" as Log

   Rpt -> Rpt : encolar export

   opt [supervisor.notif_buzon == true]
     Rpt ->> Log : notificar (CNST_001)
   end
   @enduml
