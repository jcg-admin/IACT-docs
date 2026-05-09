.. meta::
 :artefacto: ARQ-MOD-003
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-003:

====================================================
ARQ_MOD_003: Roles, Segmentos y Permisos (RBAC_CORE)
====================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo RBAC_CORE es el **nucleo de control de acceso** del sistema IACT.
Define roles, permisos, segmentos de datos, y calcula los permisos efectivos
de cada usuario.

**Pregunta clave que responde:**

 *"¿Que puede hacer este usuario en este modulo, sobre que datos?"*

**Incluye enforcers de seguridad** (lo que antes era SEC_RULES) como
validaciones internas del RBAC.

----

2. Alcance
==========

2.1 Incluye
-----------

- Catalogo de roles funcionales (R001-R017)
- Catalogo de permisos (view, export, create, edit, delete, etc.)
- Segmentos de datos (por centro, servicio, region)
- Calculo de permisos efectivos (precedencia: Directo > Rol > Segmento)
- Reglas de Separacion (Separation of Duties — conflicto entre roles)
- Simulacion de acceso ("¿que veria este usuario?")
- Matriz consolidada de roles/permisos (vista PMO)
- **Enforcers de seguridad** (middleware, decoradores, policies)

2.2 Excluye (NO incluye)
------------------------

- Autenticacion (login/logout) → :ref:`arq-mod-001`
- Gestion de datos de usuario → :ref:`arq-mod-002`
- UI de reportes/dashboards → :ref:`arq-mod-005`
- Logica de negocio IVR → :ref:`arq-mod-005`

----

Casos de uso relacionados:
:doc:`/requisitos/casos-uso/access/index` ·
:doc:`/requisitos/casos-uso/permissions/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 enforcers
 dependencias
 componentes
 restricciones
 diagramas/index
