.. meta::
 :artefacto: ARQ-MOD-004
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-004:

=======================================================
ARQ_MOD_004: Supervision ETL y Calidad (ETL_MONITORING)
=======================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo ETL_MONITORING **supervisa el pipeline ETL** sin ejecutarlo.
Permite ver el estado de las cargas, disponibilidad de datos, y errores
de transformacion.

**Pregunta clave que responde:**

 *"¿El ETL esta bien, cuando corrio, que datos tengo disponibles y que fallo?"*

**NO ejecuta ETL** desde la UI. El ETL corre como job nocturno automatizado.

----

2. Alcance
==========

2.1 Incluye
-----------

- Consultar historico de ejecuciones ETL (jobs, duracion, resultado)
- Ver detalle de una ejecucion (tablas, metricas, errores)
- Consultar disponibilidad de datos por periodo (trimestres completos/parciales)
- Consultar incidencias de calidad (nulos, duplicados, inconsistencias)
- Reintentar procesamiento logico sobre datos ya extraidos

2.2 Excluye (NO incluye)
------------------------

- Ejecutar ETL manualmente → Job nocturno automatizado
- Generar reportes de negocio → :ref:`arq-mod-005`
- Exponer logs tecnicos crudos → :ref:`arq-mod-008`
- Consultas directas a BD IVR (mas alla de vw_llamadas) → CNST_003

----

Casos de uso relacionados: :doc:`/requisitos/casos-uso/pipeline/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 dependencias
 componentes
 restricciones
 diagramas/index
