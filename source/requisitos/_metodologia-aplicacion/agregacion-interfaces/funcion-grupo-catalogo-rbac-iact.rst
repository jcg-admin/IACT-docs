2.1 Funcion ◇ Grupo (catálogo RBAC IACT)
----------------------------------------

.. uml::

   @startuml
   allowmixing

   class Grupo {
     - id : Integer
     - nombre : String
   }
   class Funcion {
     - codigo : String
     - descripcion : String
   }

   Grupo "*" o-- "*" Funcion : contiene
   note right of Funcion
     Una función (capacidad atómica) PUEDE
     existir sin pertenecer a ningún grupo;
     pertenece a múltiples grupos
     simultáneamente (predefinidos
     AGR-001..012 y/o creados via
     UC_PERM_05). Si un grupo se elimina,
     las funciones siguen vivas en el
     catálogo de 74 funciones (CNST_029).
   end note
   @enduml
