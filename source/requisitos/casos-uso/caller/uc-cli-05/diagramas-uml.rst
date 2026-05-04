.. _uc-cli-05-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "Caller" as Caller
 rectangle "MOD_Caller" {
   usecase "UC_CLI_05\nCSAT" as UcCli05
 }
 Caller --> UcCli05
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :Agente cuelga;
 if (Survey ofrecido?) then (no)
   :Hangup; stop
 endif
 :Reproducir prompt;
 repeat
   :Pregunta;
   :Esperar DTMF;
   if (Respuesta o skip?) then (skip)
     :Marcar skip;
   endif
 repeat while (mas preguntas)
 :INSERT SurveyResponse;
 :Mensaje agradecimiento;
 :Hangup;
 stop
 @enduml

8.3 Componentes
===============

.. uml::

 @startuml
 component "SurveyRunner" as Surveyrunner
 component "DTMFCollector" as Dtmfcollector
 component "ResponseRepo" as Responserepo
 Surveyrunner --> Dtmfcollector
 Surveyrunner --> Responserepo
 @enduml

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
 Survey -> Repo: INSERT
 Survey -> Caller: gracias + hangup
 @enduml
