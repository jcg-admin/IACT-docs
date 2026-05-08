.. _uc-pip-03-parte-08-diagrama-estados-frescura-datos:

8.3 Diagrama de estados — Frescura de datos
=============================================

.. uml::
 :caption: DisponibilidadDatos — estado segun edad del ultimo ETL exitoso.

 @startuml

 [*] --> fresco : ETL exitoso reciente (<12h)
 fresco --> degradado : >12h sin actualizacion
 degradado --> vencido : >24h sin actualizacion
 vencido --> fresco : ETL exitoso
 degradado --> fresco : ETL exitoso

 note right of fresco
   Datos confiables, sin alerta.
 end note

 note right of degradado
   Banner de aviso al user.
   Disparar alerta si SLA lo
   requiere.
 end note

 note right of vencido
   Bloqueo de reportes que
   dependen de datos frescos.
   Alerta critica al admin.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`.
