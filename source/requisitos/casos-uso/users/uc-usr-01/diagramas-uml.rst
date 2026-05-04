.. _uc-usr-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_USR_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "create_users" as ADMIN
 actor "Nuevo User" as USER <<beneficiario>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "Sistema" as Sistema <<sistema>>

 rectangle "MOD_Users" {
   usecase "UC_USR_01\nCrear Usuario" as UC01
   usecase "Generar username\n(CNST-029)" as GEN
   usecase "Generar password\ntemporal" as PWD
   usecase "Asignar AGR\nopcional" as AGR
   usecase "Notificar via\nInternalMailbox" as NOT
   usecase "AuditEvent\nUSER_CREATED" as EMI
 }

 ADMIN --> UC01
 UC01 ..> GEN : <<include>>
 UC01 ..> PWD : <<include>>
 UC01 ..> AGR : <<extend>>
 UC01 ..> NOT : <<include>>
 UC01 ..> EMI : <<include>>
 NOT --> USER : InternalMessage
 Sistema --> EMI
 EMI --> view_audit_log

 note bottom of NOT
   CNST-001 prohibe email/SMTP
   CNST-002 InternalMailbox obligatorio
 end note

 @enduml

8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_USR_01 — flujo principal

 @startuml

 actor Admin as Admin
 participant "Frontend" as Frontend
 participant "CreateUserView" as Createuserview
 participant "UserService" as Userservice
 participant "UsernameGenerator" as Usernamegenerator
 participant "PasswordGenerator" as Passwordgenerator
 database "Base de Datos" as BaseDeDatos

 Admin -> Frontend: Form (first, last, email, agr_id?)
 Frontend -> Createuserview: POST /api/users/

 Createuserview -> Createuserview: Validar JWT (CNST-009)
 Createuserview -> Createuserview: Verificar create_users (AGR-006)
 alt Sin permiso
   Createuserview --> Frontend: 403 FORBIDDEN
 else
   Createuserview -> Userservice: create_user(data, admin)

   Userservice -> BaseDeDatos: SELECT email
   alt Email existe
     Userservice --> Createuserview: EmailExists
     Createuserview --> Frontend: 409 EMAIL_EXISTS
   else No existe
     Userservice -> Usernamegenerator: generate(first, last)
     Usernamegenerator -> BaseDeDatos: SELECT COUNT username LIKE base%
     Usernamegenerator --> Userservice: ana.gomez.0001
     Userservice -> Passwordgenerator: generate(length=12)
     Passwordgenerator --> Userservice: temp_password
     Userservice -> Userservice: generarHash(temp)

     group Transaccion atomica
       Userservice -> BaseDeDatos: INSERT User\n  (username, email, password_hash,\n   first_login=true, ...)
       opt access_group_id provided
         Userservice -> BaseDeDatos: INSERT Assignment\n  (user, agr, granted_by=admin)
       end
       Userservice -> BaseDeDatos: INSERT InternalMessage\n  (recipient=user, body=temp_password)
       Userservice -> BaseDeDatos: INSERT AuditEvent\n  USER_CREATED
     end

     Userservice --> Createuserview: {user_id, username}
     Createuserview --> Frontend: 201 Created (sin password)
     Frontend --> Admin: Toast "Creado: ana.gomez.0001"
   end
 end

 @enduml

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
 :bcrypt.hashpw cost 12;

 partition "Transaccion atomica" {
   :INSERT User (first_login=true);
   if (AGR provisto?) then (si)
     :INSERT Assignment;
   else (no)
   endif
   :INSERT InternalMessage (CNST-001+002);
   :INSERT AuditEvent USER_CREATED (CNST-025);
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

8.4 Diagrama de estados — User.first_login
==========================================

.. uml::
 :caption: Estados first_login del nuevo User

 @startuml

 [*] --> first_login_true : UC_USR_01 (creacion)

 first_login_true --> first_login_true : UC_AUTH_03\n(admin reset)
 first_login_true --> first_login_false : UC_AUTH_04\n(cambio post first login)

 first_login_false --> first_login_true : UC_AUTH_03

 note right of first_login_true
   UC_AUTH_01 detecta first_login=true
   y dispara FA-01 → forzar UC_AUTH_04
 end note

 @enduml
