.. meta::
 :artefacto: INDEX_RESTRICCIONES
 :tipo: Indice
 :dominio: normativa
 :subdominio: restricciones
 :estado: Vigente
 :version: 2.0.0
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

Principio de single responsibility
----------------------------------

Cada CNST declara **una sola restriccion**. Si un concern combina
multiples condiciones de borde (prohibicion + mecanismo alternativo,
autenticacion + autorizacion, modelo + reglas + permisos), se
descompone en CNSTs atomicas con referencias cruzadas via
``:doc:``.

Catalogo
--------

.. toctree::
 :maxdepth: 1
 :caption: Comunicaciones

 CNST_001_Prohibicion_de_Email_y_SMTP
 CNST_002_Buzon_Interno_Obligatorio

.. toctree::
 :maxdepth: 1
 :caption: Sesiones

 CNST_003_Sesiones_Persistidas_en_Base_de_Datos
 CNST_004_Sesion_Unica_por_Usuario
 CNST_005_Timeout_de_Sesion_de_15_Minutos

.. toctree::
 :maxdepth: 1
 :caption: Base de datos

 CNST_006_Arquitectura_de_Base_de_Datos_Dual
 CNST_007_Base_de_Datos_IVR_es_Solo_Lectura
 CNST_008_Sincronizacion_ETL_en_Ventana_de_6_a_12_Horas

.. toctree::
 :maxdepth: 1
 :caption: Seguridad DRF

 CNST_009_Autenticacion_DRF_Obligatoria
 CNST_010_Permission_Class_Explicita_en_Vistas_DRF
 CNST_011_Throttling_Obligatorio_en_Endpoints_Publicos
 CNST_012_Validacion_de_Input_via_Serializer
 CNST_013_Manejo_Estandarizado_de_Excepciones_DRF
 CNST_014_Paginacion_Obligatoria_en_Listados

.. toctree::
 :maxdepth: 1
 :caption: Arquitectura

 CNST_015_Antipatrones_de_Arquitectura_Prohibidos
 CNST_016_Principios_SOLID_Obligatorios

.. toctree::
 :maxdepth: 1
 :caption: Performance y exportaciones

 CNST_017_SLA_de_Tiempos_de_Respuesta
 CNST_018_Rango_Maximo_de_Consulta_de_2_Anos
 CNST_019_Exportaciones_Asincronas_Sobre_10k_Registros
 CNST_020_Throttling_de_Exportaciones_por_Formato

.. toctree::
 :maxdepth: 1
 :caption: Infraestructura

 CNST_021_Stack_Obligatorio_Ubuntu_Apache_mod_wsgi
 CNST_022_Estructura_de_Directorios_en_Servidor
 CNST_023_Rollback_Obligatorio_en_Cada_Deployment

.. toctree::
 :maxdepth: 1
 :caption: Logging y auditoria

 CNST_024_Logs_Estructurados_en_Formato_JSON
 CNST_025_Auditoria_Inmutable_Append_Only
 CNST_026_PII_Prohibida_en_Logs_y_Auditoria

.. toctree::
 :maxdepth: 1
 :caption: Datos

 CNST_027_Clasificacion_Obligatoria_de_Datos_en_4_Niveles
 CNST_028_Cifrado_Obligatorio_de_Datos_Confidenciales

.. toctree::
 :maxdepth: 1
 :caption: RBAC

 CNST_029_RBAC_Modelo_Plano
 CNST_030_Reglas_de_Separacion_de_Funciones_SoD
 CNST_031_Permisos_Temporales_Maximo_6_Meses
 CNST_032_Menu_Dinamico_Obligatorio
 CNST_033_Vocabulario_Unificado_RBAC

Convenciones
------------

- Todas las CNST estan en estado Vigente desde 2026-04-28.
- La numeracion es flat consecutiva (CNST_001 a CNST_033).
- Cada CNST tiene clasificacion ``Critico``, ``Alto`` o ``Medio``
  segun el impacto de su violacion.
- El formato de archivo y metadata sigue
  :doc:`/normativa/estandares/std-007-convencion-naming` y
  :doc:`/normativa/estandares/plantillas/tpl-cnst-restricciones`.
