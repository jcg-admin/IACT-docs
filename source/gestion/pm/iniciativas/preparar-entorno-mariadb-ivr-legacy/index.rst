.. meta::
   :artefacto: INICIATIVA-PREPARAR-ENTORNO-MARIADB-IVR-LEGACY
   :tipo: Iniciativa
   :dominio: gestion
   :subdominio: pm/iniciativas
   :repo_objetivo: IACT-db
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:31:19
   :ultimo_cambio: 2026-05-19T18:31:19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _iniciativa-preparar-entorno-mariadb-ivr-legacy:

==========================================================
Iniciativa: Preparar Entorno MariaDB ivr_legacy
==========================================================

Habilita el ejecutar pruebas del proyecto IACT-api que dependen
de la base de datos legada ``ivr_legacy`` en MariaDB. Sin esta
base con datos simulados, los tests de Django que tocan el ORM
``ivr`` fallan por conexion o por tablas inexistentes.

Es la primera iniciativa del sistema con ``:repo_objetivo:``
distinto de ``IACT-docs`` o ``multiple``: documenta en IACT-docs
(este repo) la ejecucion realizada sobre IACT-db (provisioners
de MariaDB) en un entorno de pruebas runtime. Sigue el modelo C
de PROC-GOB-013 v2.0.0 (D3): documentacion siempre en IACT-docs,
ejecucion en el repo declarado.

El volumen de produccion (~11-14M filas en ``tbl_historico_*``)
se reduce a magnitudes simuladas en el entorno de pruebas
(``SEED_ROWS=3000`` por defecto), suficiente para validar logica
del ORM, queries y stored procedures sin saturar recursos del
contenedor de desarrollo.

.. toctree::
   :maxdepth: 1

   alcance-preparar-entorno-mariadb-ivr-legacy
   analisis-preparar-entorno-mariadb-ivr-legacy
   tareas-preparar-entorno-mariadb-ivr-legacy
   progreso-preparar-entorno-mariadb-ivr-legacy
