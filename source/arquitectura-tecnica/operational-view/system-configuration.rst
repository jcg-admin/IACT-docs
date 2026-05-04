.. meta::
 :artefacto: AT_OPERATIONAL_VIEW_CONFIG
 :tipo: Diagrama Arquitectonico — Operational View
 :dominio: arquitectura_tecnica
 :subdominio: OperationalView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-operational-config:

=========================
Configuracion del Sistema
=========================

Parametros configurables del sistema IACT en produccion: variables de entorno,
parametros del pipeline ETL, umbrales de alerta, horarios de ejecucion
automatica y politicas de retencion de logs.

Stack tecnologico inmutable
==============================

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Componente
   - Descripcion
 * - **Django REST Framework**
   - Framework de la aplicacion. No Django plain — DRF es
     el stack oficial del proyecto.
 * - **PostgreSQL**
   - Base de datos propia de IACT. Unico almacen de escritura.
 * - **MariaDB (BD Operativa IVR)**
   - Fuente de datos del IVR. **Solo lectura** (P-01, CNST-007).
     IACT nunca escribe en esta base.
 * - **APScheduler**
   - Disparador del pipeline ETL. Embebido en el proceso Django.
     No Celery, no workers externos.

.. warning::

 **Prohibido en produccion:**
 escritura en BD Operativa IVR (MariaDB) — P-01.
 Cualquier credencial de escritura hacia MariaDB invalida CNST-007.

Categorias de configuracion
=============================

.. list-table::
 :header-rows: 1
 :widths: 22 20 58

 * - Categoria
   - Gestionada por
   - Descripcion
 * - **Variables de entorno**
   - DevOps / Ops
   - Credenciales de BD (PostgreSQL, MariaDB), claves JWT
     (``SECRET_KEY``), modo DEBUG, host y puerto de la
     aplicacion. Configuradas en el entorno de despliegue.
 * - **Conexion IVR (BD Operativa)**
   - DevOps
   - Host, puerto, credenciales de solo lectura a MariaDB.
     CNST-007: ``GRANT SELECT`` exclusivo. No modificable
     en runtime.
 * - **Parametros ETL**
   - AGR_ADMIN / Ops
   - Tablas origen (``tbl_historico_*``), trimestre de
     procesamiento, tamano de batch. Ventana de ejecucion:
     6-12 horas (CNST-008).
 * - **Horario APScheduler**
   - AGR_ADMIN
   - Expresion cron del disparador ETL automatico.
     Configurable via interfaz de administracion.
 * - **Umbrales de alerta**
   - AGR_OPERADOR
   - Valor de umbral (``Threshold.value``), operador de
     comparacion (GT/GE/LT/LE/EQ/NE), severidad.
     Gestionados por AGR_OPERADOR desde MOD_Alerts.
 * - **Retencion de logs**
   - Ops
   - Politica de retencion unificada (CNST-024) para
     ApplicationLog, ETLLog, InfrastructureLog,
     SystemHealth y TechnicalMetric.

Diagrama de estados — configuracion ETL
=========================================

.. uml::
 :caption: Figura — Estados de configuracion del pipeline ETL

 @startuml

 skinparam state {
   BackgroundColor White
   BorderColor #333333
 }
 skinparam ArrowColor #444444
 skinparam shadowing false

 [*] --> Deshabilitado : despliegue inicial

 Deshabilitado --> Configurado : AGR_ADMIN define\nschedule y parametros
 Configurado --> Activo : APScheduler inicia\nsegun schedule
 Activo --> EnEjecucion : ETL lanza run\n(CNST-008: ventana 6-12h)
 EnEjecucion --> Activo : ejecucion exitosa\n(ETLEjecucion.estado = exitoso)
 EnEjecucion --> Fallido : error en ETL\n(ETLEjecucion.estado = fallido)
 Fallido --> Activo : siguiente disparo automatico\n(P-04: fallo no bloquea)
 Activo --> Deshabilitado : AGR_ADMIN deshabilita\nschedule

 note right of EnEjecucion
   P-04: el fallo del ETL no
   corrompe datos existentes
   ni bloquea operaciones.
 end note

 @enduml

.. seealso::

 :doc:`system-administration`
 :doc:`system-support`
 :doc:`/arquitectura-tecnica/deploy-view/index`
