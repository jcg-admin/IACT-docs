Equivalente IACT del flujo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro muestra activaciones encajadas en el flujo
sign-up con tres niveles: ``Sign Up Service`` activo
durante el POST, dentro del cual ``User Service`` se
activa para el ``POST /users``. Aplicado a UC_AUTH_01
con activaciones encajadas:

.. uml::

   @startuml
   title UC_AUTH_01 — activaciones encajadas

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP_CORPORATIVO
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> Browser : envia credenciales
   Browser -> Auth ++ : POST /login

   Auth -> Auth : validar formato

   alt [credenciales invalidas]
     Auth ->> Audit : registrar intento (CNST_011)
     Auth --> Browser -- : 401 Unauthorized
   else [credenciales validas]
     Auth -> LDAP_CORPORATIVO ++ : authenticate(user, pass)
     LDAP_CORPORATIVO --> Auth -- : OK + atributos
     Auth -> Redis : crear sesion (CNST_002)
     Auth ->> Audit : registrar acceso
     Auth --> Browser -- : 302 Redirect (panel)
   end
   Browser --> Supervisor : muestra panel
   @enduml
