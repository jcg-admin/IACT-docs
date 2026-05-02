.. _arq-mod-005-diagramas:

================================================
ARQ_MOD_005 — Diagramas de Comportamiento
================================================


Flujo de Acceso a Visualizaciones
===================================

.. uml::
 :caption: Flujo de acceso a visualizaciones — consulta RBAC, segmentos y exportación.

 @startuml

 start

 :Usuario accede al módulo\nde visualizaciones;

 :Consultar ARQ_MOD_003 RBAC\n¿Qué dashboards/reportes puede ver?\n¿Tiene permiso de exportación?;

 :Aplicar filtro de segmentos de datos\n(Centro, Servicio, Región según RBAC);

 if (¿Tiene permiso 'view'?) then (sí)
   :Mostrar dashboards y tablas\nfiltradas por segmento;
   if (¿Tiene permiso 'export'?) then (sí)
     :Mostrar opciones de exportación\n(CSV / Excel / PDF);
     if (¿Solicita exportación?) then (sí)
       :Validar límites diarios (CNST_007);
       if (¿Dentro del límite?) then (sí)
         :Encolar job de exportación asíncrona;
         :Notificar via buzón interno\ncuando esté listo;
         stop
       else (límite excedido)
         :Rechazar → error de cuota;
         stop
       endif
     else (no exporta)
       stop
     endif
   else (sin permiso export)
     stop
   endif
 else (sin permiso view)
   :Mostrar pantalla vacía\n(sin datos, sin error);
   stop
 endif

 @enduml
