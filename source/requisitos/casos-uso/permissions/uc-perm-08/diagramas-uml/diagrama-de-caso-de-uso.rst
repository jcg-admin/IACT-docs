8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PERM_08 — generar menu

 @startuml
 left to right direction

 actor "User autenticado" as UserAutenticado
 actor "Frontend" as Frontend

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_08\nGenerar Menu" as UC_PERM_08
   usecase "UC_PERM_07\nbulk check" as UC_PERM_07
   usecase "FunctionRegistry\nlookup" as RegistroFunciones
   usecase "MenuCache" as MenuCache
 }

 UserAutenticado --> Frontend
 Frontend --> UC_PERM_08
 UC_PERM_08 ..> UC_PERM_07 : <<include>>
 UC_PERM_08 ..> REG : <<include>>
 UC_PERM_08 ..> MenuCache : <<include>>

 note bottom of UC_PERM_08
   El menu filtra UI; la seguridad
   real esta en UC_PERM_07.
 end note

 @enduml

