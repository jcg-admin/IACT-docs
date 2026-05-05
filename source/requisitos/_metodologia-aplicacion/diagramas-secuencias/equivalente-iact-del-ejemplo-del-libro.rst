Equivalente IACT del ejemplo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro publica un evento ``User Created`` en Kafka
desde ``User Service``. En IACT el evento equivalente
es un **registro de auditoría** disparado desde
``aud_app`` cuando una sesión se crea, sin que el
flujo principal espere acuse:

.. uml::

   @startuml
   title UC_AUTH_01 — registro auditable async (CNST_025)

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth
   participant "log_app" as Log
   database "Redis" as Redis
   database "audit_log" as Audit

   Supervisor -> Browser : envia credenciales
   Browser -> Auth : POST /login
   Auth -> Redis : crear sesion (CNST_002)
   Auth ->> Audit : registrar evento (async)
   Auth ->> Log : notificar buzon supervisor (async, CNST_001)
   Auth --> Browser : 302 Redirect (panel)
   Browser --> Supervisor : muestra panel
   @enduml

Análisis:

- ``Auth ->> Audit`` — flecha asíncrona; el flujo
  principal no espera la confirmación de
  ``audit_log``. La invariante CNST_025 (audit
  inmutable) se preserva por construcción del bus de
  eventos: si la persistencia falla, se reintenta sin
  detener el login.
- ``Auth ->> Log`` — la notificación al buzón interno
  no bloquea la respuesta al supervisor.
- ``Auth --> B`` — síncrono (línea punteada con flecha
  rellena) porque el navegador sí espera la
  redirección.
