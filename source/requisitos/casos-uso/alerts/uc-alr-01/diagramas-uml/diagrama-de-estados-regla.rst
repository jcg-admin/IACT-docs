.. _uc-alr-01-parte-08-diagrama-estados-regla:

8.3 Diagrama de estados — AlertRule
=====================================

.. uml::
 :caption: AlertRule — ciclo de vida.

 @startuml

 [*] --> active : crear (UC_ALR_01)
 active --> paused : pause
 paused --> active : resume
 active --> deleted : delete (BR-009 baja logica)
 paused --> deleted : delete (BR-009 baja logica)

 note right of active
   La regla es evaluada por el
   EvaluatorReloader y dispara
   alertas si la condicion se
   cumple en la ventana definida.
 end note

 note right of paused
   Regla preservada pero no
   evaluada. Util para
   troubleshooting o pausas
   programadas.
 end note

 note right of deleted
   Soft delete (BR-009).
   La regla no se borra fisicamente.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`.
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`.
