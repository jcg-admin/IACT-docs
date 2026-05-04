8.4 Diagrama de actividad
=========================

.. uml::
 :caption: UC_USR_02 — actividad combinada

 @startuml

 start

 if (Sub-flujo?) then (listar)
   :GET /api/users/?filtros;
   if (JWT valido?) then (no)
     :401; stop
   else (si)
   endif
   if (list_users?) then (no)
     :403; :Audit UNAUTHORIZED;
     stop
   else (si)
   endif
   if (Filtros validos?) then (no)
     :400 BAD_FILTER; stop
   else (si)
   endif
   :Query con paginacion;
   :Restringir campos PII;
   if (filter user_id?) then (si)
     :Audit USERS_VIEWED_FOR_USER;
   else (no)
   endif
   :200 OK lista;
   stop
 else (detalle)
   :GET /api/users/{id}/;
   if (JWT valido?) then (no)
     :401; stop
   else (si)
   endif
   if (view_users?) then (no)
     :403; :Audit UNAUTHORIZED;
     stop
   else (si)
   endif
   if (User existe?) then (no)
     :404; stop
   else (si)
   endif
   :Cargar Assignments + AGRs;
   :Audit USER_DETAIL_VIEWED;
   :200 OK detalle;
   stop
 endif

 @enduml
