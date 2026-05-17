17.8 Mensaje síncrono y respuesta
---------------------------------

.. uml::

   @startuml
   participant "Browser" as Browser
   participant "rpt_app" as Rpt

   Browser -> Rpt : GET /dashboard
   Rpt --> Browser : 200 OK (HTML + datos)
   @enduml
