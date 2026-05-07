8.4 Estado del share
====================

.. uml::

 @startuml
 [*] --> active : crear
 active --> revoked : eliminar active --> expired : expires_at
 active --> orphan : view borrada (cascade)
 revoked --> [*]
 expired --> [*]
 orphan --> [*]
 @enduml
