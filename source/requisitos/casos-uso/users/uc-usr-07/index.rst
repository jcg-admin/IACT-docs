.. meta::
 :artefacto: UC_USR_07
 :tipo: Caso de Uso (Spec Completa)
 :dominio: requisitos
 :subdominio: casos_uso/users
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Importante
 :normativa: CNST-009, CNST-013, CNST-025, CNST-026

.. _uc-usr-07:

==================================
UC_USR_07 — Editar Perfil Propio
==================================

.. note::

 **Especificacion completa de 12 partes** — promocion del
 placeholder Reservado a spec Aprobada por el WP
 ``2026-05-08-04-10-27-uc-view-domain-alignment``.

Resumen
=======

UC_USR_07 permite que un User autenticado edite **campos
editables de su propio perfil**: ``full_name``, ``email``
(opcionalmente). NO toca atributos sensibles como
``primary_access_group_id``, ``segment_id`` o ``state`` —
esos requieren UC_USR_03 (modificacion administrativa).

UC_USR_07 es **self-service**: el actor es el propio
User; no hay admin involucrado. La capability
``edit_own_profile`` es asignacion default a TODOS los
Users activos del sistema (todo User puede editarse a si
mismo).

Distinto de:

- **UC_USR_03**: modificacion**administrativa** por un
  admin sobre **otro** User. Permite cambiar atributos
  sensibles.
- **UC_AUTH_03**: reset de password — credencial,
  no perfil.

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_USR_07
 * - **Modulo**
   - MOD_Users
 * - **Criticidad**
   - MEDIA (afecta presentacion del User pero no
     privilegios)
 * - **Complejidad**
   - BAJA (1 dia)
 * - **Actor Principal**
   - Cualquier User autenticado con funcion
     ``edit_own_profile``
 * - **Funcion RBAC**
   - ``edit_own_profile`` (asignacion default a todos los
     Users activos)
 * - **BReq satisfecho**
   - BReq-002 (Experiencia de Usuario) + BReq-004
     (auditoria del cambio)

Documentos vinculados
=====================

- :doc:`/requisitos/casos-uso/users/uc-usr-03/index`
  (modificacion administrativa — campos sensibles)
- :doc:`/requisitos/casos-uso/auth/uc-auth-04/index`
  (cambiar password — credencial, scope distinto)

Estructura de la spec
=====================

.. toctree::
 :maxdepth: 1
 :caption: Las 12 partes

 informacion-general
 actores-precondiciones
 flujo-principal
 flujos-alternos
 excepciones
 requisitos-no-funcionales
 datos-involucrados
 diagramas-uml/index
 criterios-aceptacion
 patrones-diseno
 implementacion-tecnica
 testing
