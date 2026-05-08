.. _uc-adm-01-parte-08-diagrama-estados-sod-rule:

8.3 Diagrama de estados — SeparationRule
=========================================

.. uml::
 :caption: SeparationRule — ciclo de vida (BR-009 baja logica).

 @startuml

 [*] --> ACTIVE : create_separation_rule\n(UC_ADM_01)

 ACTIVE --> ACTIVE : update_separation_rule\n(incrementa version)
 ACTIVE --> INACTIVE : disable_separation_rule\n(BR-009 baja logica)
 INACTIVE --> ACTIVE : reactivar\n(PATCH state=ACTIVE)

 note right of ACTIVE
   Estado operativo.
   El EvaluatorReloader la
   incluye en el catalogo
   activo de validacion.
 end note

 note right of INACTIVE
   Soft delete (BR-009).
   La regla no se borra fisicamente.
   El catalogo activo no la incluye
   pero queda en audit log.
   Reactivable.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/separation-rule`.
 - :doc:`/requisitos/reglas-negocio/br-007-separacion-de-funciones`
   (BR-007 SoD).
 - :doc:`/requisitos/reglas-negocio/br-009-bajas-logicas`
   (semantica soft delete).
