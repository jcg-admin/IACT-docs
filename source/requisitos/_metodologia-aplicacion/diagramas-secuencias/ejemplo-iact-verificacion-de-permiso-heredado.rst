9.1 Ejemplo IACT — verificación de permiso heredado
---------------------------------------------------

UC_PERM_07: una macro-función puede implicar otras (catálogo
con relaciones reflexivas, ver
:doc:`relaciones-uml` § 5.2). El verificador recursivo debe
expandir cada función hasta llegar a las atómicas.

.. uml::

   @startuml

   participant ":SecRules"  as SecRules
   participant ":BDAnalytics" as BDAnalytics

   [-> SecRules : verificarPermiso(usuario, "manage_users")
   activate SecRules

   SecRules -> BDAnalytics : SELECT funciones_implicadas("manage_users")
   activate BDAnalytics
   BDAnalytics --> SecRules : [view_users, create_users, modify_users, deactivate_users]
   deactivate BDAnalytics

   loop para cada función implicada
     SecRules -> SecRules : verificarPermiso(usuario, sub_funcion)
     activate SecRules
     SecRules --> SecRules : true | false
     deactivate SecRules
   end

   SecRules -->] : true (todas las atómicas\nestán autorizadas)
   deactivate SecRules
   @enduml

----
