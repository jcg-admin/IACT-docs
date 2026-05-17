8. Diagrama de componentes
--------------------------

**Propósito:** bloques de software reutilizables y sus
dependencias. Componentes + interfaces + dependencias.

**Cuándo usarlo:** cuando hablas de**arquitectura de
software** (qué módulos/componentes existen y cómo dependen
unos de otros).

**Lección completa:** :doc:`/base-cognitiva/_uml/uml-12-diagramas-componentes/index`.

.. uml::

   @startuml

   component "Interfaz de Usuario" as UI
   component "Controlador Principal" as Ctrl
   component "Motor de Lavado" as Motor

   UI ..> Ctrl : <<usa>>
   Ctrl ..> Motor : <<usa>>
   @enduml
