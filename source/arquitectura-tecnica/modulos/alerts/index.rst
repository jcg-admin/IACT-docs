.. meta::
 :artefacto: ARQ-MOD-006
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/alerts
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-006:

==============================================
ARQ_MOD_006: Alertas y Notificaciones (ALERTS)
==============================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo ALERTS gestiona el **sistema de alertas operativas** y el
**buzon interno de notificaciones**. Respeta la restriccion critica de
**NO EMAIL** — todo se entrega via InternalMessage.

**Pregunta clave que responde:**

 *"¿Que condiciones disparan alertas y que mensajes internos se envian a los usuarios?"*

----

2. Alcance
==========

2.1 Incluye
-----------

- Configuracion de alertas operativas (THRESHOLD, ANOMALY, TREND)
- Evaluacion periodica de condiciones de alerta
- Buzon interno (InternalMessage) — reemplaza email
- Bandeja de notificaciones con filtros
- Silenciar/posponer alertas (snooze)
- Confirmar/cerrar alertas

2.2 Excluye (NO incluye)
------------------------

- Envio de email → CNST_001 (prohibido)
- Consultas directas a BD IVR → :ref:`arq-mod-004`
- Logica de permisos → :ref:`arq-mod-003`
- Generacion de reportes → :ref:`arq-mod-005`

----

Casos de uso relacionados: :doc:`/requisitos/casos-uso/alerts/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 dependencias
 componentes
 restricciones
 casos-uso
 diagramas/index
