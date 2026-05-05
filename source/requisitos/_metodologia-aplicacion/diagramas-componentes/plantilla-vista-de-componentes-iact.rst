16.10 Plantilla — vista de componentes IACT
-------------------------------------------

.. uml::

   @startuml
   title Vista de componentes — <subdominio>

   package "iact.wsgi" {
     component "<app principal>" as Main
     component "<app dependencia>" as Dep
     interface IContrato
   }

   component "<sistema externo>" as Ext

   Dep ..|> IContrato : implementa
   Main ..> IContrato : usa
   Main ..> Ext : <protocolo>
   @enduml
