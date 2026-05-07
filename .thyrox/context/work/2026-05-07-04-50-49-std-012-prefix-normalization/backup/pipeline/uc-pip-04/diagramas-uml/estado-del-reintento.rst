8.3 Estado del reintento
=========================

.. uml::

 @startuml
 [*] --> en_ejecucion : POST reintento aceptado
 en_ejecucion --> exitoso : SP completa sin errores
 en_ejecucion --> fallido : SP lanza error
 exitoso --> [*]
 fallido --> [*] : requiere nuevo reintento
 @enduml

