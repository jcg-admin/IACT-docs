8.3 Estado de la alerta
=======================

.. uml::

 @startuml
 [*] --> firing : evaluator dispara
 firing --> acknowledged : UC_ALR_03
 firing --> resolved : metric vuelve normal
 acknowledged --> resolved : metric normal
 acknowledged --> closed : forced close
 resolved --> closed : auto cleanup
 closed --> [*]
 @enduml

