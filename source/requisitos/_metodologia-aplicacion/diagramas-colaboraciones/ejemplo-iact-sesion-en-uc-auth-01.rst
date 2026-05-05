6.1 Ejemplo IACT — Sesion en UC_AUTH_01
---------------------------------------

.. uml::

   @startuml
   allowmixing

   object "sesion : Sesion\n[Anonima]"  as SesionAnonima
   object ":AuthService"                as AuthService
   object ":SessionStore"               as SessionStore
   object "sesion : Sesion\n[Activa]"   as SesionActiva

   actor Usuario

   Usuario -> AuthService : "1: login(email, pass)"
   AuthService -> SessionStore      : "2: validar_credenciales()"
   SessionStore -> AuthService      : "3: ok + segmento"
   AuthService -> SesionAnonima     : "4: invalidar_anonima()"
   AuthService -> SesionActiva      : "5: crear_activa(token)"
   SesionAnonima ..> SesionActiva   : "<<se_transforma_en>>"
   @enduml
