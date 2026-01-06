.. meta::
   :artefacto: UC_001
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/auth
   :modulo: MOD_Auth
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-001:

==============================================================================
UC-001: Iniciar Sesion
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
     - UC-001
   * - **Nombre**
     - Iniciar Sesion
   * - **Actor Primario**
     - Usuario no autenticado
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

Permite a un usuario autenticarse en el sistema IACT proporcionando sus
credenciales (username y password) para obtener acceso a las funcionalidades
segun sus permisos asignados. Implementa sesion unica por usuario (BR_005)
y registro de auditoria de accesos (BR_008).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-001 Iniciar Sesion
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

   actor "Usuario\nNo Autenticado" as U
   actor "Sistema\nAuditoria" as SA #LightGray

   rectangle "MOD_Auth" {
       usecase "UC-001:\nIniciar Sesion" as UC001
       usecase "UC-003:\nRecuperar\nPassword" as UC003
       usecase "Registrar\nEvento" as REG
       usecase "Invalidar\nSesiones\nPrevias" as INV
   }

   U --> UC001
   UC001 ..> UC003 : <<extends>>\n[olvido password]
   UC001 ..> REG : <<include>>
   UC001 ..> INV : <<include>>\n[BR_005]
   UC001 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene cuenta activa en el sistema (estado = ACTIVO)
2. Usuario conoce sus credenciales (username y password)
3. Sistema esta disponible y accesible
4. Usuario no tiene sesion activa (o sera invalidada)

4.2 Trigger
^^^^^^^^^^^

Usuario accede a la URL de login del sistema (/login).

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Token JWT generado y entregado al cliente
2. Sesiones anteriores del usuario invalidadas (BR_005)
3. Evento de login registrado en tabla de auditoria (BR_008)
4. Usuario redirigido a dashboard principal
5. Contador de intentos fallidos reseteado a cero

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Credenciales nunca se almacenan en logs ni en texto plano
2. Intentos fallidos siempre se registran para BR_015
3. Hash de password usa bcrypt con cost >= 12

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
     - Accede a la pantalla de login
     -
   * - 2
     -
     - Muestra formulario con campos username y password
   * - 3
     - Ingresa username y password
     -
   * - 4
     - Presiona boton "Iniciar Sesion"
     -
   * - 5
     -
     - Valida formato de campos (longitud, caracteres)
   * - 6
     -
     - Verifica que cuenta no este bloqueada (BR_015)
   * - 7
     -
     - Busca usuario por username en base de datos
   * - 8
     -
     - Verifica password con bcrypt.checkpw()
   * - 9
     -
     - Valida que usuario tenga estado ACTIVO
   * - 10
     -
     - Invalida sesiones previas del usuario (BR_005)
   * - 11
     -
     - Genera token JWT con claims del usuario
   * - 12
     -
     - Resetea contador de intentos fallidos
   * - 13
     -
     - Registra evento LOGIN en auditoria (BR_008)
   * - 14
     -
     - Retorna token JWT al cliente
   * - 15
     -
     - Redirige a dashboard principal

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-001 Iniciar Sesion
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center
   skinparam responseMessageBelowArrow true
   skinparam participant {
       BackgroundColor #E8F5E9
       BorderColor #388E3C
   }
   skinparam database {
       BackgroundColor #FFF3E0
       BorderColor #F57C00
   }
   skinparam actor {
       BackgroundColor #1976D2
   }

   actor "Usuario" as U
   participant "Frontend\n(React)" as FE #E3F2FD
   participant "AuthController\n(DRF)" as AC #E8F5E9
   participant "AuthService" as AS #E8F5E9
   participant "UserRepository" as UR #E8F5E9
   participant "SessionService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a /login
   activate FE
   FE --> U: 2. Muestra formulario

   U -> FE: 3. Ingresa credenciales
   FE -> FE: 4. Validacion client-side

   FE -> AC: 5. POST /api/auth/login\n{username, password}
   activate AC

   AC -> AS: 6. authenticate(username, password)
   activate AS

   AS -> UR: 7. findByUsername(username)
   activate UR
   UR -> DB: SELECT * FROM users\nWHERE username = ?
   DB --> UR: User record
   deactivate UR

   AS -> AS: 8. checkAccountLocked()
   note right: BR_015:\nVerifica intentos fallidos

   AS -> AS: 9. bcrypt.checkpw(password, hash)

   AS -> AS: 10. validateUserActive()

   AS -> SS: 11. invalidatePreviousSessions(userId)
   activate SS
   note right: BR_005:\nSesion unica
   SS -> DB: UPDATE sessions\nSET active = false
   deactivate SS

   AS -> AS: 12. generateJWT(user)
   note right: Claims: user_id,\nusername, exp, iat

   AS -> AS: 13. resetFailedAttempts(userId)

   AS -> AUD: 14. logEvent(LOGIN, userId, SUCCESS)
   activate AUD
   note right: BR_008:\nAuditoria
   AUD -> DB: INSERT INTO audit_log
   deactivate AUD

   AS --> AC: 15. {token, user}
   deactivate AS

   AC --> FE: 16. 200 OK\n{access_token, token_type, expires_in}
   deactivate AC

   FE -> FE: 17. localStorage.setItem('token', token)
   FE --> U: 18. Redirect /dashboard
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Usuario Olvido Password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 2 del flujo normal

**Condicion:** Usuario hace clic en enlace "Olvide mi password"

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 2.1
     - Sistema navega a UC-003 Recuperar Password
   * - 2.2
     - Fin del UC-001 (continua en UC-003)

