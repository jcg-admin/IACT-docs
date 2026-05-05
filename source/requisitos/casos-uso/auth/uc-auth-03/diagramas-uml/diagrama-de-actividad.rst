8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_AUTH_03 — actividad

 @startuml

 start

 :Admin selecciona User;
 :Admin click "Resetear contrasena";
 :Modal de confirmacion;

 if (Admin confirma?) then (no)
   :Cancelar; stop
 else (si)
 endif

 :POST /api/users/{id}/reset-password/;

 if (JWT valido?) then (no)
   :401 INVALID_TOKEN; stop
 else (si)
 endif

 if (Tiene reset_password?) then (no)
   :403 FORBIDDEN;
   :Audit UNAUTHORIZED_ACCESS_ATTEMPT;
   stop
 else (si)
 endif

 if (User existe?) then (no)
   :404 USER_NOT_FOUND; stop
 else (si)
 endif

 if (Es auto-reset?) then (si)
   :400 SELF_RESET_FORBIDDEN; stop
 else (no)
 endif

 if (User ELIMINATED?) then (si)
   :400 USER_ELIMINATED; stop
 else (no)
 endif

 :Generar password temporal (12+ chars);
 :generarHash (costo de hash configurado);

 partition "Transaccion atomica" {
   :actualizar User (password_hash, first_login=true);
   :actualizar Session (CLOSED, PASSWORD_RESET);
   :registrar BlacklistedToken;
   :registrar InternalMessage (CNST-001+002);
   :registrar AuditEvent PASSWORD_RESET (CNST-025);
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK;
   :500/503;
   stop
 else (si)
 endif

 :200 OK (sin temp_password en response);
 :Frontend muestra confirmacion (sin password);

 stop

 @enduml

