4.2 Contexto de sistema — IACT completo
---------------------------------------

.. uml::

   @startuml
   allowmixing

   package "IACT (contexto del sistema)" {
     class Usuario
     class Sesion
     class Reporte
     class Metrica
     class Alerta
     class Suscripcion
     class EjecucionETL
     class EventoAuditoria
     class IVR
     class BuzonInterno

     Usuario --> Sesion         : abre
     Usuario --> Reporte        : consulta
     Reporte --> Metrica        : agrega
     Alerta  --> Suscripcion    : notifica
     Suscripcion --> Usuario    : pertenece
     EjecucionETL --> IVR       : lee (read-only)
     Alerta --> BuzonInterno    : notifica via (CNST_001)
     Usuario --> EventoAuditoria : genera
   }

   cloud "Stripe / SendGrid" as Externos
   note right of Externos
     NO aplica a IACT —
     sin pasarela de pago,
     sin email externo.
   end note
   @enduml

----
