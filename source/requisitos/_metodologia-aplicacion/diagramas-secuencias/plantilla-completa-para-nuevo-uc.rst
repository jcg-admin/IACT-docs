17.21 Plantilla completa para nuevo UC
--------------------------------------

Punto de partida combinando los recursos más
frecuentes. Reemplazar nombres y mensajes según
el UC objetivo:

.. uml::

   @startuml
   title UC_XXX_NN — descripcion breve

   autonumber

   actor "Actor" as ActorRol
   participant "App emisora" as Emisor
   participant "App receptora" as Receptor
   database "BD destino" as BdDestino
   database "audit_log" as Audit

   ActorRol -> Emisor ++ : disparador

   alt [precondicion ok]
     Emisor -> Receptor : operacion principal
     Receptor -> BdDestino : persistir resultado
     BdDestino --> Receptor : ack
     Receptor --> Emisor : ok
     Emisor ->> Audit : registrar evento (CNST_025)
     Emisor --> ActorRol -- : exito
   else [precondicion no cumplida]
     Emisor ->> Audit : registrar denegado
     Emisor --> ActorRol -- : error
   end
   @enduml
