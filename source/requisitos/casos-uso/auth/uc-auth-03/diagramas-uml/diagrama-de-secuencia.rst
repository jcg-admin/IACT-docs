8.2 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_AUTH_03 — flujo principal

 @startuml

 actor Admin as Admin
 participant "Frontend" as Frontend
 participant "ResetPasswordEndpoint" as Resetpasswordview
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

   Authservice -> BaseDeDatos: consultar User WHERE id=target_id
   BaseDeDatos --> Authservice: user
   Authservice -> Authservice: Validar (no auto-reset, no eliminado)

   Authservice -> Passwordgenerator: generate(length=12)
   Passwordgenerator --> Authservice: temp_password
   Authservice -> Authservice: generarHash(temp_password)

   group Transaccion atomica
     Authservice -> BaseDeDatos: actualizar user SET\n  password_hash=?,\n  first_login=true,\n  password_changed_at=marca_tiempo_actual
     Authservice -> BaseDeDatos: actualizar session SET\n  state='CLOSED',\n  close_reason='PASSWORD_RESET'\n  WHERE user_id=? AND state='ACTIVE'
     Authservice -> BaseDeDatos: registrar BlacklistedToken (N tokens)
     Authservice -> BaseDeDatos: registrar InternalMessage\n  (recipient=user, body=temp_pwd)
     Authservice -> BaseDeDatos: registrar AuditEvent\n  (PASSWORD_RESET)
   end

   Authservice --> Resetpasswordview: success (sin temp_password)
   Resetpasswordview --> Frontend: 200 OK
   Frontend --> Admin: "Contrasena reseteada. Notificacion en buzon."
 end

 @enduml

