.. meta::
 :artefacto: INDEX_AT_DEPLOYVIEW
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: DeployView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-deployview-index:

=====================================
Deployment View — Vista de Despliegue
=====================================

Topologia de despliegue del sistema IACT. Describe los nodos fisicos,
artefactos desplegados y protocolos de comunicacion entre ellos.

El sistema IACT tiene tres variantes de topologia de despliegue:

1. **Estandar**: ClienteWeb → ServidorApp → AlmacenDatos (PostgreSQL).
   Cubre 11 de los 13 modulos del sistema.
2. **Auth con cache**: Agrega nodo CacheSession para validacion
   de tokens JWT sin consultar la BD en cada request. Cubre MOD_Auth.
3. **ETL**: Agrega BDOperativa (MariaDB, solo lectura) para el
   pipeline ETL. Cubre MOD_Pipeline.

.. toctree::
 :maxdepth: 1
 :caption: Variantes de despliegue

 deploy-estandar
 deploy-auth-cache
 deploy-etl
