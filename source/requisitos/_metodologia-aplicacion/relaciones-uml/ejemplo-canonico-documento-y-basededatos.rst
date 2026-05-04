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

   class BaseDeDatos {
     + guardar()
     + cargar()
     + eliminar()
   }

   class Documento {
     - contenido : String
     - titulo : String
     + editarContenido()
     + mostrarDocumento()
   }

   Documento --|> BaseDeDatos
   note right of Documento
     Documento NO es-una BaseDeDatos.
     La herencia miente sobre el dominio.
   end note
   @enduml

Diseño correcto (composición):

.. uml::

   @startuml
   title Diseno correcto — composicion

   class BaseDeDatos {
     + guardar()
     + cargar()
     + eliminar()
   }

   class DocumentoCorrecto {
     - contenido : String
     - titulo : String
     - persistencia : BaseDeDatos
     + editarContenido()
     + mostrarDocumento()
     + guardarDocumento()
   }

   DocumentoCorrecto o-- BaseDeDatos : tiene-un
   note right of DocumentoCorrecto
     DocumentoCorrecto tiene-un
     BaseDeDatos como componente
     (composicion).
   end note
   @enduml
