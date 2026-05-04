.. meta::
 :artefacto: DB_001
 :tipo: Modelo de Datos
 :dominio: databases
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-04-29
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

====================
Modelo de Datos Dual
====================

El sistema IACT opera sobre dos servidores de bases de datos con
roles distintos. Almacen de Datos aloja **dos espacios logicos separados**
dentro del mismo servidor; PostgreSQL es exclusivo para tablas
operacionales de Django.

1. Almacen de Datos 10.1.48 — IVR Fuente (solo lectura)
=======================================================

- **Owner:** cliente (proveedor IVR).
- **Acceso desde IACT:** SOLO LECTURA (CNST_007).
- **Tablas:** ``tbl_historico_tN_YYYY`` — una por trimestre calendario.
- **Contenido:** registro historico de llamadas del IVR: DID, menu,
  opcion, telefono, timestamps de inicio y fin.
- **No se modifica:** IACT no escribe NADA en este espacio bajo
  ninguna circunstancia (3 niveles de enforcement: GRANT SELECT,
  Django ``managed = False``, middleware de proteccion).

2. Almacen de Datos 10.1.48 — IVR Analitica (lectura/escritura ETL)
===================================================================

- **Owner:** IACT (propio dentro del mismo servidor Almacen de Datos).
- **Acceso:** read/write para el ETL; read-only para las vistas
  Django de reportes.
- **Tablas principales:**

  - ``base_ivr_detalle`` — tabla agregada de detalle por llamada,
    generada por el ETL a partir de ``tbl_historico_*``.
  - ``base_ivr_clientes`` — tabla de dimension de clientes IVR,
    generada por el ETL.
  - ``etl_runs`` — tabla de tracking de ejecuciones ETL (propiedad
    IACT), usada por los casos de uso de supervision del pipeline.

- **El ETL trabaja completamente dentro de Almacen de Datos:** lee de las
  tablas fuente del cliente y escribe en las tablas analiticas de
  IACT. No hay transferencia de datos IVR hacia PostgreSQL.

3. PostgreSQL — Operacional IACT
=================================

- **Owner:** sistema IACT.
- **Acceso:** read/write para Django ORM (tablas operacionales).
- **Contenido exclusivo:** tablas operacionales del sistema IACT:
  usuarios, sesiones, RBAC, alertas, audit log, configuraciones.
  Todas gestionadas por el ORM Django (migraciones normales).
- **Sin datos IVR:** PostgreSQL no recibe datos del ETL ni contiene
  ninguna tabla de analitica IVR.

4. Sincronizacion
=================

El ETL sincroniza datos **dentro de Almacen de Datos**: desde las tablas
fuente ``tbl_historico_*`` (cliente) hacia las tablas analiticas
``base_ivr_*`` (IACT). El patron es TRUNCATE + INSERT (idempotente).

- **Frecuencia:** cada 6 a 12 horas (CNST_008).
- **Ventana preferente:** 02:00-04:00 hora local.
- **Sin datos hacia PostgreSQL:** PostgreSQL solo recibe operaciones
  de Django ORM para tablas de usuarios y configuracion.

Ver :doc:`etl-pipeline`.

5. Routers de base de datos
===========================

.. note::

 Los detalles de implementacion de este modelo estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
Las vistas de reportes IVR no usan modelos ORM — consultan
directamente via ``cursor.callproc()`` sobre la conexion ``ivr``
(Almacen de Datos). Ver :doc:`/arquitectura-tecnica/modulos/vis-reports/componentes`.

6. Resumen de tres bases logicas
=================================

.. list-table::
 :widths: 25 15 20 40
 :header-rows: 1

 * - Base logica
   - Servidor
   - Acceso IACT
   - Contenido
 * - IVR Fuente
   - Almacen de Datos
   - SOLO LECTURA
   - ``tbl_historico_tN_YYYY`` (del cliente)
 * - IVR Analitica
   - Almacen de Datos
   - R/W (ETL) / R (reportes)
   - ``base_ivr_detalle``, ``base_ivr_clientes``, ``etl_runs``
 * - Operacional IACT
   - PostgreSQL
   - R/W (ORM)
   - usuarios, RBAC, sesiones, alertas, audit log
