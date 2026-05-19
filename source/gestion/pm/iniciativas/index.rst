.. meta::
   :artefacto: INDEX-PM-INICIATIVAS
   :tipo: Indice
   :dominio: gestion
   :subdominio: pm/iniciativas
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2026-05-16T23:01:11
   :ultimo_cambio: 2026-05-19T18:18:39
   :autor: NestorMonroy
   :clasificacion: Interno

.. _pm-iniciativas:

=============
Iniciativas
=============

Registro de todas las iniciativas documentales y de proyecto
ejecutadas o en curso bajo ``source/gestion/pm/``.

Cada iniciativa sigue el ciclo definido en
:doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`.

Iniciativas activas
===================

.. toctree::
   :maxdepth: 1

   auditar-cobertura-uc-implementacion/index
   integrar-contenido-rescatado/index
   plan-maestro-iniciativas-pendientes/index
   resolver-ramas-pendientes/index
   sanear-deuda-ci-y-normativa/index

Iniciativas cerradas
====================

.. toctree::
   :maxdepth: 1

   aclarar-uc-047-resolver-segmento/index
   adoptar-protocolo-grep-validado-en-auditorias/index
   ampliar-devops-runbooks/index
   auditar-conformidad-fr-tests-aceptacion/index
   crear-infrastructure-skeleton/index
   declarar-tst-ref-en-58-frs-sin-marcar/index
   documentar-ucs-implementados-no-declarados/index
   enumerar-otros-ucs-inclusion/index
   evolucionar-proc-gob-013-multirepo/index
   habilitar-jest-iact-ui/index
   habilitar-pytest-iact-api/index
   implementar-uc-rpt-05-06-programacion-reportes/index
   preparar-entorno-mariadb-ivr-legacy/index
   preparar-entorno-postgresql-iact-analytics/index
   resolver-tests-alerts-residual-iact-api/index
   resolver-tests-dashboard-iact-api/index
   resolver-tests-dashboard-residual-iact-api/index
   resolver-tests-fallidos-pytest-iact-api/index
   resolver-tests-pipeline-residual-iact-api/index
   sanear-deuda-runtime-multirepo/index
   sanear-pytest-config-iact-api/index
   verificar-mapping-docs-codigo-todos-los-dominios/index

Trazabilidad
============

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Procedimiento rector**
     - :doc:`/normativa/procedimientos/proc-gob-013-nueva-iniciativa-gestion`
   * - **Naming**
     - ``{verbo}-{objeto}`` en kebab-lowercase.
       Ejemplo: ``integrar-infrastructure-source``
   * - **Ubicacion**
     - ``source/gestion/pm/iniciativas/{nombre-iniciativa}/``
