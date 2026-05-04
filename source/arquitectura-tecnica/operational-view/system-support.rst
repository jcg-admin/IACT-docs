.. meta::
 :artefacto: AT_OPERATIONAL_VIEW_SUPPORT
 :tipo: Diagrama Arquitectonico — Operational View
 :dominio: arquitectura_tecnica
 :subdominio: OperationalView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-operational-support:

======================
Soporte en Produccion
======================

Procedimientos de soporte del sistema IACT en ejecucion: monitoreo del pipeline
ETL, diagnostico de alertas, consulta de logs y supervision del estado de salud
del sistema. Operado principalmente por AGR_OPERADOR y AGR_AUDITOR.

Flujo de diagnostico — fallo en pipeline ETL
==============================================

.. uml::
 :caption: Figura — Flujo de diagnostico ante fallo del pipeline ETL

 @startuml

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam ActivityDiamondBackgroundColor #FFF9C4
 skinparam shadowing false

 start

 :Sistema detecta ETLEjecucion.estado = fallido;
 :Alerta generada automaticamente\n(si threshold configurado);
 :AGR_OPERADOR recibe notificacion\nen InternalMailbox;

 :Consultar ETLLog\n(view_etl_logs — ver mensaje_error);

 if (¿Error de conexion IVR?) then (si)
   :Verificar disponibilidad BD Operativa IVR\n(CNST-007: credenciales solo lectura);
   :Escalar a Ops / DBA;
 else (no)
   if (¿Error de datos / transformacion?) then (si)
     :Revisar tablas tbl_historico_*\n(tablas origen — solo lectura);
     :Corregir parametros ETL si es necesario;
   else (no)
     :Verificar ApplicationLog\n(view_application_logs);
     :Revisar SystemHealth\n(view_system_health: CPU, memoria, disco);
   endif
 endif

 :AGR_OPERADOR solicita retry manual si procede\n(request_pipeline_retry);
 :Nuevo ETLEjecucion registrado;
 :AuditEvent generado (CNST-025);

 stop

 @enduml

Capacidades de soporte por rol
================================

.. list-table::
 :header-rows: 1
 :widths: 20 80

 * - Rol
   - Capacidades de soporte
 * - **AGR_OPERADOR**
   - Monitorear estado del pipeline ETL (``view_pipeline_status``);
     ver y reconocer alertas (``view_alerts``, ``acknowledge_alert``);
     solicitar retry de pipeline (``request_pipeline_retry``);
     ver logs ETL (``view_etl_logs``).
 * - **AGR_AUDITOR**
   - Consultar y exportar audit log (``view_audit_log``,
     ``export_audit_log``); buscar en audit log
     (``search_audit_log``); generar reportes de cumplimiento
     (``generate_compliance_report``).
 * - **AGR_ADMIN**
   - Ver sesiones activas; cerrar sesiones en caso de incidente
     de seguridad (``view_all_active_sessions``); ver
     asignaciones y reglas SoD.
 * - **Ops / DevOps**
   - Acceso a metricas tecnicas (``TechnicalMetric``:
     response_time, throughput, error_rate, CPU, memoria);
     snapshot de salud (``SystemHealth``); logs de
     infraestructura (``InfrastructureLog``).

Metricas de salud del sistema
===============================

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Metrica
   - Descripcion
 * - ``ETLEjecucion.estado``
   - Estado del ultimo run ETL: ``en_ejecucion``, ``exitoso``,
     ``fallido``. Fuente de verdad del pipeline.
 * - ``SystemHealth.cpu_usage_pct``
   - Uso de CPU del servidor de aplicacion. Snapshot periodico.
 * - ``SystemHealth.memory_usage_pct``
   - Uso de memoria RAM. Alert si supera umbral configurado.
 * - ``SystemHealth.services_status``
   - Estado de servicios clave (Django app, ETL service,
     PostgreSQL, conexion IVR). Map<String, String>.
 * - ``TechnicalMetric`` (RESPONSE_TIME)
   - Tiempo de respuesta de la aplicacion. Agregacion periodica.
 * - ``TechnicalMetric`` (ERROR_RATE)
   - Tasa de error de peticiones HTTP. Trigger para alertas.

.. seealso::

 :doc:`system-administration`
 :doc:`system-configuration`
 :doc:`/arquitectura-tecnica/process-view/index`
