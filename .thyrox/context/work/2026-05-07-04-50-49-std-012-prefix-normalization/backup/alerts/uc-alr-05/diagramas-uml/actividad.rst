8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST sub;
 :JWT + RBAC (own o admin);
 :Validar type + scope;
 if (Cross-segmento?) then (si)
   :400; stop
 endif
 if (Duplicada?) then (si)
   :409; stop
 endif
 :registrar;
 :Audit;
 :201;
 stop
 @enduml

