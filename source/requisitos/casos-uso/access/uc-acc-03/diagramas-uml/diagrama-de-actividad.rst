8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_ACC_03 — actividad

 @startuml

 start

 :GET /api/users/{id}/effective-permissions/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (tiene view_assignments\no es self-view?) then (no)
   :403;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404; stop
 else (si)
 endif

 :Cargar Assignments directos ACTIVE;
 :Cargar AGR Assignments ACTIVE;
 :Expandir funciones de cada AGR;
 :Cargar ExceptionalPermissions ACTIVE;

 :Consolidar set efectivo
  + metadata origen por funcion;
 :Detectar Assignments con expires_at < marca_tiempo_actual
  (expired_pending_purge);
 :Evaluar SoDRules informativamente
  (sod_violations_detected);

 :Audit EFFECTIVE_PERMISSIONS_VIEWED (P-16);

 :200 OK con vista consolidada;
 :Frontend renderiza tabla con badges;

 stop

 @enduml

