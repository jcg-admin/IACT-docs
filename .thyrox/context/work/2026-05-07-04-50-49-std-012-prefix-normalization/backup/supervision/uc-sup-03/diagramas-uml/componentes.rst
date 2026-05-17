8.3 Componentes
===============

.. uml::

 @startuml
 component "Endpoint" as Endpoint
 component "MailboxService" as Mailboxservice
 component "SSE Push" as SsePush
 Endpoint --> Mailboxservice
 Endpoint --> SsePush
 @enduml

