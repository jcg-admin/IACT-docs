6. Diagrama de actividades
--------------------------

**Propósito:** flujo de trabajo o decisiones dentro de un
proceso. Actividades + decisiones (sí/no) + sincronización.

**Cuándo usarlo:** cuando necesitas mostrar**procesos
complejos con decisiones** (similar a un diagrama de flujo).

**Lección completa:** :doc:`/base-cognitiva/_uml/uml-11-diagramas-actividades/index`.

.. uml::

   @startuml

   start
   :Agregar ropa;
   :Agregar detergente;
   if ([ropa sucia]) then (sí)
     :Activar lavadora;
     :Llenar (1-2 min);
     :Remojar (5 min);
     :Lavar (15 min);
     :Enjuagar;
     :Centrifugar (5 min);
     :Sacar ropa;
   else (no)
   endif
   stop
   @enduml
