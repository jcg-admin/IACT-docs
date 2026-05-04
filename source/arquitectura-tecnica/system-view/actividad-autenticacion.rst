.. meta::
 :artefacto: AT_UML_SISTEMA_06_ACTIVIDAD_AUTH
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_actividad_auth:

=================================================================
Sistema IACT — Diagrama de Actividad: Sub-actividad Autenticacion
=================================================================

6. Diagrama de Actividad — Sub-actividad Autenticacion
========================================================

Flujo interno de la funcion de autenticacion. El usuario ingresa
credenciales; el sistema las valida en PostgreSQL, genera el JWT
con payload RBAC y carga las funciones del usuario. Si las
credenciales son incorrectas se retorna 401.

.. uml::
 :caption: Figura 7 — Diagrama de actividad (sub-actividad autenticacion)

 @startuml

 |User|
 start
 :Ingresar username y password;

 |Sistema IACT|
 :Recibir POST /api/auth/login/;
 :Consultar auth_user en PostgreSQL;
 if (Credenciales correctas?) then (si)
   :Cargar funciones RBAC del usuario;
   :Generar JWT con payload RBAC;
   |User|
   :Acceder al sistema;
   :Autenticacion exitosa;
 else (no)
   :Retornar 401 Unauthorized;
   |User|
   if (Reintentar?) then (si)
     :Ingresar credenciales nuevamente;
   else (no)
     stop
   endif
 endif

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`
