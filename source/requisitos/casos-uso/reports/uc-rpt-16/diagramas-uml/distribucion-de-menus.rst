8.3 Distribucion de menus
==========================

.. uml::

 @startuml
 (Entry IVR) --> (Menu principal) : n llamadas
 (Menu principal) --> (Opcion 1 - transferencia) : n
 (Menu principal) --> (cliente_colgo) : n abandono
 (Menu principal) --> (SinOpcion_Cabecera) : n abandono
 (Menu principal) --> (VACIO) : n sin menu
 @enduml

