8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST break;
 :Validar quota;
 if (Excedida?) then (si)
   :409; stop
 endif
 :Delegar UC_OPR_01;
 :Iniciar timer;
 :200;
 stop
 @enduml

