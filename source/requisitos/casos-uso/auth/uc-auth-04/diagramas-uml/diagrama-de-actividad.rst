8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_AUTH_04 — actividad

 @startuml

 start

 :User envia (current, new, confirm);

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 if (new == confirmation?) then (no)
   :400 MISMATCH; stop
 else (si)
 endif

 if (verificarHash(current, user.hash)?) then (no)
   :delay defensivo;
   :incrementar contador;
   if (5+ fallos en 5min?) then (si)
     :429 TOO_MANY_ATTEMPTS;
     :Audit SUSPICIOUS;
     stop
   else (no)
     :400 WRONG_CURRENT;
     stop
   endif
 else (si)
 endif

 if (Politica OK?) then (no)
   :400 WEAK_PASSWORD; stop
 else (si)
 endif

 if (Igual a actual?) then (si)
   :400 SAME_AS_CURRENT; stop
 else (no)
 endif

 if (En history N=5?) then (si)
   :400 PASSWORD_REUSED; stop
 else (no)
 endif

 :generarHash(new);

 partition "Transaccion atomica" {
   :actualizar User (hash, first_login=false);
   :registrar PasswordHistory;
   if (Setting cierra otras?) then (si)
     :actualizar Sessions != current → CLOSED;
     :registrar BlacklistedToken;
   else (no)
   endif
   :registrar AuditEvent PASSWORD_CHANGED;
 }

 if (Transaccion OK?) then (no)
   :ROLLBACK; :500/503;
   stop
 else (si)
 endif

 :200 OK;
 :Frontend toast + nav;

 stop

 @enduml

