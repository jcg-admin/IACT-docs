4. Diagrama de estados — ``EjecucionETL`` (UC_PIP)
==================================================

.. uml::

   @startuml

   [*] --> Programada

   Programada --> Ejecutando : scheduler.dispara()
   Ejecutando --> Cargando : conexion_ivr_ok
   Cargando --> Validando : filas_cargadas

   Validando --> Exitosa : sin_errores
   Validando --> ConErrores : errores_detectados

   ConErrores --> Reintentada : admin.solicitarReintento\n(UC_PIP_04)
   Reintentada --> Ejecutando

   Exitosa --> [*]
   ConErrores --> [*] : si admin descarta

   note right of Cargando
     Ventana CNST_008 (6-12 horas).
     No real-time per CNST_006.
   end note

   note right of Reintentada
     UC_PIP_04 — sólo funciones
     autorizadas. Auditado en
     CNST_025 (inmutable).
   end note
   @enduml

**Aplicación:** UC_PIP — supervisión del ETL nocturno.

----
