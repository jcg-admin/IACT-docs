6.1 Jerarquía de Usuario en IACT
--------------------------------

.. uml::

   @startuml

   class Usuario {
     - id : Integer
     - email : String
     - password_hash : String
     + login()
     + logout()
   }

   class Operador {
     + verDashboard()
     + verAlertasActivas()
   }

   class Supervisor {
     - centros : List<Integer>
     + verReportesHistoricos()
     + reconocerAlerta()
   }

   class AdminAcceso {
     + asignarFunciones()
     + revocarFunciones()
   }

   class AdminPipeline {
     + supervisarETL()
     + solicitarReintento()
   }

   class Auditor {
     + consultarAuditoria()
     + generarReporteCompliance()
   }

   Usuario <|-- Operador
   Usuario <|-- Supervisor
   Usuario <|-- AdminAcceso
   Usuario <|-- AdminPipeline
   Usuario <|-- Auditor
   note right of Usuario
     Cada rol "es un tipo de"
     Usuario. Todos heredan
     login(), logout().
   end note
   @enduml
