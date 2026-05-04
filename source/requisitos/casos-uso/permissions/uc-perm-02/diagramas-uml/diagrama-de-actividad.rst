8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_02 — actividad

 @startuml

 start

 :Identifica User + AGR a revocar;
 :GET preview-revoke;
 :Modal con composicion + warnings;

 if (Confirma?) then (no)
   :Cancela; stop
 else (si)
 endif

 if (Warnings criticos?) then (si)
   :Doble confirmacion (escribir);
   if (Confirma literal?) then (no)
     :Cancela; stop
   else (si)
   endif
 else (no)
 endif

 :eliminar backend;
 note right
   Flujo identico a UC_ACC_02
   sobre target_type=AGR
 end note

 if (Backend OK?) then (no)
   :Mostrar error; stop
 else (si)
 endif

 :Refresh catalogo (count -1);
 :Toast confirmacion;

 stop

 @enduml

