8. Ejemplo completo — ciclo de vida de un Reporte programado
============================================================

UC_RPT_07 (Programar reporte) crea un objeto ``ReporteProgramado``
que pasa por varios estados a lo largo de su vida.

.. uml::

   @startuml

   [*] --> Programado

   state Programado {
     Programado : entry / registrar_en_scheduler()
     Programado : do / esperar_proxima_ejecucion()
     Programado : exit / liberar_slot()
   }

   Programado --> Ejecutando : trigger_scheduler()\n/ verificar_permiso(UC_PERM_07)

   state Ejecutando {
     Ejecutando : entry / aplicar_filtro_segmento(BR_012)
     Ejecutando : do / generar_reporte()
     Ejecutando : exit / registrar_run() + auditar(CNST_025)
   }

   Ejecutando --> Disponible : [generacion_ok]\n/ guardar_archivo()
   Ejecutando --> Fallido : [error_bd_analytics]\n/ registrar_error()
   Ejecutando --> Fallido : [throttling CNST_020 alcanzado]\n/ posponer()

   Disponible --> Notificado : / enviar_buzon_interno(CNST_001)
   Notificado --> Programado : [recurrencia_activa] / reagendar()
   Notificado --> [*] : [recurrencia_unica]

   Fallido --> Programado : [reintentos < 3]\n/ reagendar_con_delay()
   Fallido --> [*] : [reintentos >= 3]\n/ notificar_supervisor()

   note right of Ejecutando
     CNST_017 — SLA ≤ 10 s.
     CNST_008 — segmento siempre
       aplicado en SQL.
     CNST_020 — throttling diario
       por formato (CSV/Excel/PDF).
   end note
   @enduml
