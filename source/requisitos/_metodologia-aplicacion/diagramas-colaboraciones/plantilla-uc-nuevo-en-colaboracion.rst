14.12 Plantilla — UC nuevo en colaboración
------------------------------------------

.. uml::

   @startuml
   allowmixing
   title UC_XXX_NN — vista de colaboracion

   object ":Actor" as Actor
   object ":AppEmisora" as Emisor
   object ":AppReceptora" as Receptor
   object ":BD" as BaseDatos
   object ":audit_log" as Audit

   Actor -> Emisor : "1: disparador()"
   Emisor -> Receptor : "1.1: operacion_principal(req)"
   Receptor -> BaseDatos : "1.1.1: persistir(datos)"
   BaseDatos --> Receptor : "1.1.2: ack"
   Receptor --> Emisor : "1.1.3: ok"
   Emisor -> Audit : "1.2: registrar_evento(CNST_025)"
   Emisor --> Actor : "1.3: exito"
   @enduml
