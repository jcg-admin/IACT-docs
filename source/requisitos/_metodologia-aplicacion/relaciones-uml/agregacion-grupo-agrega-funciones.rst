7.1 Agregación — Grupo agrega Funciones
---------------------------------------

.. uml::

   @startuml

   class Grupo
   class Funcion
   Grupo "1" o-- "0..*" Funcion : contiene
   note right of Funcion
     Agregación:
     si el Grupo se elimina,
     la Funcion sigue existiendo
     en el catálogo de 74 funciones
     (CNST_029) y puede pertenecer
     a otros grupos.
   end note
   @enduml
