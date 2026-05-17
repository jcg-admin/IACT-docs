Comprensión del dominio
-----------------------

Para dicha compresión se tiene que empezar con las entrevistas
al cliente; en la entrevista tiene que surgir el diagrama de
clases.

El diagrama de clases podría incluir las siguientes clases:
``Consultor``, ``Cliente``, ``Proyecto``, ``Propuesta``,
``Datos`` e ``Informe``.

.. uml::

   @startuml

   class Consultant
   class Client
   class Project
   class Proposal
   class Data
   class Report

   Consultant "1..*" -- "0..*" Project       : works on
   Client     "1"    -- "0..*" Project       : commissions
   Project    "1"    -- "1..*" Proposal      : produces
   Project    "1"    -- "0..*" Data          : collects
   Project    "1"    -- "1..*" Report        : delivers
   @enduml
