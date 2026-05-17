.. meta::
 :artefacto: AT_DEPLOY_ESTANDAR
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_deploy_estandar:

=====================================
Deploy View — Variante Estandar
=====================================

Topologia de despliegue estandar del sistema IACT. Cubre todos los
modulos que no requieren cache de sesiones ni pipeline ETL: consultas,
reportes, alertas, auditoria, logs, administracion de usuarios,
control de acceso RBAC.

Nodos: navegador del usuario (ClienteWeb), servidor de aplicacion
(ServidorApp con artefacto BackendIACT) y base de datos PostgreSQL
(AlmacenDatos).

.. uml::
 :caption: Deploy View IACT — variante estandar (sin cache, sin ETL).

 @startuml

 node "ClienteWeb" as ClienteWeb {
   artifact "Navegador" as Navegador
 }

 node "ServidorApp" as ServidorApp {
   artifact "BackendIACT" as BackendIACT
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 ClienteWeb --> ServidorApp  : HTTPS / REST
 ServidorApp --> AlmacenDatos : TCP / SQL

 note bottom of AlmacenDatos
   Almacen principal IACT.
   Tablas: users, sessions, assignments,
   audit_events, alerts, reports, etc.
 end note

 @enduml

Cubre los modulos: MOD_Users, MOD_Access, MOD_Permissions,
MOD_Reports, MOD_Alerts, MOD_Audit, MOD_Logs, MOD_Operator,
MOD_Supervision, MOD_Caller, MOD_Admin.

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/deploy-view/auth-cache-topology`
 :doc:`/arquitectura-tecnica/deploy-view/etl-pipeline-topology`
