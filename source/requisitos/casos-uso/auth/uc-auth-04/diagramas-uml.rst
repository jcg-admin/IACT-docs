.. _uc-auth-04-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_04 — actores y casos asociados

 @startuml

 left to right direction

 actor "User\nautenticado" as USER
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_04\nCambiar Contrasena" as UC04
   usecase "Validar password\nactual" as VAL
   usecase "Validar complejidad" as COMP
   usecase "Verificar historial\n(no reuso)" as HIST
   usecase "Cerrar otras\nSessions" as CSE
   usecase "Emitir AuditEvent\nPASSWORD_CHANGED" as EMI
 }

 USER --> UC04
 UC04 ..> VAL : <<include>>
 UC04 ..> COMP : <<include>>
 UC04 ..> HIST : <<include>>
 UC04 ..> CSE : <<include>>
 UC04 ..> EMI : <<include>>
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of HIST
   N=5 ultimas hashes (BR-AUTH-32)
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_AUTH_04 — flujo principal

 @startuml

 actor User as User
 participant "Frontend" as Frontend
 participant "ChangePasswordView" as Changepasswordview
 participant "AuthService" as Authservice
 participant "PolicyValidator" as Policyvalidator
 database "Base de Datos" as BaseDeDatos

 Usuario -> Frontend: Form (current, new, confirm)
 Frontend -> Frontend: Client-side basic validation
 Frontend -> Changepasswordview: POST /api/auth/change-password/
 Changepasswordview -> Changepasswordview: Validar JWT (CNST-009)
 Changepasswordview -> Authservice: change_password(user, current, new)

 Authservice -> BaseDeDatos: SELECT User FOR UPDATE
 BaseDeDatos --> Authservice: user
 Authservice -> Authservice: verificarHash(current, user.hash)
 alt Password actual incorrecto
   Authservice --> Changepasswordview: WrongCurrentPassword
   Changepasswordview --> Frontend: 400 WRONG_CURRENT_PASSWORD
 else OK
   Authservice -> Policyvalidator: validate(new)
   alt Falla politica
     Policyvalidator --> Authservice: violations
     Authservice --> Changepasswordview: WeakPassword
     Changepasswordview --> Frontend: 400 WEAK_PASSWORD
   else OK
     Authservice -> BaseDeDatos: SELECT history WHERE user=?\n  ORDER BY changed_at DESC LIMIT 5
     BaseDeDatos --> Authservice: hashes[5]
     Authservice -> Authservice: for h in hashes:\n  if verificarHash(new, h): reused
     alt Reuso
       Authservice --> Changepasswordview: PasswordReused
       Changepasswordview --> Frontend: 400 PASSWORD_REUSED
     else OK
       Authservice -> Authservice: generarHash(new)

       group Transaccion atomica
         Authservice -> BaseDeDatos: UPDATE user (hash, first_login=false,\n  password_changed_at=NOW())
         Authservice -> BaseDeDatos: INSERT password_history
         Authservice -> BaseDeDatos: UPDATE other sessions (CLOSED)
         Authservice -> BaseDeDatos: INSERT BlacklistedToken
         Authservice -> BaseDeDatos: INSERT AuditEvent PASSWORD_CHANGED
       end

       Authservice --> Changepasswordview: success
       Changepasswordview --> Frontend: 200 OK
       Frontend --> Usuario: "Contrasena actualizada"
     end
   end
 end

 @enduml

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
   :UPDATE User (hash, first_login=false);
   :INSERT PasswordHistory;
   if (Setting cierra otras?) then (si)
     :UPDATE Sessions != current → CLOSED;
     :INSERT BlacklistedToken;
   else (no)
   endif
   :INSERT AuditEvent PASSWORD_CHANGED;
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

8.4 Diagrama de estados — User.first_login + scope
==================================================

.. uml::
 :caption: Transiciones de scope post UC_AUTH_04

 @startuml

 state "Sesion scope reducido" as REDUCED
 state "Sesion scope pleno" as FULL

 [*] --> REDUCED : UC_AUTH_01 + FA-01\n(first_login=true)

 REDUCED --> FULL : UC_AUTH_04 OK\n(first_login=false)

 FULL --> FULL : UC_AUTH_04 voluntario

 FULL --> REDUCED : UC_AUTH_03\n(admin reset)\nuser proximo login

 @enduml
