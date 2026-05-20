.. meta::
   :artefacto: TAREAS-PREPARAR-ENTORNO-MARIADB-IVR-LEGACY
   :tipo: Tareas
   :dominio: gestion
   :subdominio: pm/iniciativas/preparar-entorno-mariadb-ivr-legacy
   :repo_objetivo: IACT-db
   :estado: Pendiente
   :version: 1.0.0
   :fecha_creacion: 2026-05-19T18:31:19
   :ultimo_cambio: 2026-05-19T18:31:19
   :autor: NestorMonroy
   :clasificacion: Interno

.. _tareas-preparar-entorno-mariadb-ivr-legacy:

==========================================================
Tareas: Preparar Entorno MariaDB ivr_legacy
==========================================================

Cada tarea es atomica. Todas viven en el entorno runtime de
IACT-db (sin commits en el repo IACT-db: las acciones aplican a
servicios y BDs, no a archivos versionados). La trazabilidad
de cada tarea son las salidas observadas — capturadas en el
progreso y referenciadas en las decisiones al cierre.

Lista de tareas
================

.. list-table::
   :header-rows: 1
   :widths: 6 4 40 30 20

   * - ID
     - Repo
     - Descripcion
     - Comando
     - Estado
   * - T-001
     - IACT-db
     - Instalar paquetes MariaDB (server + client) y dejar
       el servicio activo.
     - ``apt-get install -y mariadb-server mariadb-client && service mariadb start``
     - Pendiente
   * - T-002
     - IACT-db
     - Generar ``.env`` desde ``.env.example``.
     - ``cd /home/user/IACT-db && cp .env.example .env``
     - Pendiente
   * - T-003
     - IACT-db
     - Crear BD ``ivr_legacy``, usuario ``django_user`` en
       hosts ``%`` y ``localhost``, GRANT SELECT en
       ``ivr_legacy.*`` y CREATE/DROP/INDEX/ALTER en
       ``test_ivr_legacy.*``.
     - ``bash provisioners/mariadb/setup.sh``
     - Pendiente
   * - T-004
     - IACT-db
     - Aplicar ``funciones_utilidad.sql`` (7 funciones/SPs
       prerequisito).
     - ``mysql ivr_legacy < provisioners/mariadb/funciones_utilidad.sql``
     - Pendiente
   * - T-005
     - IACT-db
     - Aplicar ``schema_base_ivr.sql`` (5 tablas base).
     - ``mysql ivr_legacy < provisioners/mariadb/schema_base_ivr.sql``
     - Pendiente
   * - T-006
     - IACT-db
     - Sembrar 3000 filas en ``tbl_temp_prueba_ivr``.
     - ``bash provisioners/mariadb/schema_seed.sh``
     - Pendiente
   * - T-007
     - IACT-db
     - Verificar conexion TCP como ``django_user`` y conteo
       de filas/tablas.
     - ``mysql -h 127.0.0.1 -u django_user -pdjango_pass ivr_legacy -e "SELECT 1;"``
     - Pendiente

DAG de dependencias
====================

* T-001 -> T-002 -> T-003 -> T-004 -> T-005 -> T-006 -> T-007
  (cadena lineal; cada paso depende del anterior).
* T-004 y T-005 son funcionalmente independientes (no se
  referencian entre si en este alcance, las funciones son
  prerequisito de SPs aun fuera de scope), pero el orden
  documental sugerido es T-004 antes que T-005.

Verificacion por tarea
========================

Cada tarea se considera completa cuando:

* La salida observada coincide con el resultado esperado del
  analisis (tabla "Cobertura analisis -> tarea").
* El paso siguiente del DAG puede ejecutarse sin error.
* El progreso registra el outcome (conteo, mensaje clave del
  log) y referencia el comando con sus parametros completos.
