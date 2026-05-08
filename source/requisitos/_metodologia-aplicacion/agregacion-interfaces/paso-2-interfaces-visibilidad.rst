8.2 Paso 2 — interfaces + visibilidad
-------------------------------------

.. uml::

   @startuml
   allowmixing

   interface IExportable <<interface>> {
     + export(format)
   }
   class Report {
     - raw_sql : String
     # recordQuery()
     + export(format)
   }
   class SystemLog {
     - service : String
     + export(format)
   }
   Report ..|> IExportable
   SystemLog ..|> IExportable
   @enduml
