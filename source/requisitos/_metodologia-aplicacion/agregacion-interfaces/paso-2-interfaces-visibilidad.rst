8.2 Paso 2 — interfaces + visibilidad
-------------------------------------

.. uml::

   @startuml
   allowmixing

   interface IExportable <<interface>> {
     + exportar(formato)
   }
   class Reporte {
     - sql_crudo : String
     # registrarConsulta()
     + exportar(formato)
   }
   class LogSistema {
     - servicio : String
     + exportar(formato)
   }
   Reporte ..|> IExportable
   LogSistema ..|> IExportable
   @enduml
