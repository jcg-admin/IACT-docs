4.3 Ejemplo — UC_AUTH_01 (Iniciar sesión)
-----------------------------------------

.. uml::

   @startuml

   [*] --> Anonima

   Anonima --> Validando : intento_login(email, password) /\nverificar_credenciales()

   Validando --> Activa : [credenciales_ok && intentos < 5]\n/ generar_jwt() + registrar_auditoria()
   Validando --> Bloqueada : [intentos >= 5]\n/ bloquear_ip(CNST_011) + auditar()
   Validando --> Anonima : [credenciales_ko]\n/ incrementar_intentos() + auditar()

   Activa --> Anonima : logout() / invalidar_token() + auditar()
   Activa --> Anonima : timeout_15min(CNST_002) /\ninvalidar_sesion() + auditar()

   Bloqueada --> Anonima : tiempo_bloqueo_expira() / resetear_contador()

   Anonima --> [*]
   @enduml

----
