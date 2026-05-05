Contraste *pass-through* vs acceso directo
-------------------------------------------

.. uml::

   @startuml
   title Antipatron pass-through (evitar)
   class Vista
   class RptApp {
     + ultimo_evento_aud(user)
   }
   class AudApp {
     + ultimo_evento(user)
   }
   Vista --> RptApp : ultimo_evento_aud(user)
   RptApp --> AudApp : ultimo_evento(user)
   note right of RptApp
     RptApp no agrega logica:
     solo reenvia. Cambio de
     firma obliga a tocar
     Vista, RptApp y AudApp.
   end note
   @enduml

.. uml::

   @startuml
   title Acceso directo (correcto)
   class Vista
   class AudApp {
     + ultimo_evento(user)
   }
   Vista --> AudApp : ultimo_evento(user)
   note right of Vista
     Cambio de firma solo
     obliga a tocar Vista y
     AudApp. RptApp queda
     fuera del cambio.
   end note
   @enduml
