.. meta::
 :artefacto: UC_USR_06
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

.. _uc-usr-06:

================================
UC_USR_06 — Desbloquear Usuario
================================

.. note::

 **Especificacion completa de 12 partes** — promocion del
 placeholder Reservado a spec Aprobada por el WP
 ``2026-05-08-04-10-27-uc-view-domain-alignment``.

Resumen
=======

UC_USR_06 ejecuta el **desbloqueo administrativo** de un
User previamente bloqueado. Transicion
``User.state: BLOCKED → ACTIVE`` y emision de AuditEvent
``USER_UNBLOCKED`` con referencia al evento de bloqueo
original. La cuenta queda restaurada a operacion normal:
puede iniciar sesion nuevamente; los Assignments y
permisos preservados durante el bloqueo se reactivan.

Es la **operacion inversa** de UC_USR_05 y tambien aplica
a desbloquear cuentas que fueron bloqueadas
automaticamente por BR-015 (admin desbloquea tras
verificar que el bloqueo automatico no fue por
credencial comprometida).

Distinto de:

- **UC_USR_03 (modificar)** — modificacion de atributos
  generales sin cambio de state.
- **UC_USR_04 (eliminar)** — terminal, NO reversible.
  ELIMINATED no se desbloquea.

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **ID**
   - UC_USR_06
 * - **Modulo**
   - MOD_Users
 * - **Criticidad**
   - ALTA (restaura acceso al sistema)
 * - **Complejidad**
   - BAJA (1 dia)
 * - **Actor Principal**
   - User con funcion ``unblock_users``
 * - **Funcion RBAC**
   - ``unblock_users``
 * - **BReq satisfecho**
   - BReq-004 (Cumplimiento de Seguridad y Auditoria)

Documentos vinculados
=====================

- :doc:`/requisitos/business-requirements/breq-004-cumplimiento-seguridad-auditoria`
- :doc:`/requisitos/casos-uso/users/uc-usr-05/index`
  (bloqueo manual — operacion inversa)
- :doc:`/requisitos/reglas-negocio/br-015-bloqueo-intentos-fallidos`
  (bloqueo automatico — UC_USR_06 tambien lo desbloquea)
- :doc:`/requisitos/casos-uso/auth/uc-auth-01/index`
  (login — recupera capacidad tras unblock)

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
