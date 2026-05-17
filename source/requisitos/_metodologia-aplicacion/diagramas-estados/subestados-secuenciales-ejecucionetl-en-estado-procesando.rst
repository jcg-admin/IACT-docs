6.1 Subestados secuenciales — EjecucionETL en estado "Procesando"
-----------------------------------------------------------------

.. uml::

   @startuml

   [*] --> Programada

   Programada --> Procesando : horario_carga()

   state Procesando {
     [*] --> ConectandoIVR
     ConectandoIVR --> LeyendoLlamadas : conexion_ok()
     LeyendoLlamadas --> ValidandoFilas : carga_completa()
     ValidandoFilas --> ActualizandoBD : validacion_ok()
     ActualizandoBD --> [*] : commit_exitoso()
   }

   Procesando --> Exitosa : / registrar_run_ok() + auditar()
   Procesando --> ConErrores : [error_detectado]\n/ registrar_error() + alertar()

   Exitosa --> [*]
   ConErrores --> [*]

   note right of Procesando
     Estado compuesto Procesando
     con 4 subestados secuenciales
     dentro de la ventana de
     carga CNST_008 (6-12 horas).
   end note
   @enduml
