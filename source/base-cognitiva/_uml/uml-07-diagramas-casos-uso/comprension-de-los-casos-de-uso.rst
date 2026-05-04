Comprensión de los casos de uso
-------------------------------

Algunas posibilidades son:

- "Establecer niveles de seguridad"
- "Crear una propuesta"
- "Almacenar una propuesta"
- "Utilizar correo electrónico"
- "Compartir información de la base de datos"
- "Realizar la contabilidad"
- "Conectarse a la LAN desde fuera de ella"
- "Conectarse a Internet"
- "Indizar las propuestas"
- "Utilizar propuestas previas"
- "Compartir impresoras"

Este conjunto de casos de uso constituye los **requerimientos
funcionales** de la LAN.

.. uml::

   @startuml

   left to right direction
   actor Consultor
   actor Oficinista
   actor "Admin\nde red" as AR

   rectangle "LAN — Firma de Consultoría" {
     usecase "Establecer niveles\nde seguridad"      as U1
     usecase "Crear una propuesta"                   as U2
     usecase "Almacenar una propuesta"               as U3
     usecase "Utilizar correo electrónico"           as U4
     usecase "Compartir info\nde base de datos"      as U5
     usecase "Realizar la contabilidad"              as U6
     usecase "Conectarse a la LAN\ndesde fuera"      as U7
     usecase "Conectarse a Internet"                 as U8
     usecase "Indizar las propuestas"                as U9
     usecase "Utilizar propuestas previas"           as U10
     usecase "Compartir impresoras"                  as U11
   }

   Consultor   --> U2
   Consultor   --> U3
   Consultor   --> U4
   Consultor   --> U10
   Oficinista  --> U6
   Oficinista  --> U4
   AR          --> U1
   AR          --> U7
   AR          --> U8
   AR          --> U11
   AR          --> U5
   Consultor   --> U9
   @enduml
