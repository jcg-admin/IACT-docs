.. meta::
 :artefacto: ARQ_MOD_008_DIAG_SECUENCIA_CONSULTA
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/sys-logs/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_008_secuencia_consulta_logs:

=========================================
Secuencia de Consulta de Logs del Sistema
=========================================

Secuencia de Consulta de Logs del Sistema
==========================================

.. uml::
 :caption: Secuencia view_application_logs — consulta filtrada con tail SSE opcional.

 @startuml

 actor "view_application_logs" as view_application_logs
 participant "LogEndpoint\n(/logs/system/)" as Logendpoint
 database "LogStore\n(PostgreSQL)" as Logstore

 view_application_logs -> Logendpoint : GET /logs/system/?range=1h&level=ERROR
 Logendpoint -> Logendpoint : JWT + RBAC (view_application_logs)
 alt sin permiso
   Logendpoint --> view_application_logs : 403 Forbidden
 else con permiso
   Logendpoint -> Logstore : consultar WHERE level=ERROR AND ts > now()-1h
   Logstore --> Logendpoint : entries
   Logendpoint -> Logendpoint : sanitizar (eliminar PII)
   Logendpoint --> view_application_logs : 200 + entries JSON
   opt tail SSE
     loop nuevas entradas
       Logstore -> Logendpoint : new entry
       Logendpoint -> view_application_logs : SSE data
     end
   end
 end

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/sys-logs/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
