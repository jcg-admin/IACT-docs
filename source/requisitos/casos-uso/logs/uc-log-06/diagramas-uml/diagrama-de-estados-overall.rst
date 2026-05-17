.. _uc-log-06-parte-08-diagrama-estados-overall:

8.3 Diagrama de estados — Overall status
==========================================

.. uml::
 :caption: SystemHealth overall status — transicion entre niveles.

 @startuml

 [*] --> green
 green --> yellow : 1+ servicios degradados
 yellow --> red : 1+ servicios criticos
 red --> yellow : recovery a degradado
 yellow --> green : recovery completo

 note right of green
   Todos los servicios y deps OK.
 end note

 note right of yellow
   Algun servicio o dep
   degradado. Operacion continua
   con observabilidad activa.
 end note

 note right of red
   Servicio o dep critico caido.
   Alertas disparadas. Posible
   degraded mode en el sistema.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/system-health`.
