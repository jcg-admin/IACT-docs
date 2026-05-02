.. _arq-mod-003-diagramas:

================================================
ARQ_MOD_003 — Diagramas de Comportamiento
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

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

----

Evaluacion de Conflicto SoD
============================

.. uml::
 :caption: Evaluación de conflicto SoD — antes de activar cualquier asignación.

 @startuml

 start

 :Solicitud de asignación\nde función F al usuario U;

 :Obtener funciones activas del usuario U;

 if (¿Alguna función activa entra\nen conflicto SoD con F?) then (sí)
   :Rechazar asignación\n→ error SoD_VIOLATION;
   stop
 else (no)
   :Registrar asignación;
   :Emitir AuditEvent\n(PERMISSION_GRANT);
   stop
 endif

 note right
   Conflictos definidos:
   - Creador de usuarios <-> Auditor
   - Administrador de reportes <-> Exportación ilimitada
 end note

 @enduml
