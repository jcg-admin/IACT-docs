7.1 Ejemplo IACT — supervisión ETL con pausa
--------------------------------------------

Si el AdminPipeline pausa la supervisión y luego reanuda, el
sistema vuelve al subestado donde estaba (no reinicia desde
``ConectandoIVR``).

.. uml::

   @startuml

   [*] --> Programada
   Programada --> Procesando : horario_carga()

   state Procesando {
     [*] --> ConectandoIVR
     ConectandoIVR --> LeyendoLlamadas
     LeyendoLlamadas --> ValidandoFilas
     ValidandoFilas --> ActualizandoBD
     state H <<history>>
   }

   Procesando --> Pausada : admin_pausa()
   Pausada --> H : admin_reanuda() /\nretomar_subestado_anterior()
   Procesando --> Exitosa : commit_exitoso()
   Exitosa --> [*]
   @enduml

----
