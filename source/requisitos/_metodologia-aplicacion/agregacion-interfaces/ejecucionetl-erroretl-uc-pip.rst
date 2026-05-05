3.1 EjecucionETL ● ErrorETL (UC_PIP)
------------------------------------

.. uml::

   @startuml
   allowmixing

   class EjecucionETL {
     - id : Integer
     - fecha_inicio : DateTime
     - fecha_fin : DateTime
     - estado : Enum
     + cargarDesdeIVR()
   }

   class ErrorETL {
     - codigo : String
     - mensaje : String
     - tabla : String
     - timestamp : DateTime
   }

   class FilaCargada {
     - tabla : String
     - id_origen : Integer
     - timestamp : DateTime
   }

   EjecucionETL "1" *-- "0..*" ErrorETL    : compone
   EjecucionETL "1" *-- "0..*" FilaCargada : compone

   note right of EjecucionETL
     Composición:
       si la EjecucionETL se purga
       (UC_PIP), sus ErrorETL y
       FilaCargada se eliminan
       en cascada. No tienen
       sentido fuera de la
       ejecución que los generó.
   end note
   @enduml
