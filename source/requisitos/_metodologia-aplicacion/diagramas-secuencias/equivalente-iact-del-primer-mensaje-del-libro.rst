Equivalente IACT del primer mensaje del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro abre con ``Browser`` → ``Sign Up Service``
pidiendo la página de registro y la respuesta 200 OK
con el HTML. En IACT, el flujo análogo de primera
interacción para UC_AUTH_01 es la solicitud de la
página de login:

.. uml::

   @startuml
   title UC_AUTH_01 — primer intercambio

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth

   Supervisor -> Browser : abre URL del panel
   Browser -> Auth : GET /login
   Auth --> Browser : 200 OK (formulario login)
   Browser --> Supervisor : muestra formulario
   @enduml

Lectura:

- **Mensaje síncrono** (``->``) — el navegador hace
  ``GET /login`` y espera respuesta.
- **Respuesta** (``-->``) — ``auth_app`` retorna el
  HTML; línea punteada para distinguir del request.
- **Mensaje del actor al sistema** y **del sistema al
  actor** — capturados con sintaxis idéntica.

El render muestra mensajes con flechas distintas
(continua para síncronos, punteada para respuestas) que
permiten al lector distinguir requests de responses sin
leer las etiquetas.
