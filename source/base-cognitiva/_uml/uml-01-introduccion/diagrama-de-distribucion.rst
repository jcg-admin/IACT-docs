Diagrama de distribución
========================

Muestra la **arquitectura física** de un sistema informático;
puede representar los equipos y dispositivos, mostrar sus
interconexiones y el software que se encontrará en cada máquina.

Cada computadora está representada por un cubo y las
interacciones entre las computadoras están representadas por
líneas que conectan a los cubos.

.. uml::

   @startuml

   node "Servidor de Aplicación" as App {
     component [Backend API]
   }
   node "Servidor de BD" as DB {
     database "PostgreSQL"
   }
   node "Cliente" as Web {
     component [Navegador Web]
   }
   Web --> App : HTTPS
   App --> DB  : SQL
   @enduml

----
