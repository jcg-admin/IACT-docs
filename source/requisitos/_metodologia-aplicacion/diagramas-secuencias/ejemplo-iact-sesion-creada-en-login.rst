7.1 Ejemplo IACT — Sesion creada en login
-----------------------------------------

.. uml::

   @startuml

   actor Usuario
   participant ":AuthService" as AuthService
   participant ":SessionStore" as SessionStore

   Usuario -> AuthService : login(email, password)
   activate AuthService
   AuthService -> AuthService : validarCredenciales()

   create participant ":Sesion" as Sesion
   AuthService -> Sesion : <<create>> nueva(user_id, segmento)
   activate Sesion
   Sesion -> Sesion : generarTokenJWT()
   Sesion -> Sesion : generarTokenRefresh()
   Sesion --> AuthService : token + session_id

   AuthService -> SessionStore : guardar(session)
   activate SessionStore
   SessionStore --> AuthService : ok
   deactivate SessionStore

   AuthService --> Usuario : {jwt, refresh}
   deactivate AuthService

   note right of Sesion
     Objeto Sesion creado
     en este punto del tiempo.
     Vive hasta logout o
     timeout 15 min (CNST_002).
   end note
   @enduml

----
