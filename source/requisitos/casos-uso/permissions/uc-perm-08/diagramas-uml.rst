.. _uc-perm-08-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_08 — generar menu

 @startuml
 left to right direction

 actor "User autenticado" as UserAutenticado
 actor "Frontend" as Frontend

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_08\nGenerar Menu" as UC08
   usecase "UC_PERM_07\nbulk check" as UC07
   usecase "FunctionRegistry\nlookup" as REG
   usecase "MenuCache" as MC
 }

 UserAutenticado --> Frontend
 Frontend --> UC08
 UC08 ..> UC07 : <<include>>
 UC08 ..> REG : <<include>>
 UC08 ..> MC : <<include>>

 note bottom of UC08
   El menu filtra UI; la seguridad
   real esta en UC_PERM_07.
 end note

 @enduml

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

8.3 Diagrama de estructura del menu
===================================

.. uml::
 :caption: Estructura jerarquica

 @startuml

 class Menu {
   user_id
   locale_used
   generated_at
   cache: bool
 }

 class Domain {
   code
   label
   order
 }

 class Section {
   code
   label
   icon
   order
 }

 class Action {
   code
   label
   function_code
   order
 }

 Menu "1" -- "*" Domain
 Domain "1" -- "*" Section
 Section "1" -- "*" Action

 @enduml

8.4 Diagrama de secuencia
=========================

.. uml::
 :caption: UC_PERM_08 — cache miss

 @startuml

 actor "User" as User
 participant "Frontend" as Frontend
 participant "MenuView" as Menuview
 participant "MenuBuilder" as Menubuilder
 participant "PermSvc" as Permsvc
 participant "Registry" as Registry
 participant "MenuCache" as Menucache

 User -> Frontend: login + visita
 Frontend -> Menuview: GET /api/me/menu/
 Menuview -> Menuview: JWT
 Menuview -> Menucache: get(key)
 Menucache --> Menuview: miss
 Menuview -> Menubuilder: build(user_id, locale)
 Menubuilder -> Registry: list(menu_visible=true)
 Registry --> Menubuilder: codes + metadata
 Menubuilder -> Permsvc: check_bulk(user_id, codes)
 Permsvc --> Menubuilder: results
 Menubuilder -> Menubuilder: filtrar + jerarquizar
 Menubuilder --> Menuview: menu
 Menuview -> Menucache: set(key, menu, ttl=300)
 Menuview --> Frontend: 200 menu
 Frontend --> User: render nav

 @enduml
