16.8 Dependencia entre componentes
----------------------------------

.. uml::

   @startuml

   component "rpt_app" as Rpt
   component "aud_app" as Aud

   Rpt ..> Aud : registra eventos\n(CNST_025)
   @enduml
