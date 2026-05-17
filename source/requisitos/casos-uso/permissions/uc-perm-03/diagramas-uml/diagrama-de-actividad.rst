8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_03 — actividad

 @startuml

 start

 :Selecciona functions + User +
  expires_at + justification + TKT;
 :GET preview-exceptional;
 :Modal con preview separacion + warning
  high-priority audit;

 if (Confirma?) then (no)
   :Cancela; stop
 else (si)
 endif

 :POST exceptional-permissions/;
 note right
   Backend identico a UC_ACC_08
 end note

 if (Backend OK?) then (no)
   :Mostrar error segun status; stop
 else (si)
 endif

 :Refresh catalogo;
 :Toast confirmacion;

 stop

 @enduml

