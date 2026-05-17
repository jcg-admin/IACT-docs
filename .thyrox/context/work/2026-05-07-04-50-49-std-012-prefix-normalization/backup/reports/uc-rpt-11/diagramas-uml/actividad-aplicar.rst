8.3 Actividad (aplicar)
=======================

.. uml::

 @startuml
 start
 :GET con view_id;
 :Cargar SavedView;
 if (Owner == invoker?) then (si)
   :Aplicar (segmento del invoker);
 else (no)
   :Buscar ShareEntry activo;
   if (Encontrado?) then (no)
     :403; stop
   endif
   if (Expirado?) then (si)
     :403 SHARE_EXPIRED; stop
   endif
   :Aplicar (segmento del invoker);
 endif
 stop
 @enduml