**Retorno:** No retorna (flujo termina)

7.2 FA-2: Credenciales Incorrectas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 8 del flujo normal

**Condicion:** Password no coincide con hash almacenado

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 8.1
     - Sistema incrementa contador de intentos fallidos
   * - 8.2
     - Sistema registra intento fallido en auditoria
   * - 8.3
     - Sistema muestra mensaje "Credenciales incorrectas"
   * - 8.4
     - Sistema retorna a paso 2 (mostrar formulario)

**Retorno:** Paso 2 del flujo normal

7.3 FA-3: Cuenta Bloqueada por Intentos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 6 del flujo normal

**Condicion:** Usuario tiene >= 5 intentos fallidos en ultimos 30 min

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 6.1
     - Sistema calcula tiempo restante de bloqueo
   * - 6.2
     - Sistema muestra "Cuenta bloqueada. Intente en X minutos"
   * - 6.3
     - Fin del caso de uso

**Retorno:** No retorna (flujo termina)

----

8. Excepciones
--------------

8.1 EX-1: Usuario No Existe
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Username no encontrado en base de datos

**Accion del Sistema:** Muestra mensaje generico (no revela si usuario existe)

**Mensaje al Usuario:** "Credenciales incorrectas"

8.2 EX-2: Usuario Inactivo
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario tiene estado diferente de ACTIVO

**Accion del Sistema:** Rechaza login, registra en auditoria

**Mensaje al Usuario:** "Cuenta inactiva. Contacte al administrador"

8.3 EX-3: Error de Conexion a BD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** No se puede conectar a PostgreSQL

**Accion del Sistema:** Registra error en logs tecnicos

**Mensaje al Usuario:** "Error del sistema. Intente nuevamente"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-001 Iniciar Sesion
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

   :Usuario accede a /login;

   :Sistema muestra formulario;

   :Usuario ingresa credenciales;

   :Validar formato de campos;

   if (Formato valido?) then (si)

       :Buscar usuario en BD;

       if (Usuario existe?) then (si)

           :Verificar bloqueo BR_015;

           if (Cuenta bloqueada?) then (si)
               #FFCDD2:Mostrar mensaje\n"Cuenta bloqueada";
               stop
           else (no)

               :Verificar password\n(bcrypt);

               if (Password correcto?) then (si)

                   if (Usuario ACTIVO?) then (si)
                       #C8E6C9:Invalidar sesiones previas\n(BR_005);
                       :Generar token JWT;
                       :Resetear intentos fallidos;
                       #C8E6C9:Registrar en auditoria\n(BR_008);
                       :Retornar token;
                       #C8E6C9:Redirigir a dashboard;
                       stop
                   else (no)
                       #FFCDD2:Mostrar "Cuenta inactiva";
                       stop
                   endif

               else (no)
                   #FFE0B2:Incrementar intentos fallidos;
                   :Registrar intento fallido;

                   if (Intentos >= 5?) then (si)
                       #FFCDD2:Bloquear cuenta 30 min;
                   else (no)
                   endif

                   #FFE0B2:Mostrar "Credenciales\nincorrectas";
               endif

           endif

       else (no)
           #FFE0B2:Mostrar "Credenciales\nincorrectas";
           note right: No revelar si\nusuario existe
       endif

   else (no)
       #FFE0B2:Mostrar error de formato;
   endif

   :Volver a mostrar formulario;

   stop
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
     - Paso 10: Al autenticar exitosamente, se invalidan todas las sesiones previas del usuario
   * - BR_008
     - Auditoria de Accesos
     - Paso 13: Todo login exitoso se registra en audit_log con timestamp, user_id, IP, user-agent
   * - BR_015
     - Bloqueo por Intentos Fallidos
     - Paso 6: Si hay >= 5 intentos fallidos en 30 min, cuenta se bloquea temporalmente

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-001.01
     - Sistema DEBE mostrar formulario con campos username y password
   * - FR-001.02
     - Sistema DEBE validar formato username (3-50 caracteres alfanumericos)
   * - FR-001.03
     - Sistema DEBE validar formato password (8-128 caracteres)
   * - FR-001.04
     - Sistema DEBE verificar credenciales contra BD usando bcrypt
   * - FR-001.05
     - Sistema DEBE validar que usuario tenga estado ACTIVO
   * - FR-001.06
     - Sistema DEBE verificar bloqueo por intentos fallidos (BR_015)
   * - FR-001.07
     - Sistema DEBE incrementar contador de intentos fallidos si falla
   * - FR-001.08
     - Sistema DEBE invalidar sesiones previas del usuario (BR_005)
   * - FR-001.09
     - Sistema DEBE generar token JWT con claims user_id, username, exp
   * - FR-001.10
     - Sistema DEBE retornar token en response JSON
   * - FR-001.11
     - Sistema DEBE registrar evento LOGIN en auditoria (BR_008)
   * - FR-001.12
     - Sistema DEBE resetear contador de intentos tras login exitoso

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_005 (Sesion Unica), BR_008 (Auditoria), BR_015 (Bloqueo)
   * - **FR Derivados**
     - FR-001.01 a FR-001.12 (12 requerimientos)
   * - **UC Relacionados**
     - UC-002 (Cerrar Sesion), UC-003 (Recuperar Password)
   * - **Actores RBAC**
     - Todos (cualquier usuario puede autenticarse)
   * - **Funciones RBAC**
     - No aplica (acceso publico pre-autenticacion)

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
