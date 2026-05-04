Equivalente IACT del ejemplo del libro
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El libro agrega ``Note left of Kafka: other services
take action based on this event`` para señalar el
fan-out del evento. En IACT el fan-out equivalente es
el bus interno de auditoría: un evento auditable
disparado desde una app es consumido por
``aud_app`` y, en algunos UCs, también por
``log_app`` para notificar al supervisor.

.. uml::

   @startuml
   title UC_AUTH_01 — fan-out auditable

   actor Supervisor
   participant "Browser" as Browser
   participant "auth_app" as Auth
   participant "log_app" as Log
   database "audit_log" as Audit

   Supervisor -> Browser : envia credenciales
   Browser -> Auth : POST /login

   Auth ->> Audit : registrar evento (CNST_025)
   note right of Audit
     audit_log es immutable;
     no se reasigna ni borra
   end note

   Auth ->> Log : notificar buzon supervisor
   note over Log : entrega via buzon interno (CNST_001)

   Auth --> Browser : 302 Redirect (panel)
   Browser --> Supervisor : muestra panel
   @enduml

Análisis:

- **``note right of Audit``** — recuerda al lector la
  invariante CNST_025 sin saturar la etiqueta del
  mensaje. La nota se queda al lado del destino
  relevante.
- **``note over Log``** — ubica el comentario sobre el
  participante; útil cuando el detalle es **del
  participante**, no del mensaje específico.
- **Notas atravesando dos lifelines** son útiles para
  describir un **acuerdo entre componentes** (ej. un
  contrato de retry, una garantía de orden).
