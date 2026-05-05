.. meta::
 :artefacto: ARQ_MOD_003_DIAG_PRECEDENCIA
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/rbac-core/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_003_precedencia_permisos:

=======================
Precedencia de Permisos
=======================

.. uml::
 :caption: Flujo de evaluación de permisos — precedencia Directo > Rol > Segmento.

 @startuml

 start

 :Solicitud de acceso\n(usuario, función);

 if (¿Tiene permiso DIRECTO vigente?) then (sí)
   :Aplicar permiso directo\n(vence en máx. 6 meses);
   stop
 else (no)
   if (¿Tiene permiso por ROL?) then (sí)
     :Aplicar permiso heredado\ndel rol asignado;
     stop
   else (no)
     if (¿Tiene permiso por SEGMENTO?) then (sí)
       :Aplicar permiso con\nrestricción de datos del segmento;
       stop
     else (no)
       :Denegar acceso → 403;
       stop
     endif
   endif
 endif

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/rbac-core/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
