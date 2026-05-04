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
   usecase "FunctionRegistry\nlookup" as RegistroFunciones
   usecase "MenuCache" as MenuCache
 }

 UserAutenticado --> Frontend
 Frontend --> UC08
 UC08 ..> UC07 : <<include>>
 UC08 ..> REG : <<include>>
 UC08 ..> MenuCache : <<include>>

 note bottom of UC08
   El menu filtra UI; la seguridad
   real esta en UC_PERM_07.
 end note

 @enduml

