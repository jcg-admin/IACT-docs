Primer paso del Container IACT — actor y los dos primeros containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El equivalente IACT del ejemplo del libro (Web App +
Mobile App). En IACT no hay app móvil — el supervisor
opera desde un navegador en intranet. Los dos primeros
containers son entonces el **Browser** del supervisor
y el ``iact.wsgi`` que sirve la SPA.

.. uml::

   @startuml
   title IACT C4 — Container view (paso 1)

   actor "Supervisor\n[Person]\n\nMonitorea llamadas\ny reportes" as Supervisor

   rectangle "Browser\n[Navegador del supervisor]\n\nCliente de la SPA en intranet" as Browser <<c4_container>>

   rectangle "iact.wsgi\n[Django + mod_wsgi sobre Apache]\n\nServe la SPA y expone\nla API REST del backend" as SERVIDOR_WSGI <<c4_container>>

   Supervisor --> Browser : opera el panel\n[uso directo]
   Browser --> SERVIDOR_WSGI : consulta dashboards,\nreconoce alertas\n[HTTPS intranet]
   @enduml
