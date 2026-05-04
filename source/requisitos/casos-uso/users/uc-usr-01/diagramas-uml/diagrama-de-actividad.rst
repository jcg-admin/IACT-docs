8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_USR_01 — actividad

 @startuml

 start

 :Admin abre form;
 :Ingresa datos + AGR opcional;
 :POST /api/users/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (Tiene create_users?) then (no)
   :403;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (Datos validos?) then (no)
   :400 VALIDATION_ERROR; stop
 else (si)
 endif

 if (Email unico?) then (no)
   :409 EMAIL_EXISTS; stop
 else (si)
 endif

 if (Setting strict y email externo?) then (si)
   :400 EXTERNAL_EMAIL_FORBIDDEN; stop
 else (no)
 endif

 :Generar username CNST-029;
 :Generar password temporal;
 :generarHash (costo de hash configurado);

 partition "Transaccion atomica" {
   :registrar User (first_login=true);
   if (AGR provisto?) then (si)
     :registrar Assignment;
   else (no)
   endif
   :registrar InternalMessage (CNST-001+002);
   :registrar AuditEvent USER_CREATED (CNST-025);
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK; :500/503;
   stop
 else (si)
 endif

 :201 Created (sin password en response);
 :Frontend toast con username;

 stop

 @enduml

