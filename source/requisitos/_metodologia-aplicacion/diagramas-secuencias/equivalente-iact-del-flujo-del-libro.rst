Equivalente IACT del flujo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro modela ``Sign Up Service`` validando input,
con rama ``invalid → Error`` y rama ``valid → POST
/users → 201 Created → 301 Redirect``. En IACT el
flujo análogo es **UC_AUTH_01 Login** con validación
de credenciales:

.. uml::

   @startuml
   title UC_AUTH_01 — Login con bifurcacion happy/unhappy

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> Browser : envia credenciales
   Browser -> Auth : POST /login (user, pass)
   Auth -> Auth : validar formato

   alt [credenciales invalidas]
     Auth -> Audit : registrar intento fallido (CNST_011)
     Auth --> Browser : 401 Unauthorized
     Browser --> Supervisor : muestra error
   else [credenciales validas]
     Auth -> LDAP : authenticate(user, pass)
     LDAP --> Auth : OK + atributos
     Auth -> Redis : crear sesion (CNST_002)
     Auth -> Audit : registrar acceso exitoso
     Auth --> Browser : 302 Redirect (panel)
     Browser --> Supervisor : muestra panel
   end
   @enduml
