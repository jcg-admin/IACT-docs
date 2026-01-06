.. meta::
   :artefacto: UC_002
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/auth
   :modulo: MOD_Auth
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-002:

==============================================================================
UC-002: Cerrar Sesion
==============================================================================

.. contents:: Contenido
   :local:
   :depth: 2

----

1. Resumen
----------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **ID**
     - UC-002
   * - **Nombre**
     - Cerrar Sesion
   * - **Actor Primario**
     - Usuario autenticado
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Auth
   * - **Complejidad**
     - Baja
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite a un usuario autenticado finalizar su sesion activa de manera segura,
invalidando su token JWT en el servidor y limpiando los datos de sesion en
el cliente. Registra el evento de logout en auditoria (BR_008).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-002 Cerrar Sesion
   :align: center
   :scale: 90%

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA
   skinparam usecase {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
       BorderThickness 2
   }
   skinparam rectangle {
       BackgroundColor #ECEFF1
       BorderColor #455A64
   }

   actor "Usuario\nAutenticado" as U
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Auth" {
       usecase "UC-002:\nCerrar Sesion" as UC002
       usecase "Invalidar\nToken JWT" as INV
       usecase "Registrar\nEvento" as REG
   }

   U --> UC002
   UC002 ..> INV : <<include>>
   UC002 ..> REG : <<include>>
   UC002 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene sesion activa (token JWT valido)
2. Usuario esta en cualquier pantalla del sistema

4.2 Trigger
^^^^^^^^^^^

Usuario hace clic en opcion "Cerrar Sesion" del menu de usuario.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Token JWT invalidado en servidor (agregado a blacklist)
2. Token eliminado del almacenamiento del cliente
3. Evento LOGOUT registrado en auditoria (BR_008)
4. Usuario redirigido a pantalla de login

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Si falla invalidacion en servidor, token expirara naturalmente (24h)
2. Cliente siempre limpia su almacenamiento local

----

5. Flujo Normal
---------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Actor
     - Sistema
   * - 1
     - Hace clic en menu de usuario (header)
     -
   * - 2
     -
     - Muestra menu desplegable con opciones
   * - 3
     - Selecciona "Cerrar Sesion"
     -
   * - 4
     -
     - Muestra modal de confirmacion
   * - 5
     - Confirma cierre de sesion
     -
   * - 6
     -
     - Envia request de logout al servidor
   * - 7
     -
     - Invalida token JWT (agrega a blacklist)
   * - 8
     -
     - Registra evento LOGOUT en auditoria (BR_008)
   * - 9
     -
     - Retorna confirmacion de logout
   * - 10
     -
     - Limpia token de localStorage/sessionStorage
   * - 11
     -
     - Redirige a pantalla de login
   * - 12
     -
     - Muestra mensaje "Sesion cerrada exitosamente"

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-002 Cerrar Sesion
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center
   skinparam participant {
       BackgroundColor #E8F5E9
       BorderColor #388E3C
   }
   skinparam database {
       BackgroundColor #FFF3E0
       BorderColor #F57C00
   }

   actor "Usuario" as U
   participant "Frontend\n(React)" as FE #E3F2FD
   participant "AuthController\n(DRF)" as AC #E8F5E9
   participant "SessionService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Clic en "Cerrar Sesion"
   activate FE

   FE -> FE: 2. Mostrar modal confirmacion
   FE --> U: "¿Confirma cerrar sesion?"

   U -> FE: 3. Confirma

   FE -> AC: 4. POST /api/auth/logout\nAuthorization: Bearer {token}
   activate AC

   AC -> AC: 5. Extraer token de header

   AC -> SS: 6. invalidateToken(token)
   activate SS
   SS -> DB: INSERT INTO token_blacklist\n(token, invalidated_at)
   note right: Token en blacklist\nrechazado en futuras requests
   SS --> AC: OK
   deactivate SS

   AC -> AUD: 7. logEvent(LOGOUT, userId)
   activate AUD
   AUD -> DB: INSERT INTO audit_log\n(action='LOGOUT', user_id, ip, timestamp)
   note right: BR_008:\nRegistro de auditoria
   AUD --> AC: OK
   deactivate AUD

   AC --> FE: 8. 200 OK\n{message: "Logout exitoso"}
   deactivate AC

   FE -> FE: 9. localStorage.removeItem('token')
   FE -> FE: 10. Limpiar estado de aplicacion

   FE --> U: 11. Redirect /login
   FE --> U: 12. Toast: "Sesion cerrada"
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Usuario Cancela Cierre
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 4 del flujo normal

