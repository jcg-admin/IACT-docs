.. meta::
 :artefacto: AT_UC_MOD_ADMIN
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 3.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_admin:

=========================================================
MOD_Admin — Administracion del Modelo RBAC: UC por Modulo
=========================================================

.. note:: Modulo NUEVO en RBAC v5.6.0 — extendido en v5.6.x

 MOD_Admin es uno de los **9 modulos in-scope** del modelo RBAC
 v5.6.0 (3 UCs baseline) extendido a 5 UCs en v5.6.x con la
 incorporacion de UC_ADM_04 y UC_ADM_05 (gestion del catalogo y
 lifecycle de ``MenuItem``, WP
 ``2026-05-06-21-42-06-menu-rbac-user-scope-docs``).
 Formaliza el plano de configuracion del modelo RBAC que en
 versiones anteriores estaba implicito en MOD_Access y
 MOD_Permissions. Ver
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index` y
 :doc:`/requisitos/casos-uso/admin/index`.

MOD_Admin — Administracion del Modelo RBAC
===========================================

Plano de **configuracion del modelo RBAC**: gestiona QUE funciones,
grupos del sistema y reglas SoD EXISTEN — anterior e independiente de
a quien se asignan (:doc:`/arquitectura-tecnica/use-case-view/access/index`) o de como se verifican en runtime
(:doc:`/arquitectura-tecnica/use-case-view/permissions/index`).

**Actor principal:** ``SystemAdmin`` (AGR-010).

**Diferencia clave con MOD_Access y MOD_Permissions:**

- MOD_Admin opera sobre el **modelo** (que elementos RBAC existen).
- MOD_Access opera sobre **asignaciones** (quien tiene que elementos).
- MOD_Permissions opera sobre **verificacion** (tiene permiso ahora?).

.. uml::
 :caption: MOD_Admin v5.6.x — SystemAdmin gestiona 5 catalogos
           del modelo RBAC. UC_ADM_04 y UC_ADM_05 son extension
           v5.6.x para el catalogo UX persistido (MenuItem).

 @startuml
 left to right direction

 actor SystemAdmin
 actor Auditor
 actor "Planificador\nde Tareas" as PlanificadorTareas

 rectangle "MOD_Admin" {
   usecase "UC_ADM_01\nGestionar Ciclo\nde Vida de Reglas SoD" as ADM01
   usecase "UC_ADM_02\nGestionar Catalogo\nde Funciones" as ADM02
   usecase "UC_ADM_03\nGestionar Catalogo\nde Agrupadores del Sistema" as ADM03
   usecase "UC_ADM_04\nGestionar Catalogo\nde MenuItems\n(v5.6.x)" as ADM04
   usecase "UC_ADM_05\nGestionar Lifecycle\nde MenuItem\n(v5.6.x)" as ADM05
 }

 SystemAdmin --> ADM01
 SystemAdmin --> ADM02
 SystemAdmin --> ADM03
 SystemAdmin --> ADM04
 SystemAdmin --> ADM05

 Auditor --> ADM01
 Auditor --> ADM02
 Auditor --> ADM03
 Auditor --> ADM04
 Auditor --> ADM05

 PlanificadorTareas --> ADM05 : auto_archive_menu_items\n(actor=system)

 ADM05 ..> ADM04 : <<requires>>\nMenuItem creado

 note right of MOD_Admin
   Codenames RBAC v5.6.x (6 funciones):
   v5.6.0 baseline:
     SystemAdmin (AGR-010) →
       view_separation_rules,
       create_separation_rule,
       update_separation_rule,
       disable_separation_rule,
       manage_function_catalog,
       assign_functions_to_group
   v5.6.x extension (is_critical=True):
     SystemAdmin (AGR-010) →
       manage_menu_catalog (UC_ADM_04),
       manage_menu_lifecycle (UC_ADM_05)
     manage_critical_function_flag:
       SIN TITULAR (TD-RBAC-03,
       gobernanza via migration)
   Auditor (AGR-008) → view_* (read-only)
   Toda escritura emite AuditEvent
   de criticidad alta.
 end note

 @enduml

----

Casos de Uso
------------

.. list-table::
 :header-rows: 1
 :widths: 15 30 30 25

 * - UC
   - Nombre
   - Funciones RBAC
   - Notas
 * - UC_ADM_01
   - Gestionar Ciclo de Vida de Reglas SoD
   - ``view_separation_rules``,
     ``create_separation_rule``,
     ``update_separation_rule``,
     ``disable_separation_rule``
   - Consolida las operaciones de configuracion de SoD:
     crear nueva regla, actualizar parametros,
     activar/desactivar. Complementa UC_ACC_05 que
     cubre la vista operativa.
 * - UC_ADM_02
   - Gestionar Catalogo de Funciones
   - ``manage_function_catalog``
   - CRUD sobre las definiciones de funciones atomicas.
     Permite agregar, actualizar o desactivar funciones
     del catalogo sin edicion directa de codigo.
 * - UC_ADM_03
   - Gestionar Catalogo de Agrupadores del Sistema
   - ``assign_functions_to_group``
     (scope: AGR-001..012)
   - Gestiona la composicion de los 12 grupos predefinidos
     del sistema. A diferencia de UC_PERM_05 que crea
     grupos custom, este UC modifica los AGR de sistema
     (inmutables para operadores, mutables solo por SystemAdmin).
 * - UC_ADM_04 (v5.6.x)
   - Gestionar Catalogo de MenuItems
   - ``manage_menu_catalog``
     (``is_critical=True``)
   - CRUD del catalogo de ``MenuItem`` (wrapper UX 1:1
     sobre ``Function``). Maneja metadata visual
     (display_label, icon, route_path, display_order, parent).
     **No** modifica ``status`` (eso es UC_ADM_05).
     Capability con bypass de cache (AP-2b).
 * - UC_ADM_05 (v5.6.x)
   - Gestionar Lifecycle de MenuItem
   - ``manage_menu_lifecycle``
     (``is_critical=True``)
   - State machine de transiciones DRAFT → ACTIVE →
     DEPRECATED → ARCHIVED (5 transiciones validas) +
     gestion del flag ``block_auto_archive``. El
     Planificador de Tareas ejecuta auto-archive a 90d
     con ``actor=system``.

----

Relacion con otros modulos
--------------------------

.. list-table::
 :header-rows: 1
 :widths: 20 80

 * - Modulo
   - Relacion
 * - :doc:`/arquitectura-tecnica/use-case-view/access/index`
   - MOD_Access lee las reglas SoD configuradas por MOD_Admin.
     UC_ACC_05 (ver reglas) consume lo que UC_ADM_01 configura.
 * - :doc:`/arquitectura-tecnica/use-case-view/permissions/index`
   - MOD_Permissions lee el catalogo de funciones para construir
     el effective_set y el menu dinamico.
 * - :doc:`/arquitectura-tecnica/use-case-view/audit/index`
   - Toda operacion de MOD_Admin genera evento de auditoria de
     alta criticidad (cambios al modelo RBAC).

----

Funciones RBAC requeridas
--------------------------

5 funciones nuevas requeridas por este modulo respecto al
catalogo v5.5.0 (2 v5.6.0 baseline + 3 v5.6.x extension):

.. list-table::
 :header-rows: 1
 :widths: 28 12 10 50

 * - Codename
   - Modulo catalogo
   - is_critical
   - Descripcion
 * - ``create_separation_rule``
   - ACC (extend)
   - False
   - Crea nueva regla SoD declarando el par de conjuntos de
     funciones mutuamente excluyentes. Complementa
     ``update_separation_rule`` y ``disable_separation_rule``
     (existentes v5.4.0) para cubrir el ciclo de vida completo.
 * - ``manage_function_catalog``
   - ADM (nueva)
   - False
   - CRUD sobre definiciones de funciones atomicas: nombre,
     descripcion, scope, modulo, estado activo/inactivo. **No**
     incluye el campo ``is_critical`` (gobernanza separada).
 * - ``manage_menu_catalog`` (v5.6.x)
   - ADM (nueva)
   - **True**
   - CRUD del catalogo de ``MenuItem`` wrapper UX. Bypass de
     cache (AP-2b) — strong consistency en cada request.
     ADR-BACK-008.
 * - ``manage_menu_lifecycle`` (v5.6.x)
   - ADM (nueva)
   - **True**
   - Transiciones de estado del ``MenuItem`` y gestion del flag
     ``block_auto_archive``. Bypass de cache. ADR-BACK-008.
 * - ``manage_critical_function_flag`` (v5.6.x)
   - ADM (nueva)
   - **True**
   - Modifica el campo ``Function.is_critical``. **Sin titular
     en v5.6.x** (TD-RBAC-03). Solo via migracion de datos del
     Servicio de Aplicacion con review ≥ 2 aprobaciones.
     Read-only en admin.
     ADR-BACK-010.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

**v5.6.0 baseline:**

- :doc:`/arquitectura-tecnica/domain-model/function` — Function (UC_ADM_02 catálogo + campo ``is_critical`` v5.6.x).
- :doc:`/arquitectura-tecnica/domain-model/function-group` — FunctionGroup (UC_ADM_03).
- :doc:`/arquitectura-tecnica/domain-model/separation-rule` — SeparationRule (UC_ADM_01).
- :doc:`/arquitectura-tecnica/domain-model/audit-event` — AuditEvent (toda escritura emite evento).

**v5.6.x extension (Phase 7 lote C-C):**

- :doc:`/arquitectura-tecnica/domain-model/menu-item` — MenuItem (UC_ADM_04 modelo).
- :doc:`/arquitectura-tecnica/domain-model/menu-item-repo` — MenuItemRepo (queryset visible/for_user).
- :doc:`/arquitectura-tecnica/domain-model/menu-lifecycle-service` — MenuLifecycleService (UC_ADM_05 state machine).
- :doc:`/arquitectura-tecnica/domain-model/user-capability-resolver` — UserCapabilityResolver (resolver con bypass).

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_ADM_01 </requisitos/casos-uso/admin/uc-adm-01/index>`
   - uc-adm-01
   - :doc:`Diagrama </requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_ADM_02 </requisitos/casos-uso/admin/uc-adm-02/index>`
   - uc-adm-02
   - :doc:`Diagrama </requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_ADM_03 </requisitos/casos-uso/admin/uc-adm-03/index>`
   - uc-adm-03
   - :doc:`Diagrama </requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_ADM_04 </requisitos/casos-uso/admin/uc-adm-04/index>`
   - uc-adm-04
   - :doc:`Secuencia </requisitos/casos-uso/admin/uc-adm-04/diagramas-uml/diagrama-de-secuencia>`,
     :doc:`Actividad </requisitos/casos-uso/admin/uc-adm-04/diagramas-uml/diagrama-de-actividad>`
 * - :doc:`UC_ADM_05 </requisitos/casos-uso/admin/uc-adm-05/index>`
   - uc-adm-05
   - :doc:`Estados </requisitos/casos-uso/admin/uc-adm-05/diagramas-uml/diagrama-de-estados>`,
     :doc:`Secuencia </requisitos/casos-uso/admin/uc-adm-05/diagramas-uml/diagrama-de-secuencia>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`

UC standalone uml-07
====================

Diagramas standalone uml-07 por UC (auto-explicativos):

.. toctree::
 :maxdepth: 1

 uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod
 uc-adm-02-gestionar-catalogo-de-funciones
 uc-adm-03-gestionar-catalogo-de-agrupadores-del-sistema
 uc-adm-04-gestionar-catalogo-menuitems
 uc-adm-05-gestionar-lifecycle-menuitem
