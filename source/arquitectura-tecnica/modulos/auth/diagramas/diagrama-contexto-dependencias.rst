.. meta::
 :artefacto: ARQ_MOD_001_DIAG_CONTEXTO_DEPS
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/auth/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_001_diagrama_contexto_deps:

===================================
Diagrama de Contexto (Dependencias)
===================================

.. uml::
 :caption: Dependencias del módulo AUTH — componentes que requiere y que lo requieren.

 @startuml

 component "ARQ_MOD_001\nAutenticación" as AUTH
 component "ARQ_MOD_002\nIdentidad de Usuario" as ArqMod002
 component "ARQ_MOD_003\nControl de Acceso\n(RBAC)" as RBAC
 component "ARQ_MOD_007\nAuditoría" as ArqMod007

 AUTH --> ArqMod002 : verifica usuario activo
 AUTH --> RBAC : obtiene roles para claims del token
 AUTH --> ArqMod007 : emite evento login/logout

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/auth/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`
