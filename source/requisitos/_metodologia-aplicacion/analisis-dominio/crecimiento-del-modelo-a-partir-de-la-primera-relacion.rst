Crecimiento del modelo a partir de la primera relación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una vez documentada la primera relación, el modelo crece
agregando entidades vecinas y sus relaciones — siempre
una línea por relación:

.. uml::

   @startuml
   class Llamada
   class Segmento
   class EjecucionETL
   class Reporte
   class Usuario

   Llamada "1..*" -- "1" Segmento : pertenece a
   EjecucionETL "1" -- "*" Llamada : carga
   Reporte "*" -- "*" Llamada : agrega
   Usuario "*" -- "*" Reporte : consulta
   @enduml

En cinco líneas, el modelo embrionario ya captura el
flujo central de IACT: el supervisor consulta reportes
que agregan llamadas que pertenecen a segmentos y se
cargaron por ejecuciones ETL.
