7.2 Catálogo de funciones — instancia compartida
------------------------------------------------

.. uml::

   @startuml
   allowmixing

   class Function {
     - code : String
     - description : String
     - module : String
     {static} - TOTAL : Integer = 42
     {static} + listAll() : List<Function>
     {static} + findByCode(c : String) : Function
   }
   note right of Function
     - code / description / module
       → instancia (cada Function es única)
     - TOTAL = 42 (CNST_029)
       → archivador (compartido por todas
         las instancias)
     - listAll / findByCode
       → archivador (operaciones de catálogo)
   end note
   @enduml
