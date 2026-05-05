8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_05 — actividad CRUD

 @startuml

 start

 :Operacion CRUD recibida;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (create_function_group?) then (no)
   :403; :Audit UNAUTHORIZED;
   stop
 else (si)
 endif

 if (Operacion?) then (CREATE)
   if (code formato + unique?) then (no)
     :400 / 409; stop
   else (si)
   endif
   :registrar AccessGroup;
   :Audit ACCESS_GROUP_CREATED;
 else (PATCH / DELETE)
   if (AGR existe + ACTIVE + custom?) then (no)
     :404 / 400; stop
   else (si)
   endif
   if (PATCH?) then (si)
     if (incluye code?) then (si)
       :400 CODE_IMMUTABLE; stop
     else (no)
     endif
     :actualizar atributos descriptivos;
     :Audit ACCESS_GROUP_MODIFIED;
   else (DELETE)
     if (retire_reason ≥ 20?) then (no)
       :400 VALIDATION; stop
     else (si)
     endif
     :Calcular users_with_agr_count;
     if (count > 0 y politica strict?) then (si)
       :409 RETIRE_HAS_USERS; stop
     else (no)
     endif
     :actualizar state=RETIRED;
     :Audit ACCESS_GROUP_RETIRED;
   endif
 endif

 :Cache invalidate post-COMMIT;
 :200 / 201;

 stop

 @enduml

