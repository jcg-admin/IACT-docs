9.2 Ejemplo IACT — UC_ALR_03 (Reconocer alerta crítica con escalado)
--------------------------------------------------------------------

Cuando se reconoce una alerta crítica, antes de cerrar el
incidente debe haberse:

1. Registrado el ack en AuditLog (CNST_025).
2. Notificado a todos los suscriptores (CNST_001).

Sólo después se publica el cierre en el panel general.

.. uml::

   @startuml
   allowmixing

   actor Supervisor
   object ":Alerta"        as Alerta
   object ":SecRules"      as SecRules
   object ":AuditLog"      as AuditLog
   object ":BuzonInterno"  as BuzonInterno
   object ":Suscriptores"  as Suscriptores
   object ":PanelGeneral"  as PanelGeneral

   Supervisor -> SecRules : "1: verificar_permiso(\n   ack_alert)"
   Supervisor -> Alerta  : "2: reconocer()"
   Alerta          -> AuditLog : "2.1: registrar(\n   ALERT_ACK)"
   Alerta          -> BuzonInterno : "2.2: notificar(\n   suscriptores)"
   BuzonInterno         -> Suscriptores  : "2.2.1: entregar(buzon)"

   Alerta          -> PanelGeneral : "2.1, 2.2 /\n   3: publicar_cierre()"

   note right of Alerta
     El mensaje 3 (publicar cierre)
     espera a que se completen 2.1
     (auditoría) Y 2.2 (notificación
     vía buzón interno) antes de
     ejecutar.
   end note
   @enduml

----
