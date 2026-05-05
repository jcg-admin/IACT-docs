3. Ejemplo visual — Máquina de gaseosas (referencia genérica)
=============================================================

Diagrama clásico de Schmuller que sirve de base conceptual:

.. uml::

   @startuml

   left to right direction
   actor Cliente
   actor "Representante\ndel proveedor" as Proveedor
   actor Recolector
   actor Tiempo

   rectangle "Máquina de Gaseosas" {
     usecase "Comprar gaseosa"      as UC1
     usecase "Reabastecer"          as UC2
     usecase "Recolectar el dinero" as UC3
   }

   Cliente    --> UC1
   Proveedor  --> UC2
   Recolector --> UC3
   Tiempo     --> UC2
   Tiempo     --> UC3
   @enduml
