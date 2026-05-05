14.7 Mensaje con guarda condicional
-----------------------------------

.. uml::

   @startuml
   allowmixing

   object ":auth_app" as Auth
   object ":audit_log" as Audit

   Auth -> Audit : "1: [credenciales_validas] registrar_acceso()"
   @enduml
