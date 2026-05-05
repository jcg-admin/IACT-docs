8.3 Diagrama de actividad (cierre masivo 3.C)
=============================================

.. uml::
 :caption: UC_AUTH_05 sub-flujo 3.C — actividad

 @startuml

 start

 :Admin abre detalle del User;
 :Click "Cerrar todas las sesiones";
 :Modal robusto con count;

 if (Admin confirma?) then (no)
   :Cancelar; stop
 else (si)
 endif

 :POST /api/users/{id}/close-all-sessions/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene close_user_session?) then (no)
   :403; :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404; stop
 else (si)
 endif

 if (target_user == admin?) then (si)
   if (Setting permite?) then (no)
     :400 SELF_BULK_CLOSE_FORBIDDEN; stop
   else (si)
   endif
 else (no)
 endif

 :consultar Sessions ACTIVE WHERE user=target;

 if (count == 0?) then (si)
   :Audit BULK_SESSION_CLOSE_NOOP;
   :200 OK count=0;
   stop
 else (no)
 endif

 partition "Transaccion atomica" {
   :actualizar Sessions → CLOSED;
   :registrar BlacklistedToken (N);
   :registrar N AuditEvent SESSION_CLOSED;
   :registrar 1 AuditEvent BULK_SESSION_CLOSE;
   if (Setting notify) then (si)
     :registrar InternalMessage al User;
   else (no)
   endif
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK;
   :500/503;
   stop
 else (si)
 endif

 :200 OK con count;
 :Frontend toast con count;

 stop

 @enduml

