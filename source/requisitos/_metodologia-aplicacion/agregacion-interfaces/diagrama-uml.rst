Diagrama UML
~~~~~~~~~~~~

.. uml::

   @startuml
   allowmixing

   class Universidad {
     - estudiantes : List<Estudiante>
     - nombre : String
     + agregarEstudiante(e : Estudiante)
     + removerEstudiante(e : Estudiante)
     + transferirEstudiante(e, otra)
     + tieneEstudiante(e) : boolean
     + cantidadEstudiantes() : int
   }

   class Estudiante {
     - id : String
     - nombre : String
     - estado : String
     + cambiarEstado(nuevo : String)
   }

   Universidad o-- "0..*" Estudiante
   note bottom of Estudiante
     Existe independientemente
     de la Universidad
   end note
   @enduml
