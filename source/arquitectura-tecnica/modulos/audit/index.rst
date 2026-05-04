.. meta::
 :artefacto: ARQ-MOD-007
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/audit
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-007:

========================================
ARQ_MOD_007: Auditoria Funcional (AUDIT)
========================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo AUDIT registra **acciones de negocio** realizadas por los usuarios
en el sistema. Es la bitacora funcional para cumplimiento y gobernanza.

**Pregunta clave que responde:**

 *"¿Que acciones de negocio relevantes se hicieron en el sistema?"*

**NO es un log tecnico** — eso es :ref:`arq-mod-008`.

----

2. Alcance
==========

2.1 Incluye
-----------

**Eventos auditados:**

- Login/logout de usuarios
- Creacion y modificacion de usuarios
- Asignacion y retiro de roles
- Cambios de segmentos de datos
- Exportaciones de reportes
- Cambios de configuracion de alertas
- Cambios de contrasena
- Intentos de acceso fallidos

**Funcionalidades:**

- Consultar bitacora de auditoria
- Filtrar por usuario, fecha, recurso, tipo de accion
- Exportar eventos de auditoria
- Generar reportes de cambios de permisos

2.2 Excluye (NO incluye)
------------------------

- Stack traces y errores tecnicos → :ref:`arq-mod-008`
- Logs de infraestructura → :ref:`arq-mod-008`
- Definir reglas de acceso → :ref:`arq-mod-003`

----

Casos de uso relacionados: :doc:`/requisitos/casos-uso/audit/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 dependencias
 componentes
 restricciones
 retencion
 diagramas/index
