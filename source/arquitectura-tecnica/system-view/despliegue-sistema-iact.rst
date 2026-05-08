.. meta::
 :artefacto: AT_UML_SISTEMA_11_DESPLIEGUE
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_despliegue:

=====================================
Sistema IACT — Diagrama de Despliegue
=====================================

11. Diagrama de Despliegue
===========================

Los nodos representan el OS, las bases de datos y el servidor de
aplicacion. La base de datos Almacen de Datos reside en el mismo servidor
de aplicacion por proximidad con el proceso ETL. PostgreSQL
gestiona datos operacionales del sistema. El protocolo entre cliente
y servidor es HTTPS. El acceso del backend a Almacen de Datos usa la
conexion nombrada ``ivr`` en la configuracion de bases de datos.

.. uml::
 :caption: Figura 12 — Diagrama de despliegue del Sistema IACT

 @startuml

 node "<<server>>\nServidor de Aplicacion" as NODO_SERVIDOR_APLICACION {
   node "<<OS>>\nLinux" as OS_LINUX {
     node "<<WebServer>>\nGunicorn + Nginx" as WEB_SERVER {
       node "<<service>>\nBackend IACT" as IACT_SVC {
         artifact "<<artifact>>\niact-app.wsgi" as ARTEFACTO_IACT_WSGI
         artifact "<<artifact>>\nsettings.py\n(DATABASES: ivr + default)" as ART_SETTINGS
       }
     }
     node "<<database system>>\nMariaDB 10.1.48" as NODO_MARIADB {
       node "Website data\nbase_ivr" as SCHEMA_WEBSITE {
         artifact "base_ivr_detalle" as BASE_DATOS_DETALLE
         artifact "base_ivr_clientes" as BASE_DATOS_CLIENTES
       }
       node "ETL control\netl_control" as SCHEMA_ETL_CONTROL {
         artifact "pipeline_runs" as BASE_DATOS_ETL_RUNS
       }
       node "IVR source\nivr_fuente" as SCHEMA_IVR_FUENTE {
         artifact "tbl_historico_*" as BASE_DATOS_HISTORICO
       }
     }
     node "<<database system>>\nPostgreSQL" as NODO_POSTGRESQL {
       node "operational\niact_operational" as SCHEMA_IACT_OPERATIONAL {
         artifact "auth_user\nAccessGroup / AccessFunction" as BASE_DATOS_USUARIOS
         artifact "audit_log" as BASE_DATOS_AUDIT
       }
     }
   }
 }

 node "<<client>>\nview_reports\n(PC / Navegador)" as NODO_CLIENTE_REPORTES {
   node "<<app>>\nNavegador Web" as NAVEGADOR_WEB {
     artifact "<<artifact>>\nJWT Token (LocalStorage)" as ARTEFACTO_JWT_REPORTES
     artifact "<<artifact>>\nCache Reportes (30s)" as ARTEFACTO_CACHE_REPORTES
   }
 }

 node "<<client>>\nrequest_pipeline_retry\n(PC / Navegador)" as NODO_CLIENTE_PIPELINE {
   node "<<app>>\nNavegador Web" as NAVEGADOR_WEB {
     artifact "<<artifact>>\nJWT Token (LocalStorage)" as ARTEFACTO_JWT_PIPELINE
   }
 }

 NODO_CLIENTE_REPORTES -- NODO_SERVIDOR_APLICACION : +receive\nFetch\n1..* a 1\nHTTPS
 NODO_CLIENTE_PIPELINE -- NODO_SERVIDOR_APLICACION : +receive\nFetch\n1..* a 1\nHTTPS
 IACT_SVC -- NODO_MARIADB : SQL/TCP (puerto 3306)
 IACT_SVC -- NODO_POSTGRESQL : SQL/TCP (puerto 5432)

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
