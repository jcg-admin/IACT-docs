.. _arq-mod-006-componentes:

================================================
ARQ_MOD_006 — Componentes Tecnicos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Componentes de Aplicacion
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Descripcion
 * - apps.common.notifications
   - InternalMessage, AlertConfig, servicios

----

Modelos de Datos
================

- **DSC_MOD_007_Alert** — Configuracion de alertas
- **DSC_MOD_009_InternalMessage** — Mensajes internos

.. code-block:: python

 class InternalMessage(models.Model):
     """Reemplaza completamente el email. CNST_001: No se envia correo."""
     sender = models.ForeignKey(User, null=True)  # null = sistema
     recipient = models.ForeignKey(User)
     subject = models.CharField(max_length=200)
     body = models.TextField
     message_type = models.CharField(choices=MESSAGE_TYPES)
     severity = models.CharField(choices=SEVERITY_LEVELS)
     is_read = models.BooleanField(default=False)
     read_at = models.DateTimeField(null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     alert = models.ForeignKey('Alert', null=True)

 class AlertConfig(models.Model):
     name = models.CharField(max_length=100)
     alert_type = models.CharField(choices=ALERT_TYPES)
     metric = models.CharField(max_length=100)
     condition = models.CharField(max_length=50)  # GT, LT, EQ
     threshold = models.DecimalField
     severity = models.CharField(choices=SEVERITY_LEVELS)
     recipients = models.ManyToManyField(User)
     frequency = models.CharField  # IMMEDIATE, HOURLY, DAILY
     is_active = models.BooleanField(default=True)
     snooze_until = models.DateTimeField(null=True)

 class AlertInstance(models.Model):
     config = models.ForeignKey(AlertConfig)
     triggered_at = models.DateTimeField
     metric_value = models.DecimalField
     status = models.CharField  # OPEN, ACKNOWLEDGED, CLOSED
     acknowledged_by = models.ForeignKey(User, null=True)
     acknowledged_at = models.DateTimeField(null=True)

**Usos de InternalMessage:**

- Alertas operativas
- Notificaciones de ETL (fallos, completado)
- Recuperacion de contrasena (codigo temporal)
- Avisos de cambios de roles/permisos
- Mensajes del sistema

----

APIs Expuestas
==============

**API_007_Alerts_Endpoints**

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - GET
   - /api/v1/alerts/configs
   - Listar configuraciones
 * - POST
   - /api/v1/alerts/configs
   - Crear configuracion
 * - GET
   - /api/v1/notifications
   - Bandeja de notificaciones
 * - PUT
   - /api/v1/notifications/{id}/read
   - Marcar como leida
 * - PUT
   - /api/v1/alerts/{id}/snooze
   - Silenciar alerta
 * - PUT
   - /api/v1/alerts/{id}/acknowledge
   - Confirmar alerta
