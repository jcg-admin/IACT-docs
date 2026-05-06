2.1 Funcion ◇ Grupo (catálogo RBAC IACT)
----------------------------------------

.. uml::

   @startuml
   allowmixing

   class Group {
     - id : Integer
     - name : String
   }
   class Function {
     - code : String
     - description : String
   }

   Group "*" o-- "*" Function : contains
   note right of Function
     Una función (capacidad atómica) PUEDE
     existir sin pertenecer a ningún grupo;
     pertenece a múltiples grupos
     simultáneamente (predefinidos
     AGR-001..012 y/o creados via
     UC_PERM_05). Si un grupo se elimina,
     las funciones siguen vivas en el
     catálogo de 64 funciones activas (77 declaradas, 13 reservadas open-closed) (CNST_029).
   end note
   @enduml
