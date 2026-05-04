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

 Authservice -> BaseDeDatos: consultar User para actualizar
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
     Authservice -> BaseDeDatos: consultar history WHERE user=?\n  ORDER BY changed_at DESC LIMIT 5
     BaseDeDatos --> Authservice: hashes[5]
     Authservice -> Authservice: for h in hashes:\n  if verificarHash(new, h): reused
     alt Reuso
       Authservice --> Changepasswordview: PasswordReused
       Changepasswordview --> Frontend: 400 PASSWORD_REUSED
     else OK
       Authservice -> Authservice: generarHash(new)

       group Transaccion atomica
         Authservice -> BaseDeDatos: actualizar user (hash, first_login=false,\n  password_changed_at=marca_tiempo_actual)
         Authservice -> BaseDeDatos: registrar password_history
         Authservice -> BaseDeDatos: actualizar other sessions (CLOSED)
         Authservice -> BaseDeDatos: registrar BlacklistedToken
         Authservice -> BaseDeDatos: registrar AuditEvent PASSWORD_CHANGED
       end

       Authservice --> Changepasswordview: success
       Changepasswordview --> Frontend: 200 OK
       Frontend --> Usuario: "Contrasena actualizada"
     end
   end
 end

 @enduml

