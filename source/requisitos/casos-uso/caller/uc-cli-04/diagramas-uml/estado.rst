8.3 Estado
==========

.. uml::

 @startuml
 [*] --> pending
 pending --> in_progress : agente toma
 in_progress --> done : llamada exitosa
 in_progress --> expired : ventana cerro
 pending --> expired : sin tomar
 done --> [*]
 expired --> [*]
 @enduml

