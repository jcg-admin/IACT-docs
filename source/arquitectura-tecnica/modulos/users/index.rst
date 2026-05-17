.. meta::
 :artefacto: ARQ-MOD-002
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/users
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-002:

===================================================
ARQ_MOD_002: Gestion de Identidades (USER_IDENTITY)
===================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo USER_IDENTITY gestiona el **ciclo de vida de las cuentas de usuario**:
alta, modificacion, baja logica, y datos de perfil.

**Pregunta clave que responde:**

 *"¿Que usuarios existen y con que atributos/relaciones?"*

**NO responde:** *"¿Que pueden hacer?"* — Eso es :ref:`arq-mod-003`.

----

2. Alcance
==========

2.1 Incluye
-----------

- Alta de usuarios (username autogenerado, estado PENDIENTE_CONFIGURACION)
- Modificacion de datos basicos (nombre, apellidos, unidad organizacional)
- Baja logica de usuarios (deleted_at, deleted_by, conservar para auditoria)
- Gestion de preguntas de seguridad (minimo 3 preguntas)
- Consulta de perfil de usuario
- Asociacion usuario-roles como **relacion** (no como logica)

2.2 Excluye (NO incluye)
------------------------

- Calculo de permisos efectivos → :ref:`arq-mod-003`
- Definicion de catalogos de roles/permisos → :ref:`arq-mod-003`
- Validacion de separacion (conflicto de roles) → :ref:`arq-mod-003`
- Autenticacion (login/logout) → :ref:`arq-mod-001`

----

Casos de uso relacionados: :doc:`/requisitos/casos-uso/users/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 dependencias
 componentes
 restricciones
 diagramas/index
