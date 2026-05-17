.. _uc-alr-02-parte-08-diagrama-estados-alerta:

8.3 Diagrama de estados — Alert
================================

.. uml::
 :caption: Alert — ciclo de vida desde firing hasta closed.

 @startuml

 [*] --> firing : EvaluatorReloader dispara

 firing --> acknowledged : acknowledge_alert\n(UC_ALR_03)
 firing --> resolved : metric vuelve a normal
 acknowledged --> resolved : metric vuelve a normal
 acknowledged --> closed : forced close (manual)
 resolved --> closed : auto cleanup (TTL)
 closed --> [*]

 note right of firing
   Estado inicial al disparar
   la alerta. Visible en
   listado activo.
 end note

 note right of acknowledged
   Operador reconocio que esta
   atendiendo. Visible en listado
   con flag acknowledged.
 end note

 note right of resolved
   Metric volvio a estar dentro
   de los umbrales. Visible
   solo si filter incluye
   resolved.
 end note

 note right of closed
   Estado terminal. Movido a
   historico para reportes.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert`.
 - :doc:`/requisitos/casos-uso/alerts/uc-alr-03/index`
   (UC_ALR_03 acknowledge).
