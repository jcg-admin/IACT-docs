.. _uc-rpt-16-parte-08-diagrama-distribucion-de-menus:

8.3 Diagrama de distribucion — Menus IVR
==========================================

.. uml::
 :caption: UC_RPT_16 — flujo de llamadas a traves del IVR.

 @startuml

 (Entry IVR) --> (Menu principal) : n llamadas
 (Menu principal) --> (Opcion 1 - transferencia) : n
 (Menu principal) --> (cliente_colgo) : n abandono
 (Menu principal) --> (SinOpcion_Cabecera) : n abandono
 (Menu principal) --> (VACIO) : n sin menu

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/ivr-navigation-report-service`.
 - :doc:`/arquitectura-tecnica/domain-model/menu`.
