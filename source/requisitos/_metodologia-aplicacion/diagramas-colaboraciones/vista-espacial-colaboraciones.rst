11.2 Vista espacial — colaboraciones
------------------------------------

  *Pregunta:* ¿cómo se conectan?
  *Respuesta:* estructura de relaciones.

.. uml::

   @startuml
   allowmixing

   actor Operador
   object ":Frontend"   as Frontend
   object ":Backend"    as Backend
   object ":SecRules"   as SecRules
   object ":BDAnalytics" as BDAnalytics
   object ":AuditLog"   as AuditLog

   Operador -> Frontend  : "1"
   Frontend        -> Backend  : "2"
   Backend        -> SecRules : "3"
   Backend        -> BDAnalytics : "4"
   Backend        -> AuditLog : "5"
   @enduml
