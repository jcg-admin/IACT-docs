.. meta::
 :artefacto: AT_DESIGN_PACKAGE_OVERVIEW
 :tipo: Diagrama Arquitectonico — Design View — Package Overview
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_package_overview:

============================================================
Design View — Package Overview: Modulos y Dependencias
============================================================

Vista de paquetes a nivel sistema. Cada paquete corresponde a un
modulo funcional (bounded context) del catalogo CNST-033 dentro
del scope de implementacion. Las relaciones de dependencia entre
paquetes muestran el orden de lectura recomendado y los
acoplamientos esperados.

NO duplica las clases del domain-model — cada paquete agrupa las
clases que viven en su bounded context. Para detalle ver
``class-{mod}.rst`` por modulo.

.. note::

 **Scope de implementacion:** los modulos MOD_Operator,
 MOD_Supervision y MOD_Caller estan documentados en
 ``use-case-view/`` como vista de requisitos pero **NO entran
 en este DesignView** porque no se implementan en el scope
 actual. Su DesignView se construira si/cuando se decida
 implementarlos.

.. uml::
 :caption: Sistema IACT — paquetes funcionales en scope.

 @startuml

 left to right direction

 package "MOD_Auth" as MOD_Auth
 package "MOD_Permissions" as MOD_Permissions
 package "MOD_Access" as MOD_Access
 package "MOD_Admin" as MOD_Admin
 package "MOD_Users" as MOD_Users

 package "MOD_Audit" as MOD_Audit

 package "MOD_Pipeline" as MOD_Pipeline
 package "MOD_Reports" as MOD_Reports
 package "MOD_Alerts" as MOD_Alerts
 package "MOD_Logs" as MOD_Logs

 ' --- Dependencias core ---
 MOD_Permissions ..> MOD_Auth : verifica sesion
 MOD_Access ..> MOD_Permissions : grupos -> funciones
 MOD_Access ..> MOD_Admin : reglas SoD
 MOD_Admin ..> MOD_Permissions : catalogo funciones
 MOD_Users ..> MOD_Permissions : assignments

 ' --- Datos y observabilidad ---
 MOD_Pipeline ..> MOD_Audit : eventos ETL
 MOD_Reports ..> MOD_Pipeline : KPIs
 MOD_Reports ..> MOD_Permissions : view_*_report
 MOD_Alerts ..> MOD_Reports : metric thresholds
 MOD_Logs ..> MOD_Audit : application logs

 ' --- Auditoria es transversal ---
 MOD_Auth ..> MOD_Audit
 MOD_Access ..> MOD_Audit
 MOD_Admin ..> MOD_Audit
 MOD_Users ..> MOD_Audit
 MOD_Permissions ..> MOD_Audit

 note bottom of MOD_Audit
   Modulo transversal: TODA escritura
   en cualquier modulo emite AuditEvent.
   CNST-026: sin PII en logs.
 end note

 note top of MOD_Auth
   Capa fundamental: sesion + JWT.
   Sin auth valida no se ejecuta
   ningun otro modulo.
 end note

 @enduml

----

Capas conceptuales
==================

.. list-table::
 :header-rows: 1
 :widths: 25 35 40

 * - Capa
   - Modulos
   - Responsabilidad
 * - **Fundamental**
   - MOD_Auth
   - Sesion, JWT, blacklist, expiration policy
 * - **Modelo RBAC**
   - MOD_Admin, MOD_Permissions, MOD_Access, MOD_Users
   - Configuracion (Admin), runtime check (Permissions),
     asignaciones (Access), gestion usuarios (Users)
 * - **Datos y reporting**
   - MOD_Pipeline, MOD_Reports, MOD_Alerts, MOD_Logs
   - ETL, KPIs, alertas operativas, observabilidad
 * - **Transversal**
   - MOD_Audit
   - Auditoria de todas las escrituras del sistema

----

Modulos fuera del scope de implementacion
==========================================

Documentados en ``use-case-view/`` como vista de requisitos pero
sin DesignView en este WP:

- **MOD_Operator** (UC_OPR_01..10) — operaciones del agente
  (cambio de estado, manejo de llamada, disposition, breaks,
  dashboard, mailbox).
- **MOD_Supervision** (UC_SUP_01..03) — supervision en tiempo
  real, barge-in, broadcast.
- **MOD_Caller** (UC_CLI_01..05) — modelo de llamada, IVR,
  CSAT post-call.

Si en el futuro se decide implementar alguno de estos, su
DesignView se construira en un WP separado consumiendo este
package-overview como base + class-{mod} adicionales.

----

Orden de lectura recomendado
=============================

Para entender el sistema dentro del scope actual, leer los
modulos en este orden:

1. **MOD_Auth** — fundamento: sesion + JWT.
2. **MOD_Admin** — configuracion del catalogo RBAC.
3. **MOD_Permissions** — runtime check del catalogo.
4. **MOD_Access** — asignaciones de grupos a usuarios.
5. **MOD_Users** — gestion de usuarios.
6. **MOD_Pipeline** — ETL y datos crudos.
7. **MOD_Reports** — KPIs y reportes.
8. **MOD_Alerts** — alertas sobre metricas.
9. **MOD_Logs** — observabilidad tecnica.
10. **MOD_Audit** — auditoria (transversal).

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/index` — definicion
   completa de las 85 clases canonicas que viven en estos paquetes.
 - :doc:`/arquitectura-tecnica/use-case-view/index` — UCs por
   modulo (incluyendo los out-of-scope).
 - :doc:`/arquitectura-tecnica/design-view/index` — vista de
   diseno completa.
