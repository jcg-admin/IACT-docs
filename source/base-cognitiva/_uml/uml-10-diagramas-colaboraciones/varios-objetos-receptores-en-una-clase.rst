Varios objetos receptores en una clase
--------------------------------------

En ocasiones un objeto envía un mensaje a diversos objetos de la
misma clase. Por ejemplo: un profesor pide a un grupo de
estudiantes que entreguen una tarea.

En el diagrama de colaboraciones, la representación de los
diversos objetos es una **pila de rectángulos** que se extienden
"desde atrás". Agregue una condición entre corchetes precedida
por un asterisco para indicar que el mensaje irá a todos los
objetos.

.. uml::

   @startuml
   allowmixing

   object ":Profesor" as P
   object ":Estudiante" as E1
   object ":Estudiante " as E2
   object ":Estudiante  " as E3

   P -> E1 : "*[para todos los estudiantes]\n1: entregarTarea()"
   P -> E2 : "*[para todos los estudiantes]\n1: entregarTarea()"
   P -> E3 : "*[para todos los estudiantes]\n1: entregarTarea()"
   note right of E3
     pila de receptores
     (mismo mensaje "1")
   end note
   @enduml

En algunos casos, el orden del mensaje enviado es importante.
Por ejemplo, un empleado bancario da servicio a cada cliente
conforme fue llegando a la fila. Esto se representa con un
``mientras`` cuya condición implica orden:

.. uml::

   @startuml
   allowmixing

   object ":EmpleadoBancario" as EB
   object ":Cliente" as C1
   object ":Cliente " as C2
   object ":Cliente  " as C3

   EB -> C1 : "*[posición = 1..n]\n1: atender()"
   EB -> C2 : "*[posición = 1..n]\n1: atender()"
   EB -> C3 : "*[posición = 1..n]\n1: atender()"
   @enduml
