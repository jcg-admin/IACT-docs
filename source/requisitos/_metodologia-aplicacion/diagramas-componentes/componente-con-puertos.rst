16.4 Componente con puertos
---------------------------

.. uml::

   @startuml

   component "rpt_app" as Rpt {
     port p_audit
     port p_perm
   }
   component "aud_app" as Aud
   component "perm_app" as Perm

   p_audit -- Aud
   p_perm -- Perm
   @enduml
