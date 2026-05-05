.. meta::
 :artefacto: AT_UC_MOD_ADMIN
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_admin:

=========================================================
MOD_Admin — Administracion del Modelo RBAC: UC por Modulo
=========================================================

MOD_Admin — Administracion del Modelo RBAC
===========================================

Plano de **configuracion del modelo RBAC**: gestiona QUE funciones,
grupos del sistema y reglas SoD EXISTEN — anterior e independiente de
a quien se asignan (:doc:`uc-access`) o de como se verifican en runtime
(:doc:`uc-permissions`).

**Actor principal:** ``SystemAdmin`` (AGR-010).

**Diferencia clave con MOD_Access y MOD_Permissions:**

- MOD_Admin opera sobre el **modelo** (que elementos RBAC existen).
- MOD_Access opera sobre **asignaciones** (quien tiene que elementos).
- MOD_Permissions opera sobre **verificacion** (tiene permiso ahora?).

.. uml::
 :caption: MOD_Admin — SystemAdmin gestiona los 3 catálogos
           del modelo RBAC.

 @startuml
 left to right direction

 actor SystemAdmin
 actor Auditor

 rectangle "MOD_Admin" {
   usecase "UC_ADM_01\nGestionar Ciclo\nde Vida de Reglas SoD" as ADM01
   usecase "UC_ADM_02\nGestionar Catalogo\nde Funciones" as ADM02
   usecase "UC_ADM_03\nGestionar Catalogo\nde Agrupadores del Sistema" as ADM03
 }

 SystemAdmin --> ADM01
 SystemAdmin --> ADM02
 SystemAdmin --> ADM03

 Auditor --> ADM01
 Auditor --> ADM02
 Auditor --> ADM03

 note right of MOD_Admin
   Codenames RBAC:
     SystemAdmin (AGR-010) →
       view_separation_rules,
       create_separation_rule,
       update_separation_rule,
       disable_separation_rule,
       manage_function_catalog,
       assign_functions_to_group
     Auditor (AGR-008) → view_* (read-only)
   Toda escritura de MOD_Admin emite
   AuditEvent de criticidad alta.
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

----

Relacion con otros modulos
--------------------------

.. list-table::
 :header-rows: 1
 :widths: 20 80

 * - Modulo
   - Relacion
 * - :doc:`uc-access`
   - MOD_Access lee las reglas SoD configuradas por MOD_Admin.
     UC_ACC_05 (ver reglas) consume lo que UC_ADM_01 configura.
 * - :doc:`uc-permissions`
   - MOD_Permissions lee el catalogo de funciones para construir
     el effective_set y el menu dinamico.
 * - :doc:`uc-audit`
   - Toda operacion de MOD_Admin genera evento de auditoria de
     alta criticidad (cambios al modelo RBAC).

----

Funciones RBAC requeridas
--------------------------

Dos funciones nuevas requeridas por este modulo (no existen en
el catalogo v5.5.0 actual):

.. list-table::
 :header-rows: 1
 :widths: 30 15 55

 * - Codename
   - Modulo catalogo
   - Descripcion
 * - ``create_separation_rule``
   - ACC (extend)
   - Crea nueva regla SoD declarando el par de conjuntos de
     funciones mutuamente excluyentes. Complementa
     ``update_separation_rule`` y ``disable_separation_rule``
     (existentes v5.4.0) para cubrir el ciclo de vida completo.
 * - ``manage_function_catalog``
   - ADM (nueva)
   - CRUD sobre definiciones de funciones atomicas: nombre,
     descripcion, scope, modulo, estado activo/inactivo.
     Requiere migracion de datos y control de versiones del
     catalogo.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/function` — Function (UC_ADM_02 catálogo).
- :doc:`/arquitectura-tecnica/domain-model/function-group` — FunctionGroup (UC_ADM_03).
- :doc:`/arquitectura-tecnica/domain-model/separation-rule` — SeparationRule (UC_ADM_01).
- :doc:`/arquitectura-tecnica/domain-model/audit-event` — AuditEvent (toda escritura emite evento).

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/normativa/gobernanza/adr-gob-008-rbac-coexistencia-acc-perm`
