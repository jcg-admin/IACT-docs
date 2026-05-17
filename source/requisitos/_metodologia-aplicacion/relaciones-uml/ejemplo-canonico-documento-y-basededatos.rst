Ejemplo canónico — ``Documento`` y ``BaseDeDatos``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando una clase ``Documento`` hereda de ``BaseDeDatos``
solo para obtener métodos de persistencia, hay herencia por
construcción. Un documento **no es-una** base de datos —
es una violación semántica clara.

Diseño incorrecto (herencia por construcción):

.. uml::

   @startuml
   title Diseno incorrecto — herencia por construccion

   class Database {
     + save()
     + load()
     + delete()
   }

   class Document {
     - content : String
     - title : String
     + editContent()
     + showDocument()
   }

   Document --|> Database
   note right of Document
     Document NO es-una Database.
     La herencia miente sobre el dominio.
   end note
   @enduml

Diseño correcto (composición):

.. uml::

   @startuml
   title Diseno correcto — composicion

   class Database {
     + save()
     + load()
     + delete()
   }

   class CorrectDocument {
     - content : String
     - title : String
     - persistence : Database
     + editContent()
     + showDocument()
     + saveDocument()
   }

   CorrectDocument o-- Database : has-a
   note right of CorrectDocument
     CorrectDocument tiene-un
     Database como componente
     (composicion).
   end note
   @enduml
