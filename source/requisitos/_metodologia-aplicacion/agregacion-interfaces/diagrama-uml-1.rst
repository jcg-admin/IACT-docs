Diagrama UML
~~~~~~~~~~~~

.. uml::

   @startuml
   allowmixing

   class Documento {
     - parrafos : List<Parrafo>
     - titulo : String
     + modificarParrafo(pos, contenido)
     + agregarParrafo(contenido)
     + getContenidoParrafo(pos) : String
     + getNumeroParrafos() : int
   }

   class Parrafo {
     - contenido : String
     - posicion : int
     ~ getContenido() : String
     ~ modificarContenido(nuevo : String)
   }

   Documento *-- "1..*" Parrafo
   note right of Parrafo
     No existe independientemente.
     Pertenece a un unico Documento.
     Se destruye con el Documento.
   end note
   @enduml
