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
