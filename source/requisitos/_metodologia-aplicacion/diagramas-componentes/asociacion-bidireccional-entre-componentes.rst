16.6 Asociación bidireccional entre componentes
-----------------------------------------------

.. uml::

   @startuml

   component "Apache" as Apache
   component "mod_wsgi" as mod_wsgi

   Apache -- mod_wsgi : carga / ejecuta
   @enduml
