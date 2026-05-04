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
gestiona datos operacionales Django. El protocolo entre cliente
y servidor es HTTPS. El acceso de Django a Almacen de Datos usa la
conexion nombrada ``ivr`` en ``DATABASES`` de Django settings.

.. uml::
 :caption: Figura 12 — Diagrama de despliegue del Sistema IACT

 @startuml

 node "<<server>>\nServidor de Aplicacion" as NODE_APP {
   node "<<OS>>\nLinux" as OS_LINUX {
     node "<<WebServer>>\nGunicorn + Nginx" as WEB_SERVER {
       node "<<service>>\nBackend IACT" as IACT_SVC {
         artifact "<<artifact>>\niact-app.wsgi" as ART_WSGI
         artifact "<<artifact>>\nsettings.py\n(DATABASES: ivr + default)" as ART_SETTINGS
       }
     }
     node "<<database system>>\nMariaDB 10.1.48" as NODE_MARIA {
       node "Website data\nbase_ivr" as SCH_BASE {
         artifact "base_ivr_detalle" as DB_DETALLE
         artifact "base_ivr_clientes" as DB_CLIENTES
       }
       node "ETL control\netl_control" as SCH_ETL {
         artifact "etl_runs" as DB_ETLR
       }
       node "IVR source\nivr_fuente" as SCH_FUENTE {
         artifact "tbl_historico_*" as DB_HIST
       }
     }
     node "<<database system>>\nPostgreSQL" as NODE_PG {
       node "operational\niact_operational" as SCH_PG {
         artifact "auth_user\nAccessGroup / AccessFunction" as DB_USERS
         artifact "audit_log" as DB_AUDIT
       }
     }
   }
 }

 node "<<client>>\nview_reports\n(PC / Navegador)" as NODE_RVG {
   node "<<app>>\nNavegador Web" as BROWSER_RVG {
     artifact "<<artifact>>\nJWT Token (LocalStorage)" as ART_JWT_RVG
     artifact "<<artifact>>\nCache Reportes (30s)" as ART_CACHE_RVG
   }
 }

 node "<<client>>\nrequest_pipeline_retry\n(PC / Navegador)" as NODE_PAG {
   node "<<app>>\nNavegador Web" as BROWSER_PAG {
     artifact "<<artifact>>\nJWT Token (LocalStorage)" as ART_JWT_PAG
   }
 }

 NODE_RVG -- NODE_APP : +receive\nFetch\n1..* a 1\nHTTPS
 NODE_PAG -- NODE_APP : +receive\nFetch\n1..* a 1\nHTTPS
 IACT_SVC -- NODE_MARIA : SQL/TCP (puerto 3306)
 IACT_SVC -- NODE_PG : SQL/TCP (puerto 5432)

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
