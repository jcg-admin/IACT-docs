.. _uc-adm-02-parte-08-diagrama-estados-funcion:

8.3 Diagrama de estados — Function
===================================

.. uml::
 :caption: Function — ciclo de vida (BR-009 baja logica).

 @startuml

 [*] --> ACTIVE : create_function\n(via UC_ADM_02)

 ACTIVE --> ACTIVE : update_function\n(description, scope, name)
 ACTIVE --> INACTIVE : deactivate_function\n(BR-009 baja logica)
 INACTIVE --> ACTIVE : reactivate\n(PATCH is_active=True)

 note right of ACTIVE
   is_active=True. La Function es
   asignable a AccessGroup (via
   FunctionGroupMembership) y
   verificable por
   UserCapabilityResolver.
 end note

 note right of INACTIVE
   is_active=False (soft delete).
   La Function NO se borra
   fisicamente. Las asignaciones
   existentes se preservan pero
   la verificacion las filtra
   (AND f.is_active=True en query).
 end note

 note bottom
   El campo is_critical NO se
   modifica desde este UC.
   Cambios al flag solo via
   data migration (ADR-BACK-010,
   capability separada
   manage_critical_function_flag
   sin titular runtime).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/function`.
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`.
 - :doc:`/backend/adr-back-010-function-is-critical-governance`.
