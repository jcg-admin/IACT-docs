8.4 Clases
==========

.. uml::

 @startuml
 class SupervisionETLService
 class ETLEjecucionRepo
 class ResumenSaludBuilder
 SupervisionETLService --> ETLEjecucionRepo
 SupervisionETLService --> ResumenSaludBuilder
 @enduml
