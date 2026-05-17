Cómo representar las interfaces
-------------------------------

Tiene **dos formas** de representar a un componente y sus
interfaces:

**Primera forma** — la interfaz como un rectángulo que contiene
la información, conectado al componente por una **línea
discontinua y una punta de flecha de triángulo sin rellenar**
(realización):

.. uml::

   @startuml
   allowmixing

   interface IEditable {
     + abrir()
     + guardar()
     + cerrar()
   }
   component "Editor.exe" as Ed
   Ed ..|> IEditable
   @enduml

**Segunda forma** — la interfaz como un**pequeño círculo**
(*lollipop*) conectado al componente por una**línea continua**.
Aquí la línea representa la realización:

.. uml::

   @startuml
   allowmixing

   component "Editor.exe" as Ed
   () "IEditable" as I
   Ed -- I
   @enduml

Además de la realización, puede representar la **dependencia**
(relación entre un componente y una **interfaz de importación**).
La dependencia se vislumbra como una **línea discontinua con una
punta de flecha**.

Puede mostrar **realización y dependencia en el mismo diagrama**:

.. uml::

   @startuml
   allowmixing

   component "Editor.exe"   as Ed
   component "Impresora.dll" as Imp
   () "IEditable"   as IE
   () "IImprimible" as II

   Ed -- IE              : (realiza)
   Ed ..> II             : <<usa>> (depende)
   Imp -- II             : (realiza)
   @enduml
