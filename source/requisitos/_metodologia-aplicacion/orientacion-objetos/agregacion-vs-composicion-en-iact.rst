7.2 Agregación vs composición en IACT
-------------------------------------

**Agregación** — las partes pueden existir sin el todo:

.. uml::

   @startuml

   class Group
   class Function
   Group "*" o-- "*" Function : contains
   note right of Function
     Una función (capacidad atómica)
     puede ser parte de varios grupos
     (predefinidos AGR-001..012 o
     creados via UC_PERM_05). Si un
     grupo se elimina, las funciones
     siguen existiendo en el catálogo.
   end note
   @enduml

**Composición** — las partes no pueden existir sin el todo:

.. uml::

   @startuml

   class ETLExecution
   class ETLError
   class LoadedRow
   ETLExecution "1" *-- "0..*" ETLError    : composes
   ETLExecution "1" *-- "0..*" LoadedRow : composes
   note right of ETLExecution
     Si la ETLExecution se purga
     (UC_PIP), sus errores y filas
     cargadas no tienen sentido
     fuera de ella.
   end note
   @enduml
