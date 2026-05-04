Una nueva visita a la máquina de gaseosas
=========================================

El caso de uso *"Comprar gaseosa"* se encuentra dentro del
sistema junto con *"Reabastecer"* y *"Recolectar dinero"*. Los
actores son el ``Cliente``, el ``Representante del proveedor`` y
el ``Recolector``.

.. uml::

   @startuml

   left to right direction
   actor Cliente
   actor "Representante\ndel proveedor" as Proveedor
   actor Recolector

   rectangle "Máquina de Gaseosas" {
     usecase "Comprar gaseosa"      as UC1
     usecase "Reabastecer"          as UC2
     usecase "Recolectar el dinero" as UC3
   }
   Cliente    --> UC1
   Proveedor  --> UC2
   Recolector --> UC3
   @enduml

----
