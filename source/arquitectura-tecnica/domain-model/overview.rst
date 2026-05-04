.. meta::
 :artefacto: AT_DOMINIO_00_OVERVIEW
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_overview:

=================================
Modelo de Dominio IACT — Overview
=================================

.. meta::
 :artefacto: MODELO_DOMINIO_IACT
 :tipo: Modelo Arquitectonico
 :dominio: arquitectura_tecnica
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-01
 :ultimo_cambio: 2026-05-01
 :autor: NestorMonroy
 :clasificacion: Critico

.. _overview-modelo-dominio-iact:

===================
MODELO DOMINIO IACT
===================

.. note::

 **Modelo conceptual canonico del dominio IACT**, complementario a
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`. Producido por
 el WP ``2026-05-01-02-01-06-domain-model-canonization`` aplicando el
 filtro de Abbott + IEEE 830 sobre el corpus vigente (80 UCs, 74
 funciones RBAC v5.5.0, BR/CNST en sus versiones vigentes).

 **Convencion de nombres**: identificadores (clases, atributos,
 operaciones, valores de enum) en **ingles** por consistencia con el
 modelo RBAC v5.5.0 y NOM_001 § 2.3. La prosa, los comentarios y las
 notas de los diagramas estan en **espanol**.

----

1. Proposito y alcance
======================

Este documento materializa las **26 clases canonicas** del dominio
IACT distribuidas en **ocho bounded contexts** (Auth, RBAC, Calls,
Reports & Metrics, Pipeline ETL, Alerts, Audit, Logs). Cada clase
incluye atributos relevantes, operaciones de negocio, restricciones
canonicas (BR/CNST en versiones vigentes) y trazabilidad a los UCs
del catalogo.

El alcance del modelo cubre los conceptos persistentes con identidad
propia y operaciones de negocio. Roles operativos
(Operator/Supervisor/Administrator/Auditor) NO son clases — se
modelan como pertenencia del usuario a un AccessGroup. El concepto
``DataSegment`` que aparecio en versiones historicas fue descartado
por Z.1.C (Camino C) y no aparece en este modelo.

----

2. Convenciones aplicadas
=========================

2.1 Identificadores en ingles
-----------------------------

- **Clases** en PascalCase (``User``, ``Session``, ``ETLEjecucion``).
- **Atributos** en snake_case (``user_id``, ``started_at``,
  ``last_login_at``).
- **Operaciones** en snake_case (``deactivate``, ``acknowledge``,
  ``schedule_report``).
- **Valores de enum** en UPPER_SNAKE (``ACTIVE``, ``ACKNOWLEDGED``).

Justificacion: el modelo RBAC v5.5.0 ya usa ingles para nombres de
funciones tras la correccion aplicada por Z.1.C. Mantener una
unica convencion idiomatica para todos los identificadores formales
del dominio reduce el costo cognitivo y el riesgo de mismatches que
documentaron las iteraciones previas v5.0..v5.2.x.

2.2 Versiones canonicas de constraints
--------------------------------------

Todas las restricciones citadas en este documento son las versiones
vigentes tras el programa Z (modelo-rbac-improvement):

.. list-table::
 :widths: 30 15 55
 :header-rows: 1

 * - Constraint
   - Version
   - Alcance
 * - BR-009 — Bajas logicas
   - v2.0.0
   - Global; toda entidad con ciclo de vida desactiva, no elimina
 * - BR-011 — Limites de exportacion
   - v2.0.0
   - Delega a CNST-019 / CNST-020; sin cifras embebidas
 * - CNST-001 — Buzon interno
   - vigente
   - Entrega de notificaciones via ``InternalMailbox``, no email
 * - CNST-002 — Caducidad de sesion
   - vigente
   - Timeout de sesion configurable
 * - CNST-003 — Sesion unica
   - vigente
   - Una sesion activa por usuario
 * - CNST-006 / 007 / 008 — Ventana ETL
   - vigente
   - Ventana de carga, BD operativa de solo lectura, BD analitica
 * - CNST-019 — Exportaciones asincronas
   - v3.0.0
   - Cola asincrona abstracta; sin acoplamiento a tecnologia
 * - CNST-020 — Throttling de exportaciones
   - v3.0.0
   - Throttling abstracto por recursos; cifras en ADR de
     implementacion
 * - CNST-024 — Retencion de logs
   - vigente
   - Periodo de retencion para los logs y snapshots de salud
 * - CNST-025 — Auditoria inmutable
   - vigente
   - Append-only en ``AuditEvent``; sin actualizar ni DELETE
 * - CNST-030 — Separacion de funciones (SoD)
   - vigente
   - Reglas de exclusion mutua entre funciones
 * - CNST-031 — Rango temporal de permisos
   - vigente
   - Permisos excepcionales con ventana ``granted_at..expires_at``

----

3. Vista global — bounded contexts y puentes
============================================

Diagrama de overview con los siete bounded contexts y las
relaciones estructurales que cruzan los limites de contexto. Para
el detalle de cada contexto ver § 4.

.. uml::
 :caption: Overview del modelo de dominio IACT — siete bounded
           contexts y puentes inter-contexto.

 @startuml

 skinparam package {
   BackgroundColor #F8F8F8
   BorderColor #888
 }

 package "Auth" as A {
   class User
   class Session
   class InternalMailbox
 }

 package "RBAC (subsume PERM)" as R {
   class Function
   class FunctionGroup
   class AccessGroup
   class Assignment
   class ExceptionalPermission
   class SeparationRule
 }

 package "Calls" as C {
   class Call
   class Campaign
 }

 package "Reports & Metrics" as P {
   class Report
   class Metric
   class ExportJob
   class ScheduledReport
   class SavedView
 }

 package "Pipeline ETL" as E {
   class ETLEjecucion
 }

 package "Alerts" as L {
   class Alert
   class Threshold
   class Subscription
 }

 package "Audit" as D {
   class AuditEvent
 }

 package "Logs" as G {
   class ApplicationLog
   class ETLLog
   class InfrastructureLog
   class SystemHealth
   class TechnicalMetric
 }

 ' Puentes estructurales entre contextos
 User      "1" -- "*"   Session
 User      "1" -- "1"   InternalMailbox
 User      "1" -- "*"   Assignment
 Function  "*" -- "*"   FunctionGroup        : (via Assignment)
 Report    "1" -- "*"   Metric                : compone
 Report    "1" -- "*"   ExportJob
 Report    "1" -- "*"   ScheduledReport
 Report    "1" -- "*"   SavedView
 Report    "*" .. "*"   Call                  : agrega
 ETLEjecucion "1" .. "*" Call                 : carga
 Alert     "*" -- "1"   Threshold
 Alert     "1" -- "*"   Subscription
 Subscription "*" -- "1" User

 note right of D
   Toda operacion de escritura en
   cualquier contexto produce 1 o mas
   AuditEvent (CNST-025: inmutable,
   append-only).
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
