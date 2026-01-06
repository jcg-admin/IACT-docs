.. meta::
   :artefacto: UC_005
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/auth
   :modulo: MOD_Auth
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-005:

==============================================================================
UC-005: Gestionar Sesiones Activas
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
     - UC-005
   * - **Nombre**
     - Gestionar Sesiones Activas
   * - **Actor Primario**
     - Administrador de Seguridad
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Auth
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite a un administrador de seguridad visualizar todas las sesiones activas
en el sistema, ver detalles de cada sesion (usuario, IP, inicio, ultima actividad)
y forzar el cierre de sesiones individuales o todas las sesiones de un usuario.
Cada cierre forzado se registra en auditoria (BR_008).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-005 Gestionar Sesiones
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

   actor "Administrador\nSeguridad" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray
   actor "Usuario\nAfectado" as UA #LightGray

   rectangle "MOD_Auth" {
       usecase "UC-005:\nGestionar\nSesiones" as UC005
       usecase "Listar\nSesiones\nActivas" as LSA
       usecase "Ver Detalle\nSesion" as VDS
       usecase "Cerrar\nSesion\nIndividual" as CSI
       usecase "Cerrar Todas\nSesiones\nUsuario" as CTS
       usecase "Registrar\nEvento" as REG
   }

   ADM --> UC005
   UC005 ..> LSA : <<include>>
   UC005 ..> VDS : <<include>>
   UC005 ..> CSI : <<extends>>
   UC005 ..> CTS : <<extends>>
   CSI ..> REG : <<include>>
   CTS ..> REG : <<include>>
   UC005 --> SA
   CSI --> UA : notifica
   CTS --> UA : notifica
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion AUT-004 (Gestionar Sesiones)
3. Administrador pertenece a agrupador AGR-008 (admin_seguridad)

4.2 Trigger
^^^^^^^^^^^

Administrador accede a "Gestion de Sesiones" en menu de administracion.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Lista de sesiones activas mostrada con paginacion
2. Si se cerro sesion: token invalidado y auditoria registrada
3. Usuario afectado recibe 401 en siguiente request

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Solo administradores con funcion AUT-004 pueden acceder
2. Cierre forzado siempre se registra en auditoria
3. Administrador no puede cerrar su propia sesion desde aqui

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
     - Accede a "Gestion de Sesiones"
     - 
   * - 2
     - 
     - Verifica permiso AUT-004
   * - 3
     - 
     - Obtiene lista de sesiones activas
   * - 4
     - 
     - Muestra tabla paginada (20 por pagina)
   * - 5
     - Visualiza lista de sesiones
     - 
   * - 6
     - (Opcional) Aplica filtros por usuario o IP
     - 
   * - 7
     - 
     - Actualiza lista segun filtros
   * - 8
     - Selecciona una sesion para ver detalle
     - 
   * - 9
     - 
     - Muestra detalle: usuario, IP, inicio, ultima actividad, user-agent
   * - 10
     - (Opcional) Decide cerrar la sesion
     - 
   * - 11
     - 
     - Muestra modal de confirmacion
   * - 12
     - Confirma cierre de sesion
     - 
   * - 13
     - 
     - Invalida token de la sesion
   * - 14
     - 
     - Registra FORCE_LOGOUT en auditoria (BR_008)
   * - 15
     - 
     - Actualiza lista eliminando sesion cerrada
   * - 16
     - 
     - Muestra mensaje "Sesion cerrada exitosamente"

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-005 Gestionar Sesiones
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

   actor "Admin\nSeguridad" as ADM
   participant "Frontend\n(React)" as FE #E3F2FD
   participant "SessionController\n(DRF)" as SC #E8F5E9
   participant "RBACService" as RBAC #E8F5E9
   participant "SessionService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Accede a "Gestion Sesiones"
   activate FE

   FE -> SC: 2. GET /api/admin/sessions\nAuthorization: Bearer {token}
   activate SC

   SC -> RBAC: 3. checkPermission(userId, 'AUT-004')
   activate RBAC
   RBAC -> DB: SELECT * FROM user_functions\nWHERE user_id=? AND function='AUT-004'
   DB --> RBAC: {authorized: true}
   RBAC --> SC: authorized
   deactivate RBAC

   SC -> SS: 4. getActiveSessions(page=1, limit=20)
   activate SS
   SS -> DB: SELECT s.*, u.username\nFROM sessions s\nJOIN users u ON s.user_id = u.id\nWHERE s.active = true\nORDER BY s.last_activity DESC\nLIMIT 20 OFFSET 0
   DB --> SS: [sessions]
   SS --> SC: {sessions, total, page}
   deactivate SS

   SC --> FE: 5. 200 OK {sessions, pagination}
   deactivate SC

   FE --> ADM: 6. Muestra tabla de sesiones
   note right: Columnas: Usuario, IP,\nInicio, Ultima Actividad

   ADM -> FE: 7. Clic en "Cerrar" sesion X
   FE --> ADM: 8. Modal: "¿Cerrar sesion de {user}?"

   ADM -> FE: 9. Confirma

   FE -> SC: 10. DELETE /api/admin/sessions/{sessionId}
   activate SC

   SC -> RBAC: 11. checkPermission(userId, 'AUT-004')
   RBAC --> SC: authorized

   SC -> SS: 12. invalidateSession(sessionId)
   activate SS
   SS -> DB: UPDATE sessions SET active=false\nWHERE id = ?
   SS -> DB: INSERT INTO token_blacklist\n(token, invalidated_at, reason='FORCE_LOGOUT')
   SS --> SC: {invalidated: true, userId: targetUserId}
   deactivate SS

   SC -> AUD: 13. logEvent(FORCE_LOGOUT,\nadminId, targetUserId)
   activate AUD
   AUD -> DB: INSERT INTO audit_log\n(action='FORCE_LOGOUT',\nperformed_by=adminId,\ntarget_user=targetUserId)
   note right: BR_008:\nRegistra quien cerro\nla sesion de quien
   AUD --> SC: OK
   deactivate AUD

   SC --> FE: 14. 200 OK {message}
   deactivate SC

   FE -> FE: 15. Eliminar sesion de lista
   FE --> ADM: 16. "Sesion cerrada exitosamente"
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Cerrar Todas las Sesiones de un Usuario
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 10 del flujo normal

