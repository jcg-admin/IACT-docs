.. meta::
   :artefacto: TAREAS-Y-PROGRESO-DOCUMENTAR-UCS-IMPLEMENTADOS-NO-DECLARADOS
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/documentar-ucs-implementados-no-declarados
   :repo_objetivo: IACT-docs
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T21:50:00
   :ultimo_cambio: 2026-05-19T21:50:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-documentar-ucs-implementados-no-declarados:

==============================================================
Tareas y Progreso: Documentar UCs Implementados No Declarados
==============================================================

.. list-table::
   :header-rows: 1
   :widths: 6 50 44

   * - ID
     - Descripcion
     - Resultado
   * - T-001
     - Crear UC-078 (UC_ACC_03 — Permisos
       Efectivos).
     - Completada. RST en
       access/uc-078-permisos-efectivos-del-usuario.
   * - T-002
     - Crear UC-079 (UC_ACC_04 — Asignar
       Agrupador).
     - Completada. RST en
       access/uc-079-asignar-agrupador-a-usuario.
   * - T-003
     - Crear UC-080 (UC_ACC_05 — Reglas
       Separacion).
     - Completada. RST en
       access/uc-080-reglas-de-separacion-de-funciones.
   * - T-004
     - Crear UC-081 (UC_LOG_08 — Eventos
       pipeline analitico).
     - Completada. RST en
       logs/uc-081-ver-eventos-pipeline-analitico.
   * - T-005
     - Crear UC-082 (UC_PIP_05 — Gestionar
       Config Job ETL).
     - Completada. RST en
       pipeline/uc-082-gestionar-configuracion-job-etl.
   * - T-006
     - Enlazar los 5 nuevos UCs en sus
       indices de dominio
       (access/, logs/, pipeline/).
     - Completada.
   * - T-007
     - sphinx-build -b dummy 0 warnings.
     - Completada. Fix de Title overline en
       UC-080 aplicado.
   * - T-008
     - Diferir UC_USR_05/06/07 a iniciativa
       hermana alinear-numeracion-uc-api-ui.
     - Completada (registrada como out-of-scope
       en index).
   * - T-009
     - Documentacion iniciativa.
     - Completada.

Conteo
=======

* Total: 9 tareas.
* Completadas: 9/9.

Inicio: 2026-05-19T21:45:00

Cierre: 2026-05-19T21:50:00

Impacto cuantitativo
======================

Cobertura **docs UCs in-scope** (sin OUT):

* Antes: 56 / 56 + 5 markers extras sin docs (deuda
  documental inversa).
* Despues: **61 / 61** (56 originales + 5 nuevos UC-078..082
  documentados). Los 3 UI extras (UC_USR_05/06/07)
  pendientes de iniciativa siguiente.

Cobertura **api in-scope**: 100% (sin cambio — los markers
ya existian en codigo).

Cobertura **paridad docs ↔ código**:

* Antes: 56/61 = 92% (5 markers solo en codigo).
* Despues: **61/61 = 100% paridad** (excepto los 3 UI).
