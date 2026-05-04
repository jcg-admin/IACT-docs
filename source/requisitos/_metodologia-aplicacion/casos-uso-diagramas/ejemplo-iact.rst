Ejemplo IACT
~~~~~~~~~~~~

.. uml::

   @startuml
   title IACT — dependency entre UCs (snapshot)

   left to right direction

   actor Supervisor
   actor "Operador ETL" as OETL

   rectangle IACT {
     usecase "UC_PIP_01\nCarga ETL" as PIP01
     usecase "UC_RPT_07\nReporte programado" as RPT07
     usecase "UC_AUTH_01\nLogin" as AUTH01
     usecase "UC_AUD_03\nConsultar audit" as AUD03
   }

   OETL --> PIP01
   Supervisor --> RPT07
   Supervisor --> AUD03

   RPT07 ..> PIP01 : depende de
   AUD03 ..> AUTH01 : depende de
   @enduml

Lectura del diagrama:

- Las flechas continuas representan asociación
  actor → UC.
- Las flechas punteadas (``..>``) sin
  estereotipo representan dependencia entre UCs.
- ``UC_AUD_03 ..> UC_AUTH_01`` se lee:
  "consultar audit depende de login".
