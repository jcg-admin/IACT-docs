8.4 Secuencia
=============

.. uml::

 @startuml
 actor "Caller" as Caller
 participant "Survey" as Survey
 database "Repo" as Repo
 Survey -> Caller: prompt
 Caller -> Survey: DTMF
 Survey -> Caller: pregunta 2
 Caller -> Survey: DTMF
 Survey -> Repo: registrar
 Survey -> Caller: gracias + hangup
 @enduml
