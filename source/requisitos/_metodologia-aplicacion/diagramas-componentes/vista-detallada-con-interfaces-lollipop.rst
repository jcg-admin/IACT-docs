4. Vista detallada con interfaces (lollipop)
============================================

Ejemplo: flujo de exportación de reporte UC_RPT_04.

.. uml::

   @startuml
   skinparam componentStyle rectangle

   [rpt_app] as SERVICIO_REPORTES
   [perm_app] as SERVICIO_PERMISOS
   [aud_app] as SERVICIO_AUDITORIA
   [log_app] as SERVICIO_LOGS
   database "bd_analytics" as BD_ANALYTICS

   SERVICIO_PERMISOS -( ISecurity
   SERVICIO_AUDITORIA  -( IAuditLog
   SERVICIO_LOGS  -( INotificacion
   SERVICIO_REPORTES  -( IReporte
   BD_ANALYTICS  -( IDatosAnalytics

   SERVICIO_REPORTES ..> ISecurity : usa
   SERVICIO_REPORTES ..> IDatosAnalytics : usa
   SERVICIO_REPORTES ..> IAuditLog : usa
   SERVICIO_REPORTES ..> INotificacion : usa (buzon CNST_001)
   @enduml

Lectura: ``rpt_app`` *realiza* ``IReporte`` e*importa*
``ISecurity``, ``IDatosAnalytics``, ``IAuditLog`` e
``INotificacion``. Cualquier cambio interno en ``perm_app``
es transparente para ``rpt_app`` mientras ``ISecurity`` se
mantenga estable.
