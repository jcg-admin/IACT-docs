7.1 Agregación — Grupo agrega Funciones
---------------------------------------

.. uml::

   @startuml

   class Group
   class Function
   Group "1" o-- "0..*" Function : contains
   note right of Function
     Agregación:
     si el Group se elimina,
     la Function sigue existiendo
     en el catálogo de 74 funciones
     (CNST_029) y puede pertenecer
     a otros grupos.
   end note
   @enduml
