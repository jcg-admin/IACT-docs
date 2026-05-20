.. meta::
   :artefacto: TAREAS-Y-PROGRESO-ALINEAR-NUMERACION-UC-API-UI
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/alinear-numeracion-uc-api-ui
   :repo_objetivo: multiple
   :estado: COMPLETADA
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T22:10:00
   :ultimo_cambio: 2026-05-19T22:10:00
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-y-progreso-alinear-numeracion-uc-api-ui:

==============================================================
Tareas y Progreso: Alinear Numeracion UC api ↔ ui
==============================================================

.. list-table::
   :header-rows: 1
   :widths: 6 50 44

   * - ID
     - Descripcion
     - Resultado
   * - T-001
     - grep validado sobre IACT-ui para
       identificar features de UC_USR_05/06/07.
     - Completada. block/unblock/edit
       perfil.
   * - T-002
     - Verificar contrapartes en IACT-api.
     - Completada. Block/unblock AUSENTES;
       profile PATCH presente sin marker.
   * - T-003
     - Crear uc-083-bloquear-usuario con
       admonicion gap.
     - Completada.
   * - T-004
     - Crear uc-084-desbloquear-usuario con
       admonicion gap.
     - Completada.
   * - T-005
     - Crear uc-085-editar-perfil-propio
       con admonicion note (implementado).
     - Completada.
   * - T-006
     - Enlazar los 3 UCs en users/index.rst
       bajo caption retroactivo.
     - Completada.
   * - T-007
     - sphinx-build dummy 0 warnings.
     - Completada.
   * - T-008
     - Registrar 3 iniciativas candidatas
       derivadas.
     - Completada. En index.

Conteo
=======

* Total: 8 tareas.
* Completadas: 8/8.

Inicio: 2026-05-19T22:05:00

Cierre: 2026-05-19T22:10:00

Impacto cuantitativo
======================

Antes de esta iniciativa: 3 markers UC_USR_05/06/07
en UI sin contraparte en docs y solo 1 en API (uc-085
via PATCH ProfileView sin marker).

Despues: 3 UCs documentados (uc-083, 084, 085). Paridad
docs <-> codigo: 100% en lo que se puede verificar. Gap
real de implementacion: UC_USR_05 y UC_USR_06 (api
ausente — quedan como deuda de implementacion).
