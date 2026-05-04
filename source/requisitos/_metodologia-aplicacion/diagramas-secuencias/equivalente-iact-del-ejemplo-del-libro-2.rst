Equivalente IACT del ejemplo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aplicado a UC_AUTH_01 con ``autonumber``:

.. uml::

   @startuml
   title UC_AUTH_01 — login con numeracion automatica

   autonumber

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth
   database "ldap-corporativo" as LDAP
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> Browser : envia credenciales
   Browser -> Auth : POST /login
   Auth -> Auth : validar formato
   Auth -> LDAP : authenticate(user, pass)
   LDAP --> Auth : OK + atributos
   Auth -> Redis : crear sesion (CNST_002)
   Auth ->> Audit : registrar acceso (CNST_025)
   Auth --> Browser : 302 Redirect (panel)
   Browser --> Supervisor : muestra panel
   @enduml

Referirse al diagrama es directo: *"el paso 4 es la
autenticación contra LDAP"*, *"el paso 7 es donde
disparamos audit"*. Esa precisión vale especialmente
en revisiones de PR, en sesiones de design review y
en aprobaciones arquitectónicas.
