7.2 Catálogo de funciones — instancia compartida
------------------------------------------------

.. uml::

   @startuml
   allowmixing

   class Funcion {
     - codigo : String
     - descripcion : String
     - modulo : String
     {static} - TOTAL : Integer = 42
     {static} + listarTodas() : List<Funcion>
     {static} + buscarPorCodigo(c : String) : Funcion
   }
   note right of Funcion
     - codigo / descripcion / modulo
       → instancia (cada Funcion es única)
     - TOTAL = 42 (CNST_029)
       → archivador (compartido por todas
         las instancias)
     - listarTodas / buscarPorCodigo
       → archivador (operaciones de catálogo)
   end note
   @enduml
