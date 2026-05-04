9. Diagrama de distribución — despliegue del proyecto IACT
==========================================================

.. uml::

   @startuml

   node "Cliente Web" <<dispositivo>> as Browser {
     component "Chrome / Firefox"
   }

   node "Servidor IACT" <<procesador>> as Web {
     component "Apache 2.4"
     component "mod_wsgi"
     component "Django 4 (App IACT)"
   }

   node "BD Analytics" <<procesador>> as DB {
     database "MySQL\nDatos IVR + RBAC + Auditoría"
   }

   node "IVR Conmutador" <<dispositivo>> as IVR {
     component "BD IVR (read-only)"
   }

   node "Scheduler" <<procesador>> as Sched {
     component "APScheduler / Cron"
   }

   Browser -- Web   : HTTPS / SSL
   Web     -- DB    : TCP 3306
   Web     -- IVR   : TCP 3306\n(read-only,\nventana 6-12h\nCNST_006/008)
   Sched   -- Web   : disparo ETL\n(UC_PIP_01)
   @enduml

**Aplicación:** DOC-26. Stack per
:doc:`/devops/adr-devops-001-vagrant-mod-wsgi-importante-produc`
— **sin** Docker / K8s / Nginx / Gunicorn.

----
