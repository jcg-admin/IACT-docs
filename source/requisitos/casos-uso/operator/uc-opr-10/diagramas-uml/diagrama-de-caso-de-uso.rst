8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_10 — actores y casos asociados

 @startuml

 left to right direction

 actor "read_own_mailbox" as INVOKER
 actor "InternalMailbox" as MB <<sistema>>
 actor "Supervisor" as SUPER <<beneficiario>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_10\nLeer Buzon Interno" as UC_OPR_10
   usecase "Listar mensajes\n(unread first)" as LISTAR
   usecase "Marcar como leido" as MARCAR
   usecase "Soporta broadcasts\n(UC_SUP_03)" as BROADCAST <<extend>>
   usecase "Soporta alertas\noperacionales" as ALERTAS_OP <<extend>>
 }

 INVOKER --> UC_OPR_10
 UC_OPR_10 ..> LISTAR : <<include>>
 UC_OPR_10 ..> MARCAR : <<include>>
 BROADCAST ..> UC_OPR_10 : <<extend>>
 ALERTAS_OP ..> UC_OPR_10 : <<extend>>

 LISTAR --> MB
 MARCAR --> MB
 BROADCAST --> SUPER

 note bottom of UC_OPR_10
   CNST-001 NO email externo +
   CNST-002 obliga mailbox interno —
   este UC es la lectura por el agente.
   Mensajes: broadcast (UC_SUP_03),
   individual del supervisor,
   alertas operacionales (export
   ready, schedule paused, etc.).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   InternalMailbox del User (CNST-002).
 - :doc:`/arquitectura-tecnica/domain-model/user` —
   User propietario del buzon.
 - :doc:`/requisitos/casos-uso/supervision/uc-sup-03/index` —
   broadcast origen.
