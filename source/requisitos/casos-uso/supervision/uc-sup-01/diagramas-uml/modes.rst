8.3 Modes
=========

.. uml::

 @startuml
 [*] --> silent
 silent --> whisper : switch
 whisper --> silent : switch
 silent --> stopped : stop
 whisper --> stopped : stop
 stopped --> [*]
 @enduml

