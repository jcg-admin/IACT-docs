5.1 Ejemplo IACT — UC_AUTH_01 (Iniciar sesión, todos los caminos)
-----------------------------------------------------------------

.. uml::

   @startuml

   actor Usuario
   participant ":Frontend"     as Frontend
   participant ":AuthService"  as AuthService
   participant ":SecRules"     as SecRules
   participant ":SessionStore" as SessionStore
   participant ":AuditLog"     as AuditLog

   Usuario -> Frontend : 1. submit (email, password)
   Frontend -> AuthService       : 2. POST /api/auth/login
   activate AuthService

   AuthService -> SecRules : 3. verificarThrottling(IP)\n   (CNST_011: 5 / 5min)

   alt [throttling alcanzado]
     SecRules --> AuthService : 4a. denegado
     AuthService ->> AuditLog : 5a. registrar(LOGIN_BLOCKED_IP)
     AuthService --> Frontend  : 6a. {error: "IP bloqueada"}
     Frontend --> Usuario : 7a. ✗ "Intentos máximos"
   else [throttling ok]
     SecRules --> AuthService : 4b. autorizado

     AuthService -> SessionStore  : 5b. validarCredenciales(email, hash)

     alt [credenciales válidas]
       SessionStore --> AuthService : 6b1. user_record (is_active=true)

       alt [sesión existente — CNST_002]
         AuthService -> SessionStore : 7b1. invalidarSesionAnterior()
         SessionStore --> AuthService : 7b2. ok
       end

       AuthService -> SessionStore  : 8b. crearSesion(user_id, segmento)
       SessionStore --> AuthService : 9b. session_id, jwt
       AuthService ->> AuditLog : 10b. registrar(LOGIN_SUCCESS)
       AuthService --> Frontend  : 11b. {jwt, refresh_token, user}
       Frontend --> Usuario : 12b. ✓ Redirect /dashboard
     else [credenciales inválidas]
       SessionStore --> AuthService : 6c. user_not_found
       AuthService -> SessionStore  : 7c. incrementarIntentos(IP)
       AuthService ->> AuditLog : 8c. registrar(LOGIN_FAILED)
       AuthService --> Frontend  : 9c. {error: "Credenciales"}
       Frontend --> Usuario : 10c. ✗ Mostrar error
     end
   end
   deactivate AuthService
   @enduml