**Condicion:** Admin selecciona "Cerrar todas las sesiones" de un usuario

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 10.1
     - Sistema muestra opcion "Cerrar todas las sesiones de {usuario}"
   * - 10.2
     - Admin confirma accion
   * - 10.3
     - Sistema invalida TODOS los tokens del usuario
   * - 10.4
     - Sistema registra evento FORCE_LOGOUT_ALL en auditoria
   * - 10.5
     - Sistema actualiza lista eliminando todas las sesiones del usuario

**Retorno:** Paso 16 del flujo normal

7.2 FA-2: Sin Permiso de Acceso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 2 del flujo normal

**Condicion:** Usuario no tiene funcion AUT-004

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 2.1
     - Sistema retorna 403 Forbidden
   * - 2.2
     - Frontend redirige a dashboard
   * - 2.3
     - Sistema muestra "No tiene permisos para esta accion"

**Retorno:** Fin del caso de uso

7.3 FA-3: Filtrar por Usuario
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 6 del flujo normal

**Condicion:** Admin ingresa username en filtro

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 6.1
     - Admin ingresa username parcial o completo
   * - 6.2
     - Sistema filtra sesiones que coinciden (LIKE)
   * - 6.3
     - Sistema muestra resultados filtrados

**Retorno:** Paso 7 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Admin Intenta Cerrar su Propia Sesion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Admin selecciona su propia sesion para cerrar

**Accion del Sistema:** Rechaza la operacion

**Mensaje al Usuario:** "No puede cerrar su propia sesion desde aqui. Use 'Cerrar Sesion' del menu."

8.2 EX-2: Sesion Ya Invalida
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Sesion fue cerrada por otro proceso mientras admin la veia

**Accion del Sistema:** Actualiza lista y muestra mensaje

**Mensaje al Usuario:** "La sesion ya no esta activa"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-005 Gestionar Sesiones
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

   :Admin accede a\n"Gestion de Sesiones";

   :Verificar permiso AUT-004;

   if (Tiene permiso?) then (si)
       
       :Obtener lista de\nsesiones activas;
       
       :Mostrar tabla paginada;
       
       while (Admin continua gestionando?) is (si)
           
           if (Aplica filtro?) then (si)
               :Filtrar por usuario/IP;
               :Actualizar lista;
           else (no)
           endif
           
           if (Selecciona sesion?) then (si)
               :Mostrar detalle de sesion;
               
               if (Decide cerrar?) then (si)
                   
                   if (Es su propia sesion?) then (si)
                       #FFE0B2:Error: "No puede cerrar\nsu propia sesion";
                   else (no)
                       :Mostrar confirmacion;
                       
                       if (Confirma?) then (si)
                           
                           if (Cerrar todas del usuario?) then (si)
                               :Invalidar TODOS los tokens\ndel usuario;
                               #C8E6C9:Registrar FORCE_LOGOUT_ALL\n(BR_008);
                           else (no)
                               :Invalidar token individual;
                               #C8E6C9:Registrar FORCE_LOGOUT\n(BR_008);
                           endif
                           
                           :Actualizar lista;
                           #C8E6C9:Mostrar confirmacion;
                           
                       else (no)
                           :Cancelar operacion;
                       endif
                       
                   endif
                   
               else (no)
               endif
               
           else (no)
           endif
           
       endwhile (no)
       
       stop
       
   else (no)
       #FFCDD2:403 Forbidden;
       :Redirigir a dashboard;
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
   * - BR_005
     - Sesion Unica por Usuario
     - Contexto: Este UC permite gestionar el cumplimiento de BR_005
   * - BR_008
     - Auditoria de Accesos
     - Paso 14: Cierre forzado registra FORCE_LOGOUT con admin y usuario afectado

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-005.01
     - Sistema DEBE verificar permiso AUT-004 antes de acceder
   * - FR-005.02
     - Sistema DEBE listar sesiones activas con paginacion (20/pagina)
   * - FR-005.03
     - Sistema DEBE mostrar: username, IP, fecha inicio, ultima actividad, user-agent
   * - FR-005.04
     - Sistema DEBE permitir filtrar por username (busqueda parcial)
   * - FR-005.05
     - Sistema DEBE permitir filtrar por direccion IP
   * - FR-005.06
     - Sistema DEBE solicitar confirmacion antes de cerrar sesion
   * - FR-005.07
     - Sistema DEBE poder invalidar sesion individual
   * - FR-005.08
     - Sistema DEBE poder cerrar todas las sesiones de un usuario
   * - FR-005.09
     - Sistema DEBE registrar FORCE_LOGOUT en auditoria (BR_008)
   * - FR-005.10
     - Sistema DEBE actualizar lista automaticamente tras cerrar sesion

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_005 (Sesion Unica), BR_008 (Auditoria)
   * - **FR Derivados**
     - FR-005.01 a FR-005.10 (10 requerimientos)
   * - **UC Relacionados**
     - UC-001 (Iniciar Sesion), UC-002 (Cerrar Sesion)
   * - **Actores RBAC**
     - AGR-008: admin_seguridad
   * - **Funciones RBAC**
     - AUT-004: Gestionar Sesiones

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