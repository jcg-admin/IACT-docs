7. Diagrama de colaboraciones — UC_ALR_03 reconocer alerta
==========================================================

.. uml::

   @startuml
   allowmixing

   actor Supervisor
   object ":Alerta"        as Alerta
   object ":SecRules"      as SecRules
   object ":BuzonInterno"  as BuzonInterno
   object ":AuditLog"      as AuditLog
   object ":Suscriptores"  as Suscriptores

   Supervisor -> SecRules : "1: verificarPermiso(ack_alert)"
   SecRules -> Supervisor : "2: autorizado"
   Supervisor -> Alerta  : "3: reconocer()"
   Alerta -> Alerta           : "4: actualizar estado"
   Alerta -> AuditLog          : "5: registrar(ALERT_ACK)"
   Alerta -> BuzonInterno          : "6: notificarSuscriptores()"
   BuzonInterno -> Suscriptores          : "7: entregar mensaje\n(buzón, no email)"
   @enduml

**Aplicación:** DOC-20 (UC_NOT + UC_ALR). Sin email per
CNST_001.

----
