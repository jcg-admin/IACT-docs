.. _uc-alr-03-parte-08-diagrama-estados-transicion:

8.3 Diagrama de estados — Transicion firing → acknowledged
============================================================

.. uml::
 :caption: UC_ALR_03 — transicion del estado de Alert.

 @startuml

 [*] --> firing
 firing --> acknowledged : acknowledge_alert\n(UC_ALR_03)
 acknowledged --> resolved : metric vuelve\na normal
 firing --> resolved : metric vuelve\na normal
 resolved --> closed
 closed --> [*]

 note right of acknowledged
   ack_by, ack_at registrados.
   Notificaciones pendientes
   suprimidas.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert`
   (estado completo del Alert).
 - :doc:`/requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-estados-alerta`
   (vista completa del lifecycle).
