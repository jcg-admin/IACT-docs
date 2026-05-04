8.1 Paso 1 — agregación + composición
-------------------------------------

.. uml::

   @startuml
   allowmixing

   class Grupo
   class Funcion
   class EjecucionETL
   class ErrorETL

   Grupo "*" o-- "*" Funcion           : agregación
   EjecucionETL "1" *-- "0..*" ErrorETL : composición

   note right of Funcion
     Agregación: Funcion sobrevive
     al borrado de Grupo.
   end note
   note right of ErrorETL
     Composición: ErrorETL muere
     con la EjecucionETL.
   end note
   @enduml
