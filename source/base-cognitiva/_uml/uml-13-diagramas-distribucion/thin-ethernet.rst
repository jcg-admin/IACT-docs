Thin ethernet
-------------

Los equipos se conectan a un cable de red mediante dispositivos
conocidos como **conectores T**. Un segmento de red puede unirse
a otro mediante un **repetidor**, dispositivo que amplifica una
señal antes de transmitirla.

.. uml::

   @startuml

   node "PC 1" <<procesador>> as PASO_AUTENTICACION
   node "PC 2" <<procesador>> as DASHBOARD_IVR
   node "PC 3" <<procesador>> as CIERRE_SESION
   node "PC 4" <<procesador>> as GESTION_PIPELINE_ETL
   node "Repetidor" <<dispositivo>> as R
   node "PC 5" <<procesador>> as CONSULTA_LOGS
   node "PC 6" <<procesador>> as MODULO_REPORTES

   PASO_AUTENTICACION -- DASHBOARD_IVR : <<conector T>>
   DASHBOARD_IVR -- CIERRE_SESION : <<conector T>>
   CIERRE_SESION -- GESTION_PIPELINE_ETL : <<conector T>>
   GESTION_PIPELINE_ETL -- R  : <<coaxial>>
   R  -- CONSULTA_LOGS : <<coaxial>>
   CONSULTA_LOGS -- MODULO_REPORTES : <<conector T>>
   @enduml
