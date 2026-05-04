8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "admin_sistema\n(AGR-009)" as admin
 rectangle "MOD_Admin — UC_ADM_02" {
   usecase "Crear funcion\nmanage_function_catalog" as Create
   usecase "Actualizar funcion\nmanage_function_catalog" as Update
   usecase "Desactivar funcion\nmanage_function_catalog" as Deactivate
   usecase "Listar funciones\nmanage_function_catalog" as List
   usecase "Reload\nPermissionsEngine" as Reload
 }
 admin --> Create
 admin --> Update
 admin --> Deactivate
 admin --> List
 Create ..> Reload : <<include>>
 Update ..> Reload : <<include>>
 Deactivate ..> Reload : <<include>>
 @enduml