**Condicion:** Usuario hace clic en "Cancelar" en modal de confirmacion

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 4.1
     - Sistema cierra modal de confirmacion
   * - 4.2
     - Usuario permanece en pantalla actual
   * - 4.3
     - Sesion continua activa

**Retorno:** Fin del caso de uso (sin cambios)

7.2 FA-2: Error de Conexion al Servidor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 6 del flujo normal

**Condicion:** No se puede conectar al servidor para invalidar token

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 6.1
     - Sistema detecta error de conexion
   * - 6.2
     - Sistema limpia token localmente de todas formas
   * - 6.3
     - Sistema redirige a login
   * - 6.4
     - Sistema muestra mensaje "Sesion cerrada localmente"

**Retorno:** Paso 11 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Token Ya Invalido
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Token ya esta en blacklist o expiro

**Accion del Sistema:** Procede con limpieza local y redireccion

**Mensaje al Usuario:** "Sesion cerrada exitosamente"

8.2 EX-2: Sesion Expirada por Inactividad
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Token expiro por tiempo (24h) antes de logout manual

**Accion del Sistema:** Detecta 401 y limpia almacenamiento local

**Mensaje al Usuario:** "Su sesion ha expirado"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-002 Cerrar Sesion
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam activity {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
       DiamondBackgroundColor #FFF9C4
       DiamondBorderColor #F57C00
   }

   start

   :Usuario hace clic en\n"Cerrar Sesion";

   :Mostrar modal de confirmacion;

   if (Usuario confirma?) then (si)

       :Enviar request logout al servidor;

       if (Servidor responde?) then (si)

           :Invalidar token en blacklist;
           #C8E6C9:Registrar LOGOUT en auditoria\n(BR_008);

       else (no)
           note right: Error de conexion\nToken expirara naturalmente
       endif

       :Limpiar token de localStorage;
       :Limpiar estado de aplicacion;
       :Redirigir a /login;
       #C8E6C9:Mostrar "Sesion cerrada";
       stop

   else (no)
       :Cerrar modal;
       :Permanecer en pantalla actual;
       stop
   endif

   @enduml

----

10. Reglas de Negocio
---------------------

.. list-table::
   :widths: 12 25 63
   :header-rows: 1

   * - BR
     - Nombre
     - Aplicacion en este UC
   * - BR_008
     - Auditoria de Accesos
     - Paso 8: Todo logout se registra en audit_log con timestamp, user_id, IP

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-002.01
     - Sistema DEBE mostrar opcion "Cerrar Sesion" en menu de usuario
   * - FR-002.02
     - Sistema DEBE solicitar confirmacion antes de cerrar sesion
   * - FR-002.03
     - Sistema DEBE invalidar token JWT en servidor (blacklist)
   * - FR-002.04
     - Sistema DEBE limpiar token de almacenamiento del cliente
   * - FR-002.05
     - Sistema DEBE registrar evento LOGOUT en auditoria (BR_008)
   * - FR-002.06
     - Sistema DEBE redirigir a pantalla de login
   * - FR-002.07
     - Sistema DEBE mostrar mensaje de confirmacion de cierre
   * - FR-002.08
     - Sistema DEBE manejar cancelacion sin efectos secundarios

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_008 (Auditoria de Accesos)
   * - **FR Derivados**
     - FR-002.01 a FR-002.08 (8 requerimientos)
   * - **UC Relacionados**
     - UC-001 (Iniciar Sesion)
   * - **Actores RBAC**
     - Todos (cualquier usuario autenticado)
   * - **Funciones RBAC**
     - No aplica (disponible para todos los autenticados)

----

13. Historial de Cambios
------------------------

.. list-table::
   :widths: 12 12 20 56
   :header-rows: 1

   * - Version
     - Fecha
     - Autor
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Equipo IACT
     - Version con PlantUML embebido (Sphinx). 3 diagramas.
   * - 1.0.0
     - 2026-01-05
     - Equipo IACT
     - Version inicial sin diagramas