3.3 Ejemplo — EjecucionETL (UC_PIP)
-----------------------------------

.. uml::

   @startuml

   [*] --> Programada

   state Programada {
     Programada : entry / agendar(scheduler)
     Programada : do / esperar_horario_carga()
   }

   state Cargando {
     Cargando : entry / abrirConexionIVR()
     Cargando : do / leerLlamadasIVR()
     Cargando : exit / cerrarConexionIVR()
   }

   state Validando {
     Validando : entry / consultarErrores()
     Validando : do / validarFilas()
     Validando : exit / generarReporte()
   }

   Programada --> Cargando : horario_carga()
   Cargando --> Validando : carga_completa()
   Validando --> [*] : sin_errores()
   Validando --> [*] : con_errores()
   @enduml

----
