Comprensión de los usuarios
---------------------------

Se tiene que tener atención a los usuarios y entender los tipos
de funcionalidad. Esto se realiza mediante **entrevistas** —
nada puede sustituir a las entrevistas.

Un grupo de usuarios serán **consultores**, otros podrían ser
**oficinistas**. Entre otros usuarios en potencia se encontrarán
funcionarios corporativos, vendedores, administradores de red,
administradores de oficina y administradores de proyectos.

Sería conveniente mostrar a los usuarios en una **jerarquía de
generalización**.

.. uml::

   @startuml

   actor Empleado
   actor Consultor
   actor Oficinista
   actor "Funcionario\ncorporativo" as FC
   actor Vendedor
   actor "Administrador\nde red" as AR
   actor "Administrador\nde oficina" as AO
   actor "Administrador\nde proyectos" as AP

   Empleado <|-- Consultor
   Empleado <|-- Oficinista
   Empleado <|-- FC
   Empleado <|-- Vendedor
   Empleado <|-- AR
   Empleado <|-- AO
   Empleado <|-- AP
   @enduml
