Una página Web con controles ActiveX
------------------------------------

ActiveX es el medio de Microsoft para agregar componentes a las
aplicaciones. Una propiedad de un componente ActiveX es su número
de identificación hexadecimal único de 32 bits, conocido como
**CLSID** (identificador de la clase).

En las páginas Web, los componentes ActiveX se encuentran y
trabajan con código escrito en algún lenguaje de scripting como
**VBScript**.

En este ejemplo, la página Web cuenta con un control Timer, dos
cuadros combinados y tres botones ActiveX. La página permite
animar el movimiento de una esfera (imagen ``.gif``).

Los controles ActiveX se encuentran en un componente separado
conocido como **Disposición** (*Layout*). La página HTML y la
disposición están en el mismo directorio.

.. uml::

   @startuml
   allowmixing

   package "Anim" {
     component "Anim.html" as HTML
     component "Layout.alx" as LAY
   }

   package "ActiveX Controls" {
     component "Timer"      as T
     component "ComboBox 1" as CB1
     component "ComboBox 2" as CB2
     component "Boton Iniciar" as B1
     component "Boton Detener" as B2
     component "Boton Reset"   as B3
   }

   note right of HTML
     <<VBScript>>
     Lenguaje de scripting que
     coordina los controles
     ActiveX. Mostrado como
     anotación porque no es un
     componente compilado.
   end note

   HTML ..> LAY : <<contiene>>
   LAY ..> T    : <<contiene>>
   LAY ..> CB1
   LAY ..> CB2
   LAY ..> B1
   LAY ..> B2
   LAY ..> B3
   @enduml
