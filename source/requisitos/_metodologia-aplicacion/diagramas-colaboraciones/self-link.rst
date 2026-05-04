14.2 Self-link
--------------

.. uml::

   @startuml
   allowmixing

   object ":EvaluadorAlertas" as EvaluadorAlertas

   EvaluadorAlertas -- EvaluadorAlertas : "1: revisar_umbrales()"
   @enduml
