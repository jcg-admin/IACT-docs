.. _arq-mod-007-componentes:

================================================
ARQ_MOD_007 — Componentes Tecnicos
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
 * - apps.common.audit
   - Modelo AuditLog, decoradores, servicios

----

Modelos de Datos
================

**DSC_MOD_008_AuditLog** — Registro de auditoria

.. code-block:: python

 class AuditLog(models.Model):
     """Registro inmutable de auditoria funcional. CNST_009: No se modifica ni elimina."""
     # Quien
     user = models.ForeignKey(User, null=True)  # null = sistema
     user_display = models.CharField(max_length=100)  # snapshot del nombre

     # Que
     action = models.CharField(max_length=50, choices=AUDIT_ACTIONS)
     resource_type = models.CharField(max_length=50)  # User, Role, Report
     resource_id = models.CharField(max_length=100, null=True)
     resource_display = models.CharField(max_length=200)

     # Detalles
     old_value = models.JSONField(null=True)
     new_value = models.JSONField(null=True)

     # Cuando
     timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

     # Desde donde
     ip_address = models.GenericIPAddressField
     user_agent = models.TextField

     # Resultado
     result = models.CharField(choices=AUDIT_RESULTS)  # SUCCESS, FAILED, DENIED

     class Meta:
         ordering = ['-timestamp']
         indexes = [
             models.Index(fields=['user', 'timestamp']),
             models.Index(fields=['action', 'timestamp']),
             models.Index(fields=['resource_type', 'timestamp']),
         ]

----

Tipos de Accion Auditada
=========================

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Accion
   - Descripcion
   - Modulo Origen
 * - AUTH_LOGIN
   - Inicio de sesion exitoso
   - :ref:`arq-mod-001`
 * - AUTH_LOGOUT
   - Cierre de sesion
   - :ref:`arq-mod-001`
 * - AUTH_FAILED
   - Intento de login fallido
   - :ref:`arq-mod-001`
 * - USER_CREATE
   - Creacion de usuario
   - :ref:`arq-mod-002`
 * - USER_UPDATE
   - Modificacion de usuario
   - :ref:`arq-mod-002`
 * - USER_DELETE
   - Baja logica de usuario
   - :ref:`arq-mod-002`
 * - ROLE_ASSIGN
   - Asignacion de rol
   - :ref:`arq-mod-003`
 * - ROLE_REVOKE
   - Retiro de rol
   - :ref:`arq-mod-003`
 * - PERMISSION_GRANT
   - Permiso directo asignado
   - :ref:`arq-mod-003`
 * - REPORT_EXPORT
   - Exportacion de reporte
   - :ref:`arq-mod-005`
 * - ALERT_CREATE
   - Configuracion de alerta
   - :ref:`arq-mod-006`
 * - PASSWORD_CHANGE
   - Cambio de contrasena
   - :ref:`arq-mod-001`

----

Decorador de Auditoria
=======================

.. code-block:: python

 from apps.common.audit import audit_action

 @audit_action(action='USER_CREATE', resource_type='User')
 def create_user(request, data):
     # La accion se registra automaticamente
     user = User.objects.create(**data)
     return user

----

APIs Expuestas
==============

**API_008_Audit_Endpoints**

.. list-table::
 :widths: 15 40 45
 :header-rows: 1

 * - Metodo
   - Endpoint
   - Descripcion
 * - GET
   - /api/v1/audit/logs
   - Listar eventos (paginado)
 * - GET
   - /api/v1/audit/logs/{id}
   - Detalle de evento
 * - POST
   - /api/v1/audit/export
   - Exportar a CSV/Excel
 * - GET
   - /api/v1/audit/reports/permissions
   - Reporte de cambios de permisos
