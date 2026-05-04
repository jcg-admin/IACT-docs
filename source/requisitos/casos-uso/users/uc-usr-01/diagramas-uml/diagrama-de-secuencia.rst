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

   Userservice -> BaseDeDatos: consultar email
   alt Email existe
     Userservice --> Createuserview: EmailExists
     Createuserview --> Frontend: 409 EMAIL_EXISTS
   else No existe
     Userservice -> Usernamegenerator: generate(first, last)
     Usernamegenerator -> BaseDeDatos: consultar COUNT username LIKE base%
     Usernamegenerator --> Userservice: ana.gomez.0001
     Userservice -> Passwordgenerator: generate(length=12)
     Passwordgenerator --> Userservice: temp_password
     Userservice -> Userservice: generarHash(temp)

     group Transaccion atomica
       Userservice -> BaseDeDatos: registrar User\n  (username, email, password_hash,\n   first_login=true, ...)
       opt access_group_id provided
         Userservice -> BaseDeDatos: registrar Assignment\n  (user, agr, granted_by=admin)
       end
       Userservice -> BaseDeDatos: registrar InternalMessage\n  (recipient=user, body=temp_password)
       Userservice -> BaseDeDatos: registrar AuditEvent\n  USER_CREATED
     end

     Userservice --> Createuserview: {user_id, username}
     Createuserview --> Frontend: 201 Created (sin password)
     Frontend --> Admin: Toast "Creado: ana.gomez.0001"
   end
 end

 @enduml

