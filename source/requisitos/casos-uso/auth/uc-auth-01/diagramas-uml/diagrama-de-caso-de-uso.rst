8.1 Diagrama de caso de uso
===========================

Vista estatica de actores y relaciones
inter-UC. Per UML_07 y la decision DEC-A06,
UC_AUTH_01 se modela como **un solo nodo** —
los sub-pasos viven en el diagrama de secuencia
(§ 8.2).

.. uml::
 :caption: UC_AUTH_01 — diagrama de caso de uso

 @startuml

 left to right direction

 actor "User"                   as User
 actor "Sistema"                 as Sistema <<system>>
 actor "view_audit_log"                 as view_audit_log <<system>>

 rectangle "IACT — MOD_Auth" {
   usecase "UC_AUTH_01\nIniciar Sesion" as UC_AUTH_01
   usecase "UC_AUTH_04\nCambiar\nContrasena"  as UC_AUTH_04
 }

 User  --> UC_AUTH_01 : presenta\ncredenciales
 UC_AUTH_01 --> Sistema  : valida + emite\ntokens + Session
 UC_AUTH_01 --> view_audit_log  : registra\nAuditEvent LOGIN

 UC_AUTH_04 ..> UC_AUTH_01 : <<extend>>\n[primer login\no expirado]

 note bottom of UC_AUTH_01
   Pre-cond CNST-003 (Session en BD)
   Pre-cond CNST-004 (sesion unica)
   Pre-cond CNST-011 (throttling)
   Pos-cond CNST-025 (audit inmutable)
 end note

 @enduml

