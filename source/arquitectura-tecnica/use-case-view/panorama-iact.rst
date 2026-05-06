.. meta::
 :artefacto: AT_UC_PANORAMA
 :tipo: Diagrama Arquitectonico — Panorama IACT
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_panorama:

=============================
Panorama IACT — Vista Sistema
=============================

Diagrama de **alto nivel del sistema completo** mostrando
los UCs operativos clave por dominio funcional con sus
actores. Inspirado en
``ejemplo-iact-diagrama-de-alto-nivel.rst`` de
``_metodologia-aplicacion``.

Per uml-07 ``profundizacion.rst``: este panorama es el
punto de entrada — desde cada UC se profundiza al modelo
detallado de su módulo.

.. note:: Scope visual del panorama (v5.6.0)

 Este diagrama muestra UC_OPR_02 como representante de la
 actividad del Operator, pero **MOD_Operator y MOD_Supervision
 son reservados open-closed** para esta release (ver
 :doc:`/requisitos/casos-uso/operator/index`,
 :doc:`/requisitos/casos-uso/supervision/index`). El UC
 aparece en el panorama por valor narrativo del flujo
 end-to-end — no implica implementacion in-scope.

.. uml::
 :caption: Panorama IACT — UCs operativos clave por
           dominio con actores principales.

 @startuml
 left to right direction

 actor Operator
 actor Supervisor
 actor AccessAdmin
 actor PipelineAdmin
 actor Auditor
 actor "Scheduler\n<<system>>" as Scheduler
 actor "IvrSwitch\n<<system>>" as IvrSwitch
 actor "Caller\n<<external>>" as Caller

 rectangle "IACT" {
   usecase "UC_AUTH_01\nIniciar Sesion" as AUTH01
   usecase "UC_OPR_02\nAtender Llamada" as OPR02
   usecase "UC_RPT_01\nVer Dashboard" as RPT01
   usecase "UC_RPT_03\nVer Reportes\nHistoricos\n.. extension points ..\nExportar / Programar / Filtrar" as RPT03
   usecase "UC_RPT_04\nExportar Reporte" as RPT04
   usecase "UC_ALR_03\nReconocer Alerta" as ALR03
   usecase "UC_ACC_01\nAsignar Funciones" as UC_ACC_01
   usecase "UC_PERM_07\nVerificar Permiso" as PERM07
   usecase "UC_PIP_01\nVer Estado\nPipeline" as PIP01
   usecase "UC_PIP_04\nReintentar Pipeline" as PIP04
   usecase "UC_AUD_01\nConsultar Auditoria" as AUD01
   usecase "UC_CLI_01\nLlamar al IVR" as CLI01
   usecase "Ejecutar Pipeline\nAutomatico" as PIPELINE_AUTO
 }

 Operator      --> AUTH01
 Operator      --> OPR02
 Operator      --> RPT01
 Operator      --> RPT03
 Operator      --> ALR03

 Supervisor    --> RPT04
 AccessAdmin   --> UC_ACC_01
 PipelineAdmin --> PIP01
 PipelineAdmin --> PIP04
 Auditor       --> AUD01
 Scheduler     --> PIPELINE_AUTO
 Caller        --> CLI01
 IvrSwitch     <-- PIPELINE_AUTO

 RPT04 ..> RPT03 : <<extend>>

 AUTH01     ..> PERM07 : <<include>>
 RPT01      ..> PERM07 : <<include>>
 RPT03      ..> PERM07 : <<include>>
 RPT04      ..> PERM07 : <<include>>
 UC_ACC_01  ..> PERM07 : <<include>>
 PIP04      ..> PERM07 : <<include>>
 AUD01      ..> PERM07 : <<include>>

 OPR02      ..> CLI01 : <<include>>

 note right of PERM07
   UC_PERM_07 es el include canónico
   de toda verificacion de permiso (P-15).
   Aparece en ~todos los UCs operativos.
 end note

 @enduml

Lectura del panorama
====================

**Actores operativos** (humanos):

- ``Operator`` (AGR-001) — agente del call center.
  Inicia sesión, atiende llamadas, consulta dashboards
  y reportes, reconoce alertas.
- ``Supervisor`` (AGR-002..005) — hereda Operator.
  Agrega exportación de reportes y operaciones de
  supervisión.
- ``AccessAdmin`` (AGR-007) — gestiona asignaciones
  RBAC.
- ``PipelineAdmin`` (AGR-009) — supervisa el pipeline
  batch.
- ``Auditor`` (AGR-008) — consulta el log de
  auditoría inmutable.

**Actores sistema/externos:**

- ``Scheduler`` — cron / APScheduler dispara el
  pipeline batch nocturno.
- ``IvrSwitch`` — sistema PBX externo origen de las
  llamadas.
- ``Caller`` — caller externo no autenticado.

**Patrón cross-cutting:**

- ``UC_PERM_07 Verificar Permiso`` es el ``<<include>>``
  canónico que aparece en todos los UCs operativos
  (P-15 RBAC granular).
- ``UC_RPT_04 Exportar`` extiende ``UC_RPT_03 Ver
  Reportes Historicos`` (visible en su extension
  points).

.. seealso::

 :doc:`/base-cognitiva/_uml/uml-07-diagramas-casos-uso/profundizacion`
 :doc:`/requisitos/_metodologia-aplicacion/casos-uso-diagramas/ejemplo-iact-diagrama-de-alto-nivel`
 :doc:`mapa-funciones-rbac`
 :doc:`index`
