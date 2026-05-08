.. _uc-usr-05-parte-08-notas-diagramas:

8.4 Notas sobre los diagramas
==============================

8.4.1 Conformidad uml-07
-------------------------

El diagrama de caso de uso (`diagrama-de-caso-de-uso.rst`)
cumple los criterios uml-07:

- ``actor "..."`` con stick figure (``block_users`` como
  funcion RBAC, ``AuthorizationGuard`` y ``AuditService``
  como componentes del sistema actuando como actores
  secundarios).
- ``rectangle "Sistema IACT — UC_USR_05" { ... }`` como
  system boundary.
- ``usecase "..."`` para el UC principal y los included.
- ``<<include>>`` para sub-acciones siempre ejecutadas.
- ``<<extend>>`` para el flujo opcional A3 (override de
  razon sobre bloqueo automatico previo).
- ``left to right direction`` para legibilidad (iniciador
  a la izquierda, actores secundarios a la derecha).

8.4.2 Notas semanticas
-----------------------

- ``block_users`` aparece como actor (funcion RBAC) y
  como capability requerida del admin invocador. Esta es
  la convencion STD-010 §4 D-DIAG-001 (los actores RBAC
  usan el nombre exacto de la funcion del catalogo).
- Las 4 sub-acciones marcadas ``<<include>>`` ocurren
  siempre dentro de la misma transaccion atomica
  (atomicidad — ver flujo principal paso 6).

8.4.3 Notas sobre actores
--------------------------

El diagrama distingue dos tipos de actores secundarios:

- ``AuthorizationGuard`` y ``AuditService`` son
  componentes internos del sistema, no humanos. Se
  representan como actores por convencion plantuml para
  expresar el role de "iniciador del check" (Guard) y
  "consumidor del evento" (Audit).
- El User bloqueado NO aparece como actor — no participa
  activamente del UC. Es el target del efecto.

8.4.4 Decision documental
--------------------------

NO se incluye diagrama de estados (``diagrama-de-estados-
user-state.rst``) porque la transicion de estados de
``User`` ya esta cubierta canonicamente en
``casos-uso/users/uc-usr-04/diagramas-uml/
diagrama-de-estados-user-state.rst``. UC_USR_05 reutiliza
la misma maquina de estados; duplicar el diagrama crearia
riesgo de divergencia.

Referencia cruzada: ver
:doc:`/requisitos/casos-uso/users/uc-usr-04/diagramas-uml/diagrama-de-estados-user-state`
para el diagrama canonico de UserState.
