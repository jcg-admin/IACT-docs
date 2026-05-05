Ejemplo canónico — ``Documento`` → ``ContratoCorporativo``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una clase base ``Documento`` que se transforma en
``ContratoCorporativo``: ya no solo es un documento que
**almacena información**, sino que se convierte en un
**instrumento legal** que ejecuta y valida acciones
corporativas. El concepto fundamental cambia de
"almacenamiento de información" a "instrumento legal
ejecutable".

.. uml::

   @startuml

   class Documento {
     - contenido : String
     - titulo : String
     + editar()
     + mostrar()
   }

   class ContratoCorporativo {
     - firmantes : List
     - estado_legal : String
     + ejecutar()
     + validar()
     + revocar()
   }

   Documento <|-- ContratoCorporativo
   note right of ContratoCorporativo
     Mantiene estructura de Documento,
     pero el concepto se transforma:
     "almacena informacion" se convierte
     en "instrumento legal ejecutable".
     Requiere ADR explicito.
   end note
   @enduml
