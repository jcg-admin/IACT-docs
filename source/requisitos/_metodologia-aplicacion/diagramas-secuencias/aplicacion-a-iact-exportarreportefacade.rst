Aplicación a IACT — ``ExportarReporteFacade``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Diagrama de flujo de código (no UC) del facade
``ExportarReporteFacade`` (ver § 6 de
:doc:`patrones-diseno`) procesando un export:

.. uml::

   @startuml
   title Code flow — ExportarReporteFacade.ejecutar (snapshot)

   autonumber

   participant "ExportarReporteFacade" as Facade
   participant "perm_app.SecRules" as Sec
   participant "rpt_app.Reporte" as Rpt
   participant "rpt_app.Worker" as Worker
   participant "aud_app.Bus" as Audit
   participant "log_app.Buzon" as Notify

   Facade -> Sec ++ : verificar(user, "exportar")
   Sec --> Facade -- : ok

   loop por cada filtro
     Facade -> Rpt : validar_filtro(f)
   end

   Facade -> Worker ++ : encolar_tarea(cfg)
   Worker --> Facade -- : tarea_id

   par
     Facade ->> Audit : registrar_evento("export_iniciado", tarea_id)
   else
     Facade ->> Notify : notificar(destinatarios, tarea_id)
   end

   Facade --> Facade : return tarea_id
   @enduml

Lectura del flujo:

- **Verificación** sync de permiso (``perm_app``).
- **Loop** sobre los filtros del request, cada uno
  validado por ``Reporte``.
- **Encolado** sync hacia el worker que procesa
  el export.
- **``par``** dispara simultáneamente el registro
  de auditoría (CNST_025) y la notificación al
  buzón interno (CNST_001) — ninguno bloquea al
  otro ni bloquea el retorno al caller.
- **``autonumber``** facilita referenciar pasos
  específicos en revisiones de PR.
