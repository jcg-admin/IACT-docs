8.2 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_08 — flujo

 @startuml

 start

 :GET /api/me/menu/;

 if (JWT valido?) then (no)
   :401; stop
 else (si)
 endif

 :Resolver locale;

 if (Cache hit?) then (si)
   :return cached;
   stop
 else (no)
 endif

 :PermissionService.check_bulk
  con codes del registry;
 :Filtrar segmento (CNST-008);
 :Construir arbol jerarquico;
 :Ordenar y suprimir vacios;
 :Cache write con TTL=300s;
 :return menu;

 stop

 @enduml

