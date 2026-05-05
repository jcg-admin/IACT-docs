3. Diagrama de casos de uso
---------------------------

**Propósito:** qué hace el sistema desde el punto de vista del
usuario. Actor + caso de uso + relaciones.

**Cuándo usarlo:** cuando hablas con usuarios/clientes sobre
**qué** debe hacer el sistema (requisitos de negocio).

  Un caso de uso es una **descripción de acciones desde el
  punto de vista del usuario**, no de la implementación
  técnica.

**Lección completa:**
:doc:`/base-cognitiva/_uml/uml-06-introduccion-casos-uso/index`,
:doc:`/base-cognitiva/_uml/uml-07-diagramas-casos-uso/index`.

.. uml::

   @startuml

   left to right direction
   actor Usuario
   rectangle "Lavadora" {
     usecase "Lavar ropa" as UC
   }
   Usuario --> UC
   @enduml
