.. meta::
 :artefacto: UC_ADM_05_STATE
 :tipo: Diagrama UML
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

8.1 Diagrama de Estados — MenuItem Lifecycle
=============================================

.. uml::

   @startuml

   [*] --> DRAFT : crear (UC_ADM_04)

   DRAFT --> ACTIVE : publicar
   DRAFT --> DRAFT : editar metadata UX (UC_ADM_04)

   ACTIVE --> DEPRECATED : deprecar
   ACTIVE --> ACTIVE : editar metadata UX (UC_ADM_04)

   DEPRECATED --> ACTIVE : reactivar
   DEPRECATED --> ARCHIVED : archivar manual
   DEPRECATED --> ARCHIVED : auto-archive 90d\n(si NOT block_auto_archive)

   ARCHIVED --> ACTIVE : reactivar
   ARCHIVED --> [*] : (sin terminal real,\nlos items se conservan)

   note right of DEPRECATED
     deprecated_at = now() en entrada.
     Warning a 30d, 80d.
     Auto-archive a 90d si !block.
     block_auto_archive=True
       requiere block_reason >=20ch
       y block_set_by + audit log.
   end note

   note right of ARCHIVED
     archived_at = now() en entrada.
     deprecated_at preservado.
     Invisible en GET /api/v1/menu/.
     Capability sigue accesible
     via URL directa.
   end note

   note left of ACTIVE
     deprecated_at = NULL.
     archived_at = NULL.
     block_* limpiados al
     entrar a ACTIVE.
   end note

   @enduml
