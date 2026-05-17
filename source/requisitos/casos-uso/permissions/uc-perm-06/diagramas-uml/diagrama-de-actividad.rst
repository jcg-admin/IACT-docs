8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_06 — actividad

 @startuml

 start

 :POST functions/ con add + remove + reason;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (assign_functions_to_group?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (AGR existe + ACTIVE + custom?) then (no)
   :404 / 400; stop
 else (si)
 endif

 if (Functions validas?) then (no)
   :400; stop
 else (si)
 endif

 if (change_reason ≥ 20?) then (no)
   :400 VALIDATION_ERROR; stop
 else (si)
 endif

 :Filtrar idempotencia;
 :Calcular cascade_affected_user_count;
 :Validar separacion para cada User con AGR
  con set efectivo post-cambio;

 if (Cascade separacion violation?) then (si)
   if (politica strict?) then (si)
     :409 CASCADE_SEPARATION_VIOLATION;
     :Audit COMPOSITION_FAILED;
     stop
   else (permissive)
     :continuar con warning;
   endif
 else (no)
 endif

 :Iniciar transaccion atomica;
 :registrar AccessGroupFunction (add);
 :eliminar AccessGroupFunction (remove);
 :registrar AuditEvent
  COMPOSITION_CHANGED;
 :Commit;

 :PermissionCache.invalidate
  para Users con AGR (post-COMMIT);
 :200 OK con resumen + cascade;

 stop

 @enduml

