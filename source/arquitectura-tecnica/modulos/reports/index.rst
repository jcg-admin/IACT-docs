.. meta::
 :artefacto: ARQ-MOD-005
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-005:

===================================================
ARQ_MOD_005: Visualizacion y Reportes (VIS_REPORTS)
===================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo VIS_REPORTS es el **punto unico** para dashboards, reportes tabulares
y exportaciones del sistema IACT. Consume datos ya procesados por el ETL y
aplica permisos de RBAC_CORE.

**Pregunta clave que responde:**

 *"¿Que ve el usuario y que puede descargar, segun sus permisos, con datos del ETL?"*

----

2. Alcance
==========

2.1 Incluye
-----------

**Reportes Tabulares:**

- Reporte trimestral consolidado
- Reporte de problemas de menu/errores
- Reporte de transferencias y rutas de llamada

**Filtros y Criterios:**

- Filtros de fecha (presets, rango personalizado, limite 2 anos)
- Filtros por centro, servicio, cola, otros campos de negocio

**Exportaciones:**

- Exportar a CSV, Excel, PDF (con limites diarios segun CNST_007)

**Dashboards:**

- Dashboard principal del IVR
- Widgets de resumen operativo, graficos por hora/dia
- Distribucion por centro/servicio/menu
- Personalizacion de layout (max 10 widgets)

2.2 Excluye (NO incluye)
------------------------

- Ejecutar ETL o agendar jobs → :ref:`arq-mod-004`
- Implementar logica RBAC → :ref:`arq-mod-003`
- Real-time (WebSockets, SSE, auto-refresh) → CNST_003
- Consultas directas a BD IVR → CNST_003

----

Casos de uso relacionados: :doc:`/requisitos/casos-uso/reports/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 dependencias
 componentes
 restricciones
 diagramas/index
