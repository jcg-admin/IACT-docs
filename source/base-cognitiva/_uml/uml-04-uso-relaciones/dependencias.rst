Dependencias
============

Cuando una clase **utiliza** a otra, a esto se le llama
**dependencia**.

El uso más común de una dependencia es mostrar que la **firma de
la operación** de una clase utiliza a otra clase.

Ejemplo: suponga que diseñará un sistema que muestra formularios
corporativos en pantalla para que los empleados los llenen. El
empleado utiliza un menú para seleccionar el formulario. Hay una
clase ``Sistema`` y una clase ``Formulario``. La clase
``Sistema`` tiene ``mostrarFormulario(f : Form)``; el formulario
que el sistema desplegará dependerá del que elija el usuario.

La notación de UML es una **línea discontinua** con una punta de
flecha en forma de **triángulo sin relleno** que apunta a la
clase de la que depende.

.. uml::

   @startuml

   class Sistema {
     mostrarFormulario(f : Form)
   }
   class Formulario
   Sistema ..|> Formulario : <<usa>>
   @enduml

----
