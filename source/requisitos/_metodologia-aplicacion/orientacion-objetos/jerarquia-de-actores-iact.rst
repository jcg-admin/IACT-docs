3.1 Jerarquía de actores IACT
-----------------------------

.. uml::

   @startuml

   class Usuario {
     - id : Integer
     - email : String
     - password_hash : String
     - is_active : Boolean
     - segmento : SegmentoDatos
     - created_at : DateTime
     + login(email, password) : Boolean
     + logout() : void
     + changePassword(old, new) : void
   }

   class Operador {
     + verDashboard() : Dashboard
     + verAlertasActivas() : List<Alerta>
   }

   class Supervisor {
     - centros : List<Integer>
     + verReportesHistoricos() : List<Reporte>
     + reconocerAlerta(id) : void
   }

   class AdminAcceso {
     + asignarFunciones(usuario, funciones) : void
     + asignarAgrupador(usuario, AGR_id) : void
     + concederPermisoTemporal(...) : void
   }

   class AdminPipeline {
     + supervisarETL() : EstadoETL
     + solicitarReintento(ejecucion_id) : void
   }

   class Auditor {
     + consultarAuditoria(filtros) : List<EventoAud>
     + generarReporteCompliance() : Reporte
   }

   Usuario <|-- Operador
   Usuario <|-- Supervisor
   Usuario <|-- AdminAcceso
   Usuario <|-- AdminPipeline
   Usuario <|-- Auditor

   note right of Usuario
     Herencia: cada rol "es un tipo
     de" Usuario. Todos heredan
     login(), logout(),
     changePassword(). El segmento
     restringe los datos visibles
     (BR_012).
   end note
   @enduml
