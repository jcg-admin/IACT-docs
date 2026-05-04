17.9 Mensaje asíncrono — fire-and-forget
----------------------------------------

.. uml::

   @startuml
   participant "rpt_app" as Rpt
   database "audit_log" as Audit
   participant "log_app" as Log

   Rpt ->> Audit : registrar export iniciado
   Rpt ->> Log : notificar buzon (CNST_001)
   @enduml
