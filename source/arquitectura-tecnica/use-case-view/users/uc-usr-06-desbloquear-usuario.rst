.. meta::
 :artefacto: AT_UC_USR_06_USECASE
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
 :origen: incierto — referenciado en uc-auth-03/04
          sin decision arquitectonica formal documentada

.. _at_uc_usr_06_desbloquear_usuario:

==============================================
UC_USR_06 — Desbloquear Usuario (RESERVADO)
==============================================

.. warning::

   **UC en estado Reservado — sin diagrama hasta ADR formal.**

   Spec textual stub disponible en
   :doc:`/requisitos/casos-uso/users/uc-usr-06/index`.

   Counterpart de UC_USR_05. Aparece referenciado en
   uc-auth-03 y uc-auth-04 pero **nunca tuvo commit de
   creacion** (verificado en WP
   ``2026-05-07-04-08-13-use-case-view-analysis``). La
   decision arquitectonica formal sobre scope, capability
   RBAC y flujo de reactivacion esta pendiente.

   El diagrama uml-07 standalone se generara cuando un ADR
   formalice junto con UC_USR_05:

   - Capability RBAC (candidatos: ``unblock_users`` o
     ``activate_users``).
   - Si el desbloqueo limpia contador de intentos fallidos
     (BR-015) automaticamente.
   - Si requiere notificacion al usuario afectado.
   - Si requiere reset de password al desbloquear.

.. seealso::

 - :doc:`/requisitos/casos-uso/users/uc-usr-06/index` —
   stub con resumen propuesto + decision pendiente.
 - :doc:`/arquitectura-tecnica/use-case-view/users/uc-usr-05-bloquear-usuario` —
   counterpart simetrico.
 - :doc:`/requisitos/reglas-negocio/br-015-bloqueo-intentos-fallidos` —
   BR relacionada (limpieza de contador al desbloquear).
