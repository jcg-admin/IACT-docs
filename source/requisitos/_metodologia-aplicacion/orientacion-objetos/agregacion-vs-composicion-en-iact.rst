7.2 Agregación vs composición en IACT
-------------------------------------

**Agregación** — las partes pueden existir sin el todo:

.. uml::

   @startuml

   class Grupo
   class Funcion
   Grupo "*" o-- "*" Funcion : contiene
   note right of Funcion
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

   class EjecucionETL
   class ErrorETL
   class FilaCargada
   EjecucionETL "1" *-- "0..*" ErrorETL    : compone
   EjecucionETL "1" *-- "0..*" FilaCargada : compone
   note right of EjecucionETL
     Si la EjecucionETL se purga
     (UC_PIP), sus errores y filas
     cargadas no tienen sentido
     fuera de ella.
   end note
   @enduml
