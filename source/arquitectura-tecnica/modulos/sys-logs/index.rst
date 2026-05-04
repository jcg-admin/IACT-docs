.. meta::
 :artefacto: ARQ-MOD-008
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/sys-logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-008:

==========================================
ARQ_MOD_008: Bitacoras Tecnicas (SYS_LOGS)
==========================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo SYS_LOGS gestiona los **logs tecnicos** y el **estado de salud**
del sistema. Orientado a soporte, NOC y devops.

**Pregunta clave que responde:**

 *"¿Que esta pasando a nivel tecnico con el sistema y sus componentes?"*

**NO es auditoria funcional** — eso es :ref:`arq-mod-007`.

----

2. Alcance
==========

2.1 Incluye
-----------

**Logs tecnicos:**

- Errores de servidor (500, excepciones)
- Warnings de aplicacion
- Tracebacks y stack traces
- Logs de infraestructura (up/down, timeouts)

**Monitoreo:**

- Estado de salud del sistema (health endpoints)
- Estado de servicios (base de datos, caché, colas)
- Metricas tecnicas agregadas (CPU, memoria, tiempos respuesta)
- Descarga de paquetes de logs para analisis externo

2.2 Excluye (NO incluye)
------------------------

- Acciones de negocio (login, exportaciones) → :ref:`arq-mod-007`
- Reglas de seguridad → :ref:`arq-mod-003`
- PII sin enmascarar → CNST_009

----

Casos de uso relacionados: :doc:`/requisitos/casos-uso/logs/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 dependencias
 componentes
 restricciones
 casos-uso
 metricas
 diagramas/index
