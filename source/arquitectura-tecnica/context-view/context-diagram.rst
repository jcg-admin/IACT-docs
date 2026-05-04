.. meta::
 :artefacto: AT_CONTEXT_VIEW_DIAGRAM
 :tipo: Diagrama Arquitectonico — Context View
 :dominio: arquitectura_tecnica
 :subdominio: ContextView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-context-diagram:

======================
Diagrama de Contexto
======================

Diagrama de contexto del sistema IACT segun el viewpoint Context de
Rozanski & Woods. Muestra la frontera del sistema, las entidades externas
y las interacciones entre ellas.

Frontera del sistema
=====================

**Dentro de la frontera IACT:**

- Aplicacion Django (12 modulos funcionales: Auth, Users, Access, Permissions,
  Reports, Alerts, Pipeline, Audit, Logs, Operator, Supervision, Caller)
- Servicio ETL (extraccion de datos IVR, transformacion, carga en BDPropia)
- Almacen de Datos propio (PostgreSQL — tablas operacionales de IACT)
- Motor de autenticacion JWT

**Fuera de la frontera IACT (entidades externas):**

- Sistema IVR / BD Operativa (MariaDB) — solo lectura (P-01)
- APScheduler / Cron — disparador del ETL
- Usuarios IACT (navegador web) — AGR_ADMIN, AGR_OPERADOR, AGR_AUDITOR

Diagrama de contexto — System boundary
========================================

.. uml::
 :caption: Figura — Context View: frontera del sistema IACT

 @startuml

 skinparam rectangle {
   BackgroundColor White
   BorderColor #333333
   RoundCorner 6
 }
 skinparam actor {
   BackgroundColor #FFFDE7
   BorderColor #F57F17
 }
 skinparam database {
   BackgroundColor #E8F5E9
   BorderColor #388E3C
 }
 skinparam shadowing false
 skinparam ArrowColor #444444

 actor "AGR_ADMIN\n(Administrador)" as Admin
 actor "AGR_OPERADOR\n(Supervisor)" as Operador
 actor "AGR_AUDITOR\n(Auditor)" as Auditor

 database "BD Operativa IVR\n(MariaDB — solo lectura)" as IVR
 rectangle "APScheduler / Cron" as Scheduler

 rectangle "  Sistema IACT  " as IACT #EEF4FF {
   rectangle "Aplicacion\nDjango REST Framework\n(12 modulos)" as App
   rectangle "Servicio\nETL" as ETL
   database "BD Propia\n(PostgreSQL)" as BDPropia
 }

 Admin -right-> IACT    : gestionar usuarios y RBAC\n(HTTPS + JWT)
 Operador -right-> IACT : supervisar pipeline\ny alertas (HTTPS + JWT)
 Auditor -right-> IACT  : consultar audit log\ny reportes (HTTPS + JWT)

 IVR -down-> ETL        : datos IVR raw\n(SQL SELECT — P-01, CNST-007)
 Scheduler -down-> ETL  : disparo ETL\n(CNST-008: ventana 6-12h)
 ETL -right-> BDPropia  : datos procesados\n(INSERT propio)

 note bottom of IVR
   IACT nunca escribe aqui.
   P-01 — restriccion absoluta.
 end note

 @enduml

Responsabilidades del sistema
==============================

.. list-table::
 :header-rows: 1
 :widths: 35 65

 * - Responsabilidad
   - Descripcion
 * - **Analisis de datos IVR**
   - Extraer, transformar y cargar datos del call center desde
     el Sistema IVR para generar reportes y dashboards analiticos.
 * - **Control de acceso RBAC**
   - Gestionar el acceso granular mediante 74 funciones atomicas,
     grupos de funciones y AccessGroups. Enforcar SoD (CNST-030)
     y permisos temporales (CNST-031).
 * - **Auditoria regulatoria**
   - Registrar de forma inmutable (CNST-025) toda accion con
     impacto en el sistema. Soporte a reportes de cumplimiento.
 * - **Gestion de alertas**
   - Detectar anomalias en metricas IVR mediante umbrales
     configurables y notificar a los operadores.
 * - **Gestion del pipeline ETL**
   - Orquestar la ejecucion del ETL en ventana permitida,
     aislar fallos (P-04) y exponer el estado a los supervisores.

Lo que el sistema NO hace
==========================

- **No escribe en la BD Operativa IVR** (P-01 — restriccion absoluta).
- **No tiene registro publico** — las cuentas son creadas exclusivamente
  por AGR_ADMIN.
- **No accede a datos de ciudadanos directamente** — los datos IVR son
  registros operativos del call center, no datos personales directos.

.. seealso::

 :doc:`external-interfaces`
 :doc:`stakeholders`
 :doc:`/arquitectura-tecnica/arquitectura-sistema/dfd-nivel-0-contexto`
