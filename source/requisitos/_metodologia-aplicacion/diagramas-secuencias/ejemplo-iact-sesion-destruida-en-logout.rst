8.1 Ejemplo IACT — Sesion destruida en logout
---------------------------------------------

.. uml::

   @startuml

   actor Usuario
   participant ":Frontend"     as Frontend
   participant ":AuthService"  as AuthService
   participant ":Sesion"       as Sesion
   participant ":AuditLog"     as AuditLog

   Usuario -> Frontend : clic "Cerrar sesión"
   Frontend -> AuthService       : POST /api/auth/logout
   activate AuthService

   AuthService -> Sesion : invalidar()
   activate Sesion
   Sesion -> Sesion : marcarRevocada()
   Sesion --> AuthService : ok
   deactivate Sesion

   AuthService ->> AuditLog : registrar(LOGOUT)

   destroy Sesion
   note over Sesion
     Objeto Sesion destruido —
     tokens marcados revocados,
     entrada eliminada del
     SessionStore.
   end note

   AuthService --> Frontend : {ok}
   deactivate AuthService
   Frontend --> Usuario : redirigir a /login
   @enduml

----
