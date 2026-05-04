Resultado consolidado del capítulo
----------------------------------

El equivalente IACT del flujo cerrado del libro
(``Sign Up Flow`` con todos los enriquecimientos) es
**UC_AUTH_01 con todos los recursos aplicados**:

.. uml::

   @startuml
   title UC_AUTH_01 — flujo final con todos los recursos

   autonumber

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP
   database "Redis" as Redis
   database "audit_log" as Audit
   participant "log_app" as Log

   Supervisor -> Browser : abre URL del panel
   Browser -> Auth ++ : GET /login
   Auth --> Browser -- : 200 OK (formulario)
   Browser --> Supervisor : muestra formulario

   Supervisor -> Browser : envia credenciales
   Browser -> Auth ++ : POST /login (user, pass)
   Auth -> Auth : validar formato

   alt [credenciales invalidas]
     Auth ->> Audit : registrar intento fallido
     note right of Audit
       CNST_011 throttling:
       max 5 intentos / 5 min
     end note
     Auth --> Browser -- : 401 Unauthorized
     Browser --> Supervisor : muestra error
   else [credenciales validas]
     Auth -> LDAP ++ : authenticate(user, pass)
     LDAP --> Auth -- : OK + atributos
     Auth -> Redis : crear sesion
     note right of Redis
       CNST_002: sesion unica
     end note
     Auth ->> Audit : registrar acceso (CNST_025)
     Auth ->> Log : notificar buzon (CNST_001)
     Auth --> Browser -- : 302 Redirect (panel)
     Browser --> Supervisor : muestra panel
   end
   @enduml

Este diagrama combina **todos los recursos del
capítulo** — actores y participantes con tipos
específicos, sync + async + response, alt con dos
ramas, activaciones inline, notas anclando CNST_*,
numeración automática.
