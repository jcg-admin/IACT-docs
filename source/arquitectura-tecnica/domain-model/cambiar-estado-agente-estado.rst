.. meta::
 :artefacto: AT_UC_OPR_01_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_opr_01_domain_estado:

================================================================
UC_OPR_01 — Cambiar Estado del Agente — Estado de AccionOperador
================================================================

.. uml::
 :caption: UC_OPR_01 — Cambiar Estado del Agente — Estado de AccionOperador

 @startuml
 hide empty description

 [*] --> Iniciada : operador ejecuta accion
 Iniciada --> Procesando : sistema valida RBAC
 Procesando --> Completada : accion exitosa
 Procesando --> Fallida : error / sin permiso
 Completada --> [*] : registrar en auditoria
 Fallida --> [*] : registrar error

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-01/index`

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/operator/uc-opr-01/index`
