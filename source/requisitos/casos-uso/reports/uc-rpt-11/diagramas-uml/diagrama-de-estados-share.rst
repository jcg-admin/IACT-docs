.. _uc-rpt-11-parte-08-diagrama-estados-share:

8.4 Diagrama de estados — ShareEntry
======================================

.. uml::
 :caption: ShareEntry — ciclo de vida.

 @startuml

 [*] --> active : crear (UC_RPT_11)
 active --> revoked : revocacion explicita
 active --> expired : expires_at alcanzado
 active --> orphan : view borrada (cascade)
 revoked --> [*]
 expired --> [*]
 orphan --> [*]

 note right of expired
   La aplicacion del share
   responde 403 SHARE_EXPIRED.
   Auto-cleanup tras grace period.
 end note

 note right of orphan
   Si el owner borra la SavedView,
   los ShareEntry asociados quedan
   orphan y no se aplican.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/saved-view`.
