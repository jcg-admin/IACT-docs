8.3 Estado
==========

.. uml::

 @startuml
 [*] --> waiting
 waiting --> served : agente asigna
 waiting --> abandoned : caller cuelga
 waiting --> callback_offered : > X min
 callback_offered --> waiting : declina
 callback_offered --> callback_scheduled : acepta
 served --> [*]
 abandoned --> [*]
 callback_scheduled --> [*]
 @enduml

