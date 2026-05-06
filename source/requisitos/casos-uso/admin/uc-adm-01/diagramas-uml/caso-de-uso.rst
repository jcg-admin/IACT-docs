8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "system_admin\n(AGR-010)" as admin
 rectangle "MOD_Admin — UC_ADM_01" {
   usecase "Crear regla SoD\ncreate_separation_rule" as Create
   usecase "Actualizar regla\nupdate_separation_rule" as Update
   usecase "Ver reglas\nview_separation_rules" as View
   usecase "Desactivar regla\ndisable_separation_rule" as Disable
   usecase "Reload\nEnforcementEngine" as Reload
 }
 admin --> Create
 admin --> Update
 admin --> View
 admin --> Disable
 Create ..> Reload : <<include>>
 Update ..> Reload : <<include>>
 Disable ..> Reload : <<include>>
 @enduml
