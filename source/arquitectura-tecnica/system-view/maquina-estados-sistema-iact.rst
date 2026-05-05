.. meta::
 :artefacto: AT_UML_SISTEMA_07_ESTADOS
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_maquina_estados:

=============================================
Sistema IACT — Diagrama de Maquina de Estados
=============================================

7. Diagrama de Maquina de Estados
===================================

Ciclo de vida de la sesion de un usuario IACT. El estado inicial
es ``Autenticacion JWT``. Una vez autenticado, el usuario entra al
estado compuesto ``Dashboard IACT`` que contiene los sub-estados de
cada modulo. El modulo visible depende de las funciones RBAC del
JWT activo. Al cerrar sesion (o expirar el JWT) transita al estado
final.

.. uml::
 :caption: Figura 8 — Diagrama de maquina de estados (sesion IACT)

 @startuml

 state "Autenticacion JWT" as SERVICIO_AUTH
 SERVICIO_AUTH : entry/usuario ingresa username y password
 SERVICIO_AUTH : do/validar credenciales + cargar RBAC en PostgreSQL
 SERVICIO_AUTH : exit/JWT generado con payload de funciones

 state "Dashboard IACT" as DASHBOARD_IVR {
   state "Ver Dashboard IVR\n[view_dashboard]" as S_DASH
   state "MOD Reports\n[view_reports]" as S_RPT
   state "Gestion Pipeline ETL\n[view_pipeline_status]" as S_ETL
   state "Consulta de Logs\n[view_audit_log]" as S_LOG
   state "Gestion RBAC\n[assign_functions]" as S_RBAC

   S_DASH : entry/usuario selecciona dashboard
   S_DASH : do/callproc sp_rpt_centros_xsegmento
   S_DASH : exit/KPIs mostrados en frontend

   S_RPT : entry/usuario selecciona reporte
   S_RPT : do/UC_INC_RPT_01 + callproc sp_rpt_*
   S_RPT : exit/datos del reporte mostrados

   S_ETL : entry/usuario selecciona pipeline
   S_ETL : do/CALL sp_etl_maestro via DisparadorETL
   S_ETL : exit/estado registrado en pipeline_runs

   S_LOG : entry/usuario selecciona logs
   S_LOG : do/consultar audit_log en PostgreSQL
   S_LOG : exit/logs mostrados con paginacion

   S_RBAC : entry/assign_functions selecciona administracion
   S_RBAC : do/modificar AccessGroup y DIDs en PostgreSQL
   S_RBAC : exit/cambios guardados y propagados

   [*] --> S_DASH
   S_DASH --> S_RPT : choice=reportes
   S_DASH --> S_ETL : choice=pipeline
   S_DASH --> S_LOG : choice=logs
   S_DASH --> S_RBAC : choice=admin
   S_RPT --> S_DASH : volver
   S_ETL --> S_DASH : volver
   S_LOG --> S_DASH : volver
   S_RBAC --> S_DASH : volver
 }

 state "Cierre de Sesion" as CIERRE_SESION
 CIERRE_SESION : entry/usuario cierra sesion o JWT expira
 CIERRE_SESION : do/invalidar JWT + registrar en audit_log
 CIERRE_SESION : exit/fin de sesion

 [*] --> SERVICIO_AUTH
 SERVICIO_AUTH --> DASHBOARD_IVR : [credenciales validas]
 SERVICIO_AUTH --> CIERRE_SESION : [3 intentos fallidos]
 DASHBOARD_IVR --> CIERRE_SESION : [eliminar /api/auth/logout/]
 DASHBOARD_IVR --> CIERRE_SESION : [JWT expirado]
 CIERRE_SESION --> [*]

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
