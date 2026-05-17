5. Componentes dentro de los nodos
==================================

Vista de detalle de ``vm-iact`` mostrando los artefactos que
contiene y a qué interfaz corresponden (cruce con H12).

.. uml::

   @startuml

   node "vm-iact" as VmIact {
     node "Apache + mod_wsgi" {
       artifact "iact.wsgi"
       artifact "auth_app — IAutenticacion"
       artifact "perm_app — ISecurity"
       artifact "rpt_app — IReporte"
       artifact "alr_app — IAlerta"
       artifact "pip_app — IETL"
       artifact "aud_app — IAuditLog"
       artifact "log_app — INotificacion"
     }
     node "Redis"
     database "bd_analytics"
     database "audit_log"
     artifact "etl_runner.py"
   }
   @enduml
