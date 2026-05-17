Crecimiento del modelo a partir de la primera relación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una vez documentada la primera relación, el modelo crece
agregando entidades vecinas y sus relaciones — siempre
una línea por relación:

.. uml::

   @startuml
   class Call
   class Segment
   class ETLExecution
   class Report
   class User

   Call "1..*" -- "1" Segment : belongs to
   ETLExecution "1" -- "*" Call : loads
   Report "*" -- "*" Call : aggregates
   User "*" -- "*" Report : queries
   @enduml

En cinco líneas, el modelo embrionario ya captura el
flujo central de IACT: el supervisor consulta reportes
que agregan llamadas que pertenecen a segmentos y se
cargaron por ejecuciones ETL.
