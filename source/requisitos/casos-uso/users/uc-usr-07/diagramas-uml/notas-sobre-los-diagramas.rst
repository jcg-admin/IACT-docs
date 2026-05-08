.. _uc-usr-07-parte-08-notas-diagramas:

8.4 Notas sobre los diagramas
==============================

8.4.1 Conformidad uml-07
-------------------------

El diagrama de caso de uso cumple uml-07:

- ``actor`` (4): ``edit_own_profile`` (funcion RBAC),
  ``AuthorizationGuard``, ``EmailValidator``,
  ``AuditService``.
- ``rectangle "Sistema IACT — UC_USR_07"`` system
  boundary.
- ``usecase`` (5): UC + 3 included + 1 extend.
- ``<<include>>`` y ``<<extend>>`` con semantica
  correcta.
- ``left to right direction``.

8.4.2 Singularidad UC_USR_07
-----------------------------

UC_USR_07 es el unico UC del cluster ``users/`` donde:

- El actor primario y el target son el mismo User.
- No hay distincion admin vs target — es 100% self-
  service.
- La validacion de "no impersonation" es estructural: el
  ``user_id`` se infiere del JWT, no del URL. Imposible
  invocar el endpoint para editar a otro User.

8.4.3 EmailValidator como actor
--------------------------------

A diferencia de UC_USR_05/06 que solo tienen 3 actores
secundarios (Guard, Audit, y opcionalmente otros),
UC_USR_07 incluye ``EmailValidator`` como actor por su
papel central en el flujo: la validacion email
(formato + unicidad) es responsabilidad cohesiva
distinta del resto del flujo.

8.4.4 Decision documental
--------------------------

NO se incluye diagrama de estados — UC_USR_07 NO cambia
``User.state`` (sigue ACTIVE). La maquina de estados
canonica vive en
:doc:`/requisitos/casos-uso/users/uc-usr-04/diagramas-uml/diagrama-de-estados-user-state`.

8.4.5 PII en payload audit
---------------------------

El diagrama de secuencia explicita que el payload del
``PROFILE_UPDATED`` NO contiene los valores nuevos ni
viejos del email/full_name — solo la lista de
``fields_changed``. Esta es la aplicacion concreta de
CNST-026 (sin PII en payload audit) en este UC.
