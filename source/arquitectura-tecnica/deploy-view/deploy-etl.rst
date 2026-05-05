.. meta::
 :artefacto: AT_DEPLOY_ETL
 :tipo: Diagrama Arquitectonico — Deployment View
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_deploy_etl:

=====================================
Deploy View — Variante ETL Pipeline
=====================================

Topologia de despliegue para el modulo de supervision ETL. Incluye
la base de datos operativa MariaDB (BD operativa, solo lectura,
CNST-007) ademas del Almacen de Datos propio de IACT. El
DisparadorETL en el servidor de aplicacion invoca Stored Procedures
en la BD operativa para extraer datos a las tablas ``tbl_historico_*``
del Almacen de Datos. Ventana de ejecucion CNST-008 (6-12 horas).

.. uml::
 :caption: Deploy View IACT — variante ETL con BD operativa MariaDB.

 @startuml

 node "ClienteWeb" as ClienteWeb {
   artifact "Navegador" as Navegador
 }

 node "ServidorApp" as ServidorApp {
   artifact "DisparadorETL" as DisparadorETL
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos {
   artifact "pipeline_runs" as EtlRuns
 }

 database "BDOperativa\n(MariaDB)" as BDOperativa {
   artifact "tbl_historico_*" as TblHistorico
 }

 ClienteWeb   --> ServidorApp   : HTTPS / REST
 ServidorApp  --> AlmacenDatos  : TCP / SQL\n(escribe pipeline_runs)
 ServidorApp  --> BDOperativa   : TCP / SP call\n(solo lectura)

 note right of BDOperativa
   CNST-007: solo lectura.
   Datos operativos del call center.
   No escribir desde IACT.
 end note

 note bottom of AlmacenDatos
   PipelineExecution persiste en pipeline_runs.
   CNST-008: ventana 6-12 horas.
 end note

 @enduml

Cubre el modulo MOD_Pipeline: UC_PIP_01 (supervisar ETL),
UC_PIP_02 (consultar errores ETL), UC_PIP_03 (disponibilidad datos),
UC_PIP_04 (solicitar reintento pipeline).

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/deploy-view/deploy-estandar`
 :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
