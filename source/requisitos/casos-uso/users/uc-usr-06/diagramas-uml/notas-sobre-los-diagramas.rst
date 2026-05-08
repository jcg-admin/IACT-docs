.. _uc-usr-06-parte-08-notas-diagramas:

8.4 Notas sobre los diagramas
==============================

8.4.1 Conformidad uml-07
-------------------------

El diagrama de caso de uso cumple los criterios uml-07:

- ``actor`` (3): ``unblock_users`` (funcion RBAC),
  ``AuthorizationGuard``, ``AuditService``.
- ``rectangle "Sistema IACT — UC_USR_06"`` como system
  boundary.
- ``usecase`` (5): UC principal + 3 included + 1 extend.
- ``<<include>>`` para sub-acciones siempre ejecutadas.
- ``<<extend>>`` para warning de estado inconsistente
  (flujo alterno A2).
- ``left to right direction``.

8.4.2 Diferencias respecto a UC_USR_05
---------------------------------------

UC_USR_06 NO incluye sub-acciones de "cerrar Sessions" ni
"blacklistear tokens": la transicion BLOCKED→ACTIVE no
afecta sesiones (ya cerradas) ni tokens (ya
blacklistados). El User debe re-loguear (UC_AUTH_01)
para crear nueva sesion.

Si incluye una sub-accion adicional respecto a
UC_USR_05: el **lookup del bloqueo previo** para capturar
``original_block_event_id``. Este lookup es central a la
trazabilidad par bloqueo↔desbloqueo.

8.4.3 Decision documental
--------------------------

NO se incluye diagrama de estados separado por la misma
razon que en UC_USR_05: la maquina de estados de
``User`` es canonica en
:doc:`/requisitos/casos-uso/users/uc-usr-04/diagramas-uml/diagrama-de-estados-user-state`.

UC_USR_06 ejecuta la transicion ``BLOCKED → ACTIVE`` que
ya esta modelada en ese diagrama.

8.4.4 Notas sobre actores
--------------------------

Como en UC_USR_05, ``AuthorizationGuard`` y
``AuditService`` son componentes internos representados
como actor por convencion plantuml. El User desbloqueado
NO aparece como actor — recibe el efecto pasivamente
(podra loguear en el siguiente intento).
