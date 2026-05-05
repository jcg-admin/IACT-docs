Una página Web con un applet Java
---------------------------------

Modela un programa con un *applet* que ejecuta el juego de dados
*Craps* en una página Web, usando una clase ``Die`` (para crear
los dados).

Archivos en el directorio ``Tirodedados``:

- ``Craps.html`` — página Web.
- ``Craps.java`` — código fuente del applet.
- ``Craps.class`` — código objeto (componente).
- ``Die.java`` — código fuente de la clase Die.
- ``Die.class`` — código objeto.

``Craps.html`` depende de ``Craps.class`` y ``Die.class``. Cada
``.class`` es un componente y cada uno es la implementación de
una clase.

Tanto ``Craps.java`` como ``Die.java`` **importan** ``java.awt``,
un grupo de clases que muestran y controlan la GDI. Y
``Craps.java`` es un applet, por lo que se hereda desde
``java.applet.Applet``. Finalmente, ``Craps.java`` importa
``java.awt.event`` e implementa la interfaz ``ActionListener``.

.. uml::

   @startuml

   package "Tirodedados" {
     component "Craps.html"  as HTML
     component "Craps.class" as CC
     component "Craps.java"  as CJ
     component "Die.class"   as DC
     component "Die.java"    as DJ
   }

   package "JDK" {
     component "java.awt"        as AWT
     component "java.awt.event"  as AWTE
     component "java.applet.Applet" as APPLET
     interface ActionListener as AL
   }

   HTML ..> CC : <<usa>>
   HTML ..> DC : <<usa>>

   CJ ..> AWT  : <<importa>>
   DJ ..> AWT  : <<importa>>

   CJ ..> AWTE   : <<importa>>
   CJ ..|> AL    : <<implements>>
   CJ --|> APPLET
   @enduml

  Generar un modelo a partir de un código existente se conoce
  como **ingeniería inversa**.
