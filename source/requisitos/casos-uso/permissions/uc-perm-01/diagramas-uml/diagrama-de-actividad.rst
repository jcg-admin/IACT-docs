8.3 Diagrama de actividad
=========================

.. uml::
 :caption: UC_PERM_01 — actividad

 @startuml

 start

 :Invoker abre catalogo de AGRs;
 :Selecciona AGR;
 :Selecciona User destino;

 :GET preview-assign;
 :Modal con composicion + impact;

 if (Confirma?) then (no)
   :Cancela; stop
 else (si)
 endif

 :POST /api/users/{id}/access-groups/;

 note right
   Flujo backend identico
   a UC_ACC_04
 end note

 if (Backend OK?) then (no)
   :Mostrar error segun status; stop
 else (si)
 endif

 :Refrescar catalogo
  (counts AGR +1);
 :Toast confirmacion;

 stop

 @enduml

