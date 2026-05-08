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
 :registrar SurveyResponse;
 :Mensaje agradecimiento;
 :Hangup;
 stop
 @enduml

