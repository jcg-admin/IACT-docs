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

