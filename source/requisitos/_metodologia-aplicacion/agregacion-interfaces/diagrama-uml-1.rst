Diagrama UML
~~~~~~~~~~~~

.. uml::

   @startuml
   allowmixing

   class Document {
     - paragraphs : List<Paragraph>
     - title : String
     + modifyParagraph(pos, content)
     + addParagraph(content)
     + getParagraphContent(pos) : String
     + getParagraphCount() : int
   }

   class Paragraph {
     - content : String
     - position : int
     ~ getContent() : String
     ~ modifyContent(new : String)
   }

   Document *-- "1..*" Paragraph
   note right of Paragraph
     No existe independientemente.
     Pertenece a un unico Document.
     Se destruye con el Document.
   end note
   @enduml
