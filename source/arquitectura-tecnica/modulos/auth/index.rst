.. meta::
 :artefacto: ARQ-MOD-001
 :tipo: Modulo Arquitectonico
 :dominio: arquitectura-tecnica
 :subdominio: modulos/auth
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2025-12-22
 :ultimo_cambio: 2026-05-02
 :autor: NestorMonroy
 :clasificacion: Critico

.. _arq-mod-001:

============================================
ARQ_MOD_001: Autenticacion y Sesiones (AUTH)
============================================

.. contents:: Contenido
 :local:
 :depth: 1

----

1. Proposito
============

El modulo AUTH gestiona la **autenticacion de usuarios** y el **ciclo de vida
de las sesiones** en el sistema IACT.

**Pregunta clave que responde:**

 *"¿Quien eres? ¿Tu sesion es valida?"*

Este modulo es el punto de entrada al sistema. Valida credenciales, genera
tokens de autenticación, gestiona sesiones en base de datos, y controla el timeout de
inactividad.

**Lo demas lo decide:** :ref:`arq-mod-003` (permisos y accesos).

----

2. Alcance
==========

2.1 Incluye
-----------

- Login de usuario (validacion de credenciales)
- Logout del sistema (invalidacion de sesion)
- Generacion y validacion de tokens de autenticación
- Gestion de refresh tokens
- Sesion unica por usuario (CNST_002)
- Timeout de sesion por inactividad (15 minutos)
- Validacion de IP + User-Agent
- Recuperacion de contrasena via preguntas de seguridad
- Cambio de contrasena

2.2 Excluye (NO incluye)
------------------------

- Definicion de roles y permisos → :ref:`arq-mod-003`
- Validacion de que puede hacer el usuario → :ref:`arq-mod-003`
- Gestion de datos del usuario → :ref:`arq-mod-002`
- Alertas por intentos fallidos → :ref:`arq-mod-006`
- Registro de eventos de login/logout → :ref:`arq-mod-007`

----

Casos de uso relacionados: :doc:`/requisitos/casos-uso/auth/index`

.. toctree::
 :maxdepth: 1
 :caption: Especificacion

 responsabilidades
 dependencias
 componentes
 restricciones
 casos-uso
 diagramas
