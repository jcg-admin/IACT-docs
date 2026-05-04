8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_07 — algoritmo

 @startuml

 start

 :Recibir (user_id, function_code);

 if (Cache hit?) then (si)
   :return cached;
   stop
 else (no)
 endif

 if (Revocacion excepcional ACTIVA?) then (si)
   :origin=REVOKED_EXCEPTIONAL
    allowed=false;
 else (no)
   if (Concesion excepcional ACTIVA?) then (si)
     :origin=GRANTED_EXCEPTIONAL
      allowed=true;
   else (no)
     if (AGR ACTIVE con funcion?) then (si)
       :origin=GRANTED_BY_AGR
        allowed=true;
     else (no)
       :origin=DENIED_NO_GRANT
        allowed=false;
     endif
   endif
 endif

 :Cache write con TTL ajustado;
 :return result;

 stop

 @enduml

