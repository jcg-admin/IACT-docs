.. meta::
   :artefacto: INDEX_RESTRICCIONES
   :tipo: Indice
   :dominio: normativa
   :subdominio: restricciones
   :estado: Vigente
   :version: 1.1.0
   :fecha_creacion: 2025-12-17
   :ultimo_cambio: 2026-04-28
   :autor: NestorMonroy
   :clasificacion: Interno

Restricciones Tecnicas
======================

Las restricciones (CNST) son condiciones de borde no negociables del
sistema IACT. Definen los limites tecnicos, de seguridad, de
arquitectura y de operacion que toda solucion debe respetar.

A diferencia de los requisitos (que describen QUE debe hacer el
sistema), las restricciones describen QUE NO PUEDE hacer o bajo QUE
condiciones puede operar. Sirven como input arquitectonico para los
casos de uso, los requisitos funcionales y las decisiones de diseno.

Catalogo
--------

.. toctree::
   :maxdepth: 1
   :caption: Restricciones del sistema

   CNST_001_Comunicaciones_Prohibidas
   CNST_002_Gestion_Sesiones_BD
   CNST_003_Base_Datos_Dual_Inmutable
   CNST_004_Actualizacion_Datos_ETL
   CNST_005_Seguridad_DRF_Checklist
   CNST_006_Antipatrones_Arquitectura
   CNST_007_Limites_Performance_SLA
   CNST_008_Infraestructura_Deployment
   CNST_009_Logging_Auditoria_Inmutable
   CNST_010_Clasificacion_Proteccion_Datos
   CNST_011_RBAC_Flat_SoD_Permisos

Estructura por dominio
----------------------

**Comunicaciones y sesiones**

- :doc:`CNST_001_Comunicaciones_Prohibidas` — prohibicion de email,
  uso obligatorio de buzon interno.
- :doc:`CNST_002_Gestion_Sesiones_BD` — sesiones unicas en BD con
  timeout de 15 minutos.

**Base de datos**

- :doc:`CNST_003_Base_Datos_Dual_Inmutable` — BD dual con BD IVR de
  solo lectura.
- :doc:`CNST_004_Actualizacion_Datos_ETL` — ETL con ventana de 6 a
  12 horas, sin tiempo real.

**Seguridad y control de acceso**

- :doc:`CNST_005_Seguridad_DRF_Checklist` — checklist de seguridad
  para Django REST Framework.
- :doc:`CNST_011_RBAC_Flat_SoD_Permisos` — modelo RBAC plano,
  segregacion de funciones, permisos temporales.

**Arquitectura y performance**

- :doc:`CNST_006_Antipatrones_Arquitectura` — antipatrones
  prohibidos y patrones recomendados.
- :doc:`CNST_007_Limites_Performance_SLA` — limites de performance,
  rangos de reportes, throttling.

**Infraestructura y operacion**

- :doc:`CNST_008_Infraestructura_Deployment` — restricciones de
  infraestructura y deployment.

**Auditoria y datos**

- :doc:`CNST_009_Logging_Auditoria_Inmutable` — logging y auditoria
  inmutable, sin PII en logs.
- :doc:`CNST_010_Clasificacion_Proteccion_Datos` — clasificacion y
  proteccion de datos.

Convenciones
------------

- Todas las CNST estan en estado Vigente desde 2026-04-28.
- La numeracion es flat consecutiva (sin gaps): CNST_001 a CNST_011.
- Cada CNST tiene clasificacion ``Critico`` o ``Alto`` segun el
  impacto de su violacion.
- El formato de archivo y metadata sigue ``STD_007_Convencion_Naming``
  y ``TPL_CNST_Restricciones``.
