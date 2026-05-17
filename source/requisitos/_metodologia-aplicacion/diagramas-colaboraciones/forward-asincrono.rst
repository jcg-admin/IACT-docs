14.4 Forward asíncrono
----------------------

.. uml::

   @startuml
   allowmixing

   object ":rpt_app" as Rpt
   object ":audit_log" as Audit

   Rpt -> Audit : "1: registrar_evento()"
   @enduml
