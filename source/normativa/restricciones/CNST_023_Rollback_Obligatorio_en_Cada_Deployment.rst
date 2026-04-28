.. meta::
   :artefacto: CNST_023
   :tipo: Restriccion
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.0.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Critico

.. _cnst-023:

=================================================
CNST-023: Rollback Obligatorio en Cada Deployment
=================================================

Enunciado
---------

Todo deployment a produccion DEBE ser reversible mediante rollback
automatizado. Un deployment sin rollback documentado y probado NO
puede ejecutarse.

Justificacion
-------------

La reversion rapida de un deployment fallido es la diferencia entre
un incidente menor y una caida prolongada. Es responsabilidad del
deployer probar el rollback antes del go-live.

Especificacion
--------------

- Mecanismo: cambio de symlink ``current`` a release anterior +
  reload de Apache.
- Tiempo objetivo de rollback: <60 segundos.
- Migraciones que impidan rollback (drop column, drop table)
  requieren ADR explicito y plan de mitigacion.
- ``deploy.sh`` y ``rollback.sh`` deben coexistir y estar versionados.

Verificacion
------------

.. code-block:: bash

   test -x scripts/rollback.sh
   bash scripts/rollback.sh --dry-run

Referencias cruzadas
--------------------

- :doc:`CNST_022_Estructura_de_Directorios_en_Servidor`
