.. meta::
 :artefacto: AT_UC_USR_07_USECASE
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
 :origen: incierto — referenciado en users/uc-usr-02
          sin decision arquitectonica formal documentada

.. _at_uc_usr_07_editar_perfil_propio:

==============================================
UC_USR_07 — Editar Perfil Propio (RESERVADO)
==============================================

.. warning::

   **UC en estado Reservado — sin diagrama hasta ADR formal.**

   Spec textual stub disponible en
   :doc:`/requisitos/casos-uso/users/uc-usr-07/index`.

   Distinto de UC_USR_02 (admin edita usuarios con capability
   ``edit_users``): este UC permitiria al usuario autenticado
   editar su **propio perfil** (capability self-served, sin
   RBAC administrativo).

   El UC esta referenciado en
   ``users/uc-usr-02/informacion-general.rst`` pero **nunca
   tuvo commit de creacion** (verificado en WP
   ``2026-05-07-04-08-13-use-case-view-analysis``). La
   decision arquitectonica formal sobre scope esta pendiente.

   El diagrama uml-07 standalone se generara cuando un ADR
   formalice:

   - Que campos son editables por el propio usuario vs
     cuales requieren admin (UC_USR_02).
   - Si la capability ``edit_own_profile`` es self-served
     (auto-otorgada como ``view_own_*``) o requiere
     asignacion explicita.
   - Auditabilidad: si toda edicion del perfil propio
     genera audit event.

   **Explicitamente NO incluido en UC_USR_07:**

   - Cambio de password (UC_AUTH_03 / UC_AUTH_04).
   - Cambio de username (potencial impacto en audit log).
   - Cambio de ``segment_id`` (BR-012 — permanente).
   - Cambio de AGRs / capabilities (UC_PERM_01..06).

.. seealso::

 - :doc:`/requisitos/casos-uso/users/uc-usr-07/index` —
   stub con resumen propuesto + decision pendiente.
 - :doc:`/arquitectura-tecnica/use-case-view/users/uc-usr-02-modificar-usuario` —
   contraparte administrativa (admin edita usuarios).
 - :doc:`/arquitectura-tecnica/use-case-view/auth/uc-auth-03-recuperar-contrasena` —
   cambio de password (out-of-scope de este UC).
 - :doc:`/arquitectura-tecnica/use-case-view/auth/uc-auth-04-cambiar-contrasena` —
   cambio de password (out-of-scope de este UC).
