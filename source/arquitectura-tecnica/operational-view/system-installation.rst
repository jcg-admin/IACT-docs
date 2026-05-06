.. meta::
 :artefacto: AT_OPERATIONAL_VIEW_INSTALL
 :tipo: Diagrama Arquitectonico — Operational View
 :dominio: arquitectura_tecnica
 :subdominio: OperationalView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-operational-install:

================================
Instalacion y Bootstrap
================================

Procedimiento de instalacion inicial y bootstrap del sistema IACT. Cubre
desde el despliegue de la aplicacion hasta la verificacion del sistema
operacional con datos RBAC cargados.

Flujo de instalacion
=====================

.. uml::
 :caption: Figura — Flujo de instalacion y bootstrap del sistema IACT

 @startuml

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam ActivityDiamondBackgroundColor #FFF9C4
 skinparam shadowing false

 start

 partition "Infraestructura" {
   :Aprovisionar servidor(es)\n(ver deploy-view: variante aplicable);
   :Configurar variables de entorno\n(BD, JWT SECRET_KEY, IVR credentials);
   :Verificar conectividad BD Operativa IVR\n(CNST-007: GRANT SELECT);
 }

 partition "Aplicacion" {
   :Desplegar codigo Django REST Framework;
   :Instalar dependencias (pip install -r requirements.txt);
   :Ejecutar migraciones Django\n(python manage.py migrate);
 }

 partition "Bootstrap RBAC" {
   :Cargar catalogo de 64 funciones atomicas activas\n(python manage.py loaddata functions);
   :Crear AccessGroups predefinidos\n(AGR-001..012);
   :Configurar reglas SoD iniciales\n(CNST-030);
   :Crear usuario administrador inicial\n(python manage.py createsuperuser);
 }

 partition "Verificacion" {
   :Verificar build Sphinx (si entorno docs);
   :Ejecutar test suite basico;
   if (¿Verificacion exitosa?) then (si)
     :Sistema listo para operacion;
   else (no)
     :Revisar logs de instalacion\n(ApplicationLog);
     stop
   endif
 }

 :Configurar horario APScheduler\n(schedule ETL — CNST-008);
 :Notificar a AGR_ADMIN inicial\n(InternalMailbox);

 stop

 @enduml

Prerequisitos de instalacion
==============================

.. list-table::
 :header-rows: 1
 :widths: 25 75

 * - Prerequisito
   - Descripcion
 * - **PostgreSQL**
   - BD propia de IACT. Debe estar operativa antes de ejecutar
     ``manage.py migrate``. Credenciales con permisos CREATE TABLE.
 * - **Acceso BD IVR (MariaDB)**
   - Credenciales de SOLO LECTURA (GRANT SELECT) a las tablas
     ``tbl_historico_*``. P-01: nunca credenciales de escritura.
 * - **Python / pip**
   - Entorno Python con dependencias del proyecto instaladas.
 * - **Variables de entorno**
   - ``DATABASE_URL`` (PostgreSQL), ``IVR_DATABASE_URL`` (MariaDB,
     read-only), ``SECRET_KEY`` (JWT), ``DEBUG=False`` en produccion.

Variantes de despliegue
=========================

Ver :doc:`/arquitectura-tecnica/deploy-view/index` para los tres
escenarios de despliegue soportados:

- ``deploy-estandar`` — despliegue basico (app + BD propia)
- ``deploy-auth-cache`` — con cache de sesiones (Redis)
- ``deploy-etl`` — con worker ETL dedicado

.. seealso::

 :doc:`system-administration`
 :doc:`system-configuration`
 :doc:`/arquitectura-tecnica/deploy-view/index`
