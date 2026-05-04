.. _uc-auth-03-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_AUTH_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "reset_password" as ADMIN
 actor "User afectado" as USER <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Auth" {
   usecase "UC_AUTH_03\nRecuperar Contrasena" as UC03
   usecase "Generar password\ntemporal" as GEN
   usecase "Cerrar Sessions\ndel User" as CSE
   usecase "Notificar via\nInternalMailbox" as NOT
   usecase "Emitir AuditEvent\nPASSWORD_RESET" as EMI
 }

 ADMIN --> UC03
 UC03 ..> GEN : <<include>>
 UC03 ..> CSE : <<include>>
 UC03 ..> NOT : <<include>>
 UC03 ..> EMI : <<include>>
 NOT --> USER : InternalMessage
 Sistema --> EMI
 EMI --> view_audit_log : (consume\nUC_AUD_*)

 note bottom of NOT
   CNST-001 prohibe email/SMTP
   CNST-002 InternalMailbox obligatorio
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_AUTH_03 — flujo principal

 @startuml

 actor Admin as Admin
 participant "Frontend" as Frontend
 participant "ResetPasswordView" as Resetpasswordview
 participant "AuthService" as Authservice
 participant "PasswordGenerator" as Passwordgenerator
 database "Base de Datos" as BaseDeDatos

 Admin -> Frontend: Click "Resetear contrasena"
 Frontend -> Frontend: Modal de confirmacion
 Admin -> Frontend: Confirmar
 Frontend -> Resetpasswordview: POST /api/users/{id}/reset-password/

 Resetpasswordview -> Resetpasswordview: Validar JWT (CNST-009)
 Resetpasswordview -> Resetpasswordview: Verificar funcion\nreset_password (AGR-006)
 alt Sin permiso
   Resetpasswordview --> Frontend: 403 FORBIDDEN
 else Con permiso
   Resetpasswordview -> Authservice: reset_password(target_id, admin)

   Authservice -> BaseDeDatos: SELECT User WHERE id=target_id
   BaseDeDatos --> Authservice: user
   Authservice -> Authservice: Validar (no auto-reset, no eliminado)

   Authservice -> Passwordgenerator: generate(length=12)
   Passwordgenerator --> Authservice: temp_password
   Authservice -> Authservice: generarHash(temp_password)

   group Transaccion atomica
     Authservice -> BaseDeDatos: UPDATE user SET\n  password_hash=?,\n  first_login=true,\n  password_changed_at=NOW()
     Authservice -> BaseDeDatos: UPDATE session SET\n  state='CLOSED',\n  close_reason='PASSWORD_RESET'\n  WHERE user_id=? AND state='ACTIVE'
     Authservice -> BaseDeDatos: INSERT BlacklistedToken (N tokens)
     Authservice -> BaseDeDatos: INSERT InternalMessage\n  (recipient=user, body=temp_pwd)
     Authservice -> BaseDeDatos: INSERT AuditEvent\n  (PASSWORD_RESET)
   end

   Authservice --> Resetpasswordview: success (sin temp_password)
   Resetpasswordview --> Frontend: 200 OK
   Frontend --> Admin: "Contrasena reseteada. Notificacion en buzon."
 end

 @enduml

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
   :UPDATE User (password_hash, first_login=true);
   :UPDATE Session (CLOSED, PASSWORD_RESET);
   :INSERT BlacklistedToken;
   :INSERT InternalMessage (CNST-001+002);
   :INSERT AuditEvent PASSWORD_RESET (CNST-025);
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

8.4 Diagrama de estados — User.first_login
==========================================

.. uml::
 :caption: Estado first_login del User

 @startuml

 [*] --> first_login_true : UC_USR_01\n(creacion)

 first_login_true --> first_login_true : UC_AUTH_03\n(reset por admin)
 first_login_true --> first_login_false : UC_AUTH_04\n(cambio voluntario\npost first login)

 first_login_false --> first_login_true : UC_AUTH_03\n(reset)

 note right of first_login_true
   UC_AUTH_01 detecta first_login=true
   y dispara FA-01 → forzar UC_AUTH_04
 end note

 @enduml
