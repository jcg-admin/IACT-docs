11.10 Plantilla — vista de despliegue IACT
------------------------------------------

.. uml::

   @startuml
   title Deployment — <ambito>

   actor "<Actor>" as Actor

   node "<device cliente>" as Cliente {
     artifact "<bundle / cliente>"
   }

   node "vm-iact" as VmIact {
     node "<execution environment>" as ExecutionEnvironment {
       artifact "<artifact 1>"
       artifact "<artifact 2>"
     }
     database "<BD interna>" as BdInterna
   }

   node "<sistema externo>" as Ext

   Actor -- Cliente
   Cliente --> VmIact : <protocolo>
   VmIact --> Ext : <protocolo>
   VmIact ..> Ext : <dependencia opcional>
   @enduml
