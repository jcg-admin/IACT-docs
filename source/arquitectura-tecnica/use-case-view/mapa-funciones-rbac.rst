.. meta::
 :artefacto: AT_UC_MAPA_FUNCIONES_RBAC
 :tipo: Diagrama Arquitectonico — Mapa Funciones RBAC
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_uc_mapa_funciones_rbac:

============================
Mapa de Funciones RBAC IACT
============================

.. note::

   **Sin jerarquía de actores.** Per ``BR-006 RBAC Flat
   NIST`` y ``CNST-005`` el sistema NO tiene herencia
   entre roles. Lo único que distingue a un usuario de
   otro es **el conjunto de funciones efectivas** que
   tiene asignadas (directa o vía agrupador).

   Este diagrama reemplaza la antigua "jerarquía de
   actores" (que asumía herencia tipo
   ``User <|-- Operator <|-- Supervisor``) por un mapa
   **plano y función-céntrico** alineado con el modelo
   IACT real. Para nosotros importan las **funciones**,
   no los títulos.

.. uml::
 :caption: Mapa RBAC IACT — funciones (atomicas) →
           agrupadores (AGR) → usuarios. Modelo plano sin
           herencia.

 @startuml

 left to right direction

 actor User

 package "Catálogo de Funciones (CNST-033 §5)" {
   rectangle "MOD_Auth" {
     usecase "manage_sessions" as f_auth_001
     usecase "close_user_session" as f_auth_002
     usecase "reset_password" as f_auth_003
     usecase "view_active_sessions" as f_auth_004
   }
   rectangle "MOD_Reports" {
     usecase "view_reports" as f_rpt_001
     usecase "view_dashboard" as f_rpt_002
     usecase "view_kpis" as f_rpt_007
     usecase "export_csv" as f_rpt_004
     usecase "schedule_report" as f_rpt_xxx
   }
   rectangle "MOD_Access" {
     usecase "assign_functions" as f_acc_001
     usecase "revoke_functions" as f_acc_002
     usecase "view_assignments" as f_acc_003
     usecase "manage_separation_rules" as f_acc_005
   }
   rectangle "MOD_Audit" {
     usecase "view_audit_log" as f_aud_001
     usecase "search_audit_log" as f_aud_002
     usecase "export_audit_log" as f_aud_003
   }
 }

 package "Agrupadores (CNST-033 §6)" {
   rectangle "AGR-001\nbasic_operator_group" as AGR001
   rectangle "AGR-002\nreport_viewer_group" as AGR002
   rectangle "AGR-007\npermission_admin_group" as AGR007
   rectangle "AGR-008\nauditor_group" as AGR008
   rectangle "AGR-010\nsystem_admin_group" as AGR010
 }

 AGR001 ..> f_rpt_001 : <<contains>>
 AGR001 ..> f_rpt_002 : <<contains>>
 AGR002 ..> f_rpt_001 : <<contains>>
 AGR002 ..> f_rpt_004 : <<contains>>
 AGR002 ..> f_rpt_007 : <<contains>>
 AGR007 ..> f_acc_001 : <<contains>>
 AGR007 ..> f_acc_002 : <<contains>>
 AGR007 ..> f_acc_005 : <<contains>>
 AGR008 ..> f_aud_001 : <<contains>>
 AGR008 ..> f_aud_002 : <<contains>>
 AGR008 ..> f_aud_003 : <<contains>>

 User --> AGR001
 User --> AGR002
 User --> AGR007
 User --> AGR008
 User --> AGR010

 note bottom of User
   Sin titulos.
   Sin herencia entre roles.
   Lo unico que define al
   usuario es su effective_set
   = union de funciones de sus AGRs.
 end note

 note right of AGR010
   AGR-010 system_admin_group
   contiene TODAS las funciones
   del catalogo (superuser flat,
   no heredado).
 end note

 @enduml

Modelo conceptual
=================

Per **BR-006 NIST RBAC Flat** y**CNST-005**:

1. **Funciones** son las unidades atómicas de
   autorización. Tienen ``codename`` (snake_case en
   inglés, CNST-033 §3.1) y un ``function_id`` opcional
   (formato ``MODULO-NNN``) para trazabilidad
   documental.

2. **Agrupadores** (``FunctionGroup``, AGR-NNN) son
   colecciones de funciones. La asignación de un
   agrupador a un usuario equivale a asignar todas las
   funciones del agrupador.

3. **User** se asigna a 0..N agrupadores y/o tiene 0..N
   permisos excepcionales (``ExceptionalPermission``)
   con rango temporal (CNST-031).

4. **effective_set** del usuario =
   ⋃ funciones de sus agrupadores activos ∪
   permisos excepcionales activos.

5. **NO hay herencia entre roles**. El "Supervisor" de
   negocio NO hereda del "Operator" — son etiquetas de
   recursos humanos. En el sistema, un usuario
   etiquetado como Supervisor simplemente tiene
   asignados más agrupadores (AGR-002 + AGR-003 +
   AGR-004 + AGR-005) que el Operator (AGR-001).

6. **Verificación** de un permiso usa el codename de
   función (no el AGR ni el título):
   ``check(user_id, "view_reports")`` retorna ``true``
   si ``view_reports ∈ effective_set(user_id)``.

Implementación en domain-model
==============================

- :doc:`/arquitectura-tecnica/domain-model/function`
  — entidad atómica.
- :doc:`/arquitectura-tecnica/domain-model/function-group`
  — agrupador (FunctionGroup, AGR-NNN).
- :doc:`/arquitectura-tecnica/domain-model/access-group`
  — vista alternativa del agrupador.
- :doc:`/arquitectura-tecnica/domain-model/access-group-function`
  — clase de asociación que materializa "AGR contiene
  Function".
- :doc:`/arquitectura-tecnica/domain-model/assignment`
  / :doc:`/arquitectura-tecnica/domain-model/assignment-repo`
  — asignación de AGR a User.
- :doc:`/arquitectura-tecnica/domain-model/exceptional-permission`
  / :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo`
  — concesiones temporales.
- :doc:`/arquitectura-tecnica/domain-model/permission-service`
  — verificación canónica.
- :doc:`/arquitectura-tecnica/domain-model/permission-cache`
  — cache TTL con invalidación dirigida.
- :doc:`/arquitectura-tecnica/domain-model/rbac-repo`
  — repositorio de consultas agregadas.
- :doc:`/arquitectura-tecnica/domain-model/separation-rule`
  — reglas de separacion (CNST-005).

.. seealso::

 :doc:`/requisitos/reglas-negocio/br-006-rbac-flat-nist`
 :doc:`/normativa/restricciones/cnst-033-vocabulario-unificado-rbac`
 :doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones`
 :doc:`/requisitos/reglas-negocio/rbac/grupos-funciones`
 :doc:`/requisitos/reglas-negocio/rbac/separacion-de-deberes`
