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

.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
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
