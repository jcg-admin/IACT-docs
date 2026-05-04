.. meta::
 :artefacto: AT_UML_SISTEMA_05_ACTIVIDAD_PRINCIPAL
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_actividad_principal:

=====================================================
Sistema IACT — Diagrama de Actividad: Flujo Principal
=====================================================

5. Diagrama de Actividad — Flujo Principal
============================================

Carriles por grupo RBAC. El proceso inicia con la autenticacion
JWT de cada grupo. Tras el login exitoso el flujo se bifurca segun
las funciones propias de cada grupo. Todos convergen en el cierre
de sesion.

.. uml::
 :caption: Figura 6 — Diagrama de actividad (flujo principal por grupo RBAC)

 @startuml

 |view_reports|
 start

 |request_pipeline_retry|

 |assign_functions|

 |view_reports|
 :POST /api/auth/login — JWT;

 |request_pipeline_retry|
 :POST /api/auth/login — JWT;

 |assign_functions|
 :POST /api/auth/login — JWT;

 |view_reports|
 note right: funciones activas: view_reports / view_dashboard

 fork

   |view_reports|
   :GET /api/reportes/?trimestre=;
   :UC_INC_RPT_01 — Resolver Segmento;
   :callproc(sp_rpt_*);
   :Visualizar Reporte;

 fork again

   |request_pipeline_retry|
   :GET /api/dashboard/;
   :callproc(sp_rpt_centros_xsegmento);
   :Revisar KPIs;
   :POST /api/pipeline/ejecutar/;
   :CALL sp_etl_maestro(trimestre);
   if (ETL exitoso?) then
     :etl_runs.estado = exitoso;
   else
     :etl_runs.estado = fallido;
     :Generar Alerta BR-016;
   endif

 fork again

   |assign_functions|
   :Gestionar Funciones RBAC;
   :assign_functions / revoke_functions;
   :Asignar DIDs a Usuario;
   :Actualizar AccessGroup en PostgreSQL;

 end fork

 |request_pipeline_retry|
 :eliminar /api/auth/logout/;
 :Registrar en audit_log;
 stop

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
