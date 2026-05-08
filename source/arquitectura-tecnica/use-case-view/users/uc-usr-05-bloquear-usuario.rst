.. meta::
 :artefacto: AT_UC_USR_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: users
 :estado: Reservado
 :version: 0.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno
 :origen: incierto — referenciado en uc-auth-03/04/05
          sin decision arquitectonica formal documentada

.. _at_uc_usr_05_bloquear_usuario:

==============================================
UC_USR_05 — Bloquear Usuario (RESERVADO)
==============================================

.. warning::

   **UC en estado Reservado — sin diagrama hasta ADR formal.**

   Spec textual stub disponible en
   :doc:`/requisitos/casos-uso/users/uc-usr-05/index`.

   Origen incierto: el UC esta referenciado en uc-auth-03,
   uc-auth-04 y uc-auth-05 pero **nunca tuvo commit de
   creacion** (verificado en WP
   ``2026-05-07-04-08-13-use-case-view-analysis``). La
   decision arquitectonica formal sobre scope, capability
   RBAC y relacion con BR-015 (Bloqueo Intentos Fallidos)
   esta pendiente.

   El diagrama uml-07 standalone se generara cuando un ADR
   formalice:

   - Si es bloqueo administrativo manual, automatico por
     intentos fallidos, o ambos.
   - La capability RBAC asociada (candidatos:
     ``block_users`` o ``deactivate_users`` ya existente).
   - Si la funcionalidad ya esta cubierta por
     ``deactivate_users`` (UC_USR_03 + BR-009 baja logica) y
     este UC es redundante.

.. seealso::

 - :doc:`/requisitos/casos-uso/users/uc-usr-05/index` —
   stub con resumen propuesto + decision pendiente.
 - :doc:`/requisitos/casos-uso/users/index` —
   seccion "UCs Reservados".
 - :doc:`/requisitos/reglas-negocio/br-015-bloqueo-intentos-fallidos` —
   BR relacionada (semantica diferente: automatica por
   sistema).
