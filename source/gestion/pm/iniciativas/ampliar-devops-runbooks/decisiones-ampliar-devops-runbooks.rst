.. meta::
   :artefacto: DECISIONES-AMPLIAR-DEVOPS-RUNBOOKS
   :tipo: Decisiones
   :dominio: gestion
   :subdominio: pm/iniciativas/ampliar-devops-runbooks
   :estado: Aprobado
   :version: 1.0.0
   :fecha_creacion: 2026-05-16T23:57:25

.. _decisiones-ampliar-devops-runbooks:

=========================================
Decisiones: Ampliar DevOps Runbooks
=========================================

1. Decisiones de diseno
========================

**D-001: No crear source/operations/ — expandir source/devops/**

Los 4 TASKs mapean directamente a source/devops/runbooks/
(runbooks operativos) y source/gestion/pm/checklists/
(checklist de go-live). Crear un dominio nuevo habria
fragmentado contenido que ya tiene un hogar establecido.

Alternativa descartada: source/operations/ como dominio
separado. Motivo de descarte: WP #12 previa estimaba 203 inputs;
al auditar el contenido real solo habia 13 MD, de los cuales
7 no son documentacion canonica. El volumen no justifica un dominio.

**D-002: TASK-038 va a checklists, no a runbooks**

Production Readiness es un checklist de go-live, no un
procedimiento operativo paso a paso ejecutable bajo presion.
Los runbooks son para incidentes y mantenimiento recurrente.
Los checklists son para validaciones previas a eventos.

**D-003: Seccion "Tecnicas de Prompt Engineering" excluida**

Los 4 TASKs incluian una seccion de scaffolding interno
(referencias a PDCAAutomationAgent, knowledge_techniques.py).
Esta seccion es metadata de generacion, no documentacion
del sistema. Se excluyo de todos los RST.

**D-004: Datos de contacto placeholder excluidos**

TASK-036 y TASK-038 incluian numeros de telefono (+1-555-XXXX)
y nombres [PENDING]. Se reemplazaron por roles (On-call engineer,
Senior DBA, Team Lead) sin datos ficticios.

**D-005: Referencias a infraestructura futura excluidas**

TASK-036 mencionaba S3, AWS CLI, HashiCorp Vault como
infraestructura actual. En la arquitectura real el stack es
Vagrant + mod_wsgi + MySQL + Cassandra local. Se documenta
el estado actual; la infraestructura futura se registra
cuando se implemente.

2. Hallazgos durante la ejecucion
===================================

**H-001: CNST-002 y CNST-008 tienen naming diferente al esperado**

Las referencias iniciales cnst-002-sesiones-bd-timeout y
cnst-008-audit-inmutable-logs-pii no existian. Los nombres
reales son cnst-002-buzon-interno-obligatorio y
cnst-008-sincronizacion-etl-en-ventana-de-6-a-12-horas.
Resuelto en esta iniciativa corrigiendo los :doc: links.

3. Verificacion post-ejecucion
================================

.. list-table::
   :widths: 55 15 30
   :header-rows: 1

   * - Criterio de completitud
     - Resultado
     - Evidencia
   * - runbook-cron-jobs-mantenimiento.rst existe en source/
     - PASA
     - source/devops/runbooks/runbook-cron-jobs-mantenimiento.rst
   * - runbook-log-retention-policies.rst existe en source/
     - PASA
     - source/devops/runbooks/runbook-log-retention-policies.rst
   * - runbook-disaster-recovery.rst existe en source/
     - PASA
     - source/devops/runbooks/runbook-disaster-recovery.rst
   * - checklist-production-readiness.rst existe en source/
     - PASA
     - source/gestion/pm/checklists/checklist-production-readiness.rst
   * - Los 4 archivos enlazados en sus index.rst
     - PASA
     - devops/runbooks/index.rst + gestion/pm/checklists/index.rst
   * - Build Sphinx 0 warnings 0 errors
     - PASA
     - build succeeded
