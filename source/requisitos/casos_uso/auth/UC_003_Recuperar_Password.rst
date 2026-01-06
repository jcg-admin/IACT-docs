.. meta::
   :artefacto: UC_003
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/auth
   :modulo: MOD_Auth
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-003:

==============================================================================
UC-003: Recuperar Password
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
     - UC-003
   * - **Nombre**
     - Recuperar Password
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

Permite a un usuario que olvido su password recuperar el acceso al sistema
mediante verificacion de pregunta de seguridad. El sistema genera un password
temporal que se muestra en pantalla (BR_004: comunicaciones internas, sin email)
y fuerza su cambio en el siguiente login.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-003 Recuperar Password
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
       usecase "UC-003:\nRecuperar\nPassword" as UC003
       usecase "Verificar\nPregunta\nSeguridad" as VPS
       usecase "Generar\nPassword\nTemporal" as GPT
       usecase "Registrar\nEvento" as REG
       usecase "UC-001:\nIniciar\nSesion" as UC001
   }

   U --> UC003
   UC003 ..> VPS : <<include>>
   UC003 ..> GPT : <<include>>
   UC003 ..> REG : <<include>>
   UC003 --> SA
   UC003 .> UC001 : <<precedes>>
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene cuenta registrada en el sistema
2. Usuario configuro pregunta de seguridad previamente
3. Usuario no esta autenticado actualmente
4. Cuenta no esta bloqueada permanentemente

4.2 Trigger
^^^^^^^^^^^

Usuario hace clic en "Olvide mi password" en pantalla de login.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Password temporal generado y mostrado al usuario
2. Flag force_password_change activado en cuenta
3. Evento RECOVERY registrado en auditoria (BR_008)
4. Usuario puede autenticarse con password temporal

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Password original nunca se revela ni recupera
2. Intentos de recuperacion se limitan (max 3)
3. Password temporal cumple politicas de complejidad

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
     - Hace clic en "Olvide mi password"
     -
   * - 2
     -
     - Muestra formulario solicitando username
   * - 3
     - Ingresa su username
     -
   * - 4
     -
     - Valida que username exista en BD
   * - 5
     -
     - Muestra pregunta de seguridad del usuario
   * - 6
     - Ingresa respuesta a pregunta de seguridad
     -
   * - 7
     -
     - Valida respuesta (case-insensitive, trim)
   * - 8
     -
     - Genera password temporal (12 chars, complejo)
   * - 9
     -
     - Actualiza hash en BD con password temporal
   * - 10
     -
     - Activa flag force_password_change = true
   * - 11
     -
     - Registra evento RECOVERY en auditoria (BR_008)
   * - 12
     -
     - Muestra password temporal en pantalla (BR_004)
   * - 13
     - Copia/anota el password temporal
     -
   * - 14
     -
     - Muestra boton "Ir a Login"

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-003 Recuperar Password
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
   participant "RecoveryService" as RS #E8F5E9
   participant "UserRepository" as UR #E8F5E9
   participant "PasswordService" as PS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Clic "Olvide mi password"
   activate FE
   FE --> U: 2. Formulario: username

   U -> FE: 3. Ingresa username
   FE -> AC: 4. POST /api/auth/recovery/init\n{username}
   activate AC

   AC -> RS: 5. initRecovery(username)
   activate RS

   RS -> UR: 6. findByUsername(username)
   activate UR
   UR -> DB: SELECT id, security_question\nFROM users WHERE username=?
   DB --> UR: {id, security_question}
   deactivate UR

   RS --> AC: 7. {security_question}
   deactivate RS

   AC --> FE: 8. 200 OK {question}
   deactivate AC

   FE --> U: 9. Muestra pregunta de seguridad

   U -> FE: 10. Ingresa respuesta
   FE -> AC: 11. POST /api/auth/recovery/verify\n{username, answer}
   activate AC

   AC -> RS: 12. verifyAnswer(username, answer)
   activate RS

   RS -> UR: 13. getSecurityAnswer(username)
   UR -> DB: SELECT security_answer FROM users
   DB --> UR: {security_answer}

   RS -> RS: 14. compareAnswers(input, stored)
   note right: Normaliza: lowercase,\ntrim, sin acentos

   RS -> PS: 15. generateTempPassword()
   activate PS
   PS -> PS: 16. Genera 12 chars\n(A-Z, a-z, 0-9, !@#$%)
   PS --> RS: tempPassword
   deactivate PS

   RS -> PS: 17. hashPassword(tempPassword)
   PS --> RS: hashedPassword

   RS -> UR: 18. updatePassword(userId, hash, forceChange=true)
   UR -> DB: UPDATE users SET\npassword_hash=?,\nforce_password_change=true

   RS -> AUD: 19. logEvent(PASSWORD_RECOVERY, userId)
   activate AUD
   AUD -> DB: INSERT INTO audit_log
   note right: BR_008
   deactivate AUD

   RS --> AC: 20. {tempPassword}
   deactivate RS

   AC --> FE: 21. 200 OK {temp_password}
   deactivate AC

   FE --> U: 22. Muestra password temporal\n"Guarde este password"
   note right: BR_004:\nMostrar en pantalla,\nno enviar por email
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Usuario No Existe
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 4 del flujo normal

**Condicion:** Username no encontrado en BD

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 4.1
     - Sistema muestra mensaje generico (seguridad)
   * - 4.2
     - Mensaje: "Si el usuario existe, se mostrara la pregunta"
   * - 4.3
     - Sistema NO revela si usuario existe o no

**Retorno:** Fin del caso de uso

7.2 FA-2: Respuesta Incorrecta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 7 del flujo normal

**Condicion:** Respuesta no coincide con la almacenada

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.1
     - Sistema incrementa contador de intentos de recuperacion
   * - 7.2
     - Sistema muestra "Respuesta incorrecta. Intento X de 3"
   * - 7.3
     - Si intentos < 3, volver a paso 5
   * - 7.4
     - Si intentos >= 3, ir a FA-3

**Retorno:** Paso 5 o FA-3

7.3 FA-3: Maximo de Intentos Excedido
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 7.4 del FA-2

**Condicion:** Usuario excedio 3 intentos de respuesta

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.4.1
     - Sistema bloquea recuperacion por 30 minutos
   * - 7.4.2
     - Sistema registra intento fallido en auditoria
   * - 7.4.3
     - Sistema muestra "Demasiados intentos. Intente en 30 min"

**Retorno:** Fin del caso de uso

----

8. Excepciones
--------------

8.1 EX-1: Usuario Sin Pregunta de Seguridad
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario nunca configuro pregunta de seguridad

**Accion del Sistema:** Muestra mensaje indicando contactar administrador

**Mensaje al Usuario:** "Contacte al administrador para recuperar acceso"

8.2 EX-2: Cuenta Bloqueada Permanentemente
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Cuenta tiene estado BLOQUEADO (no temporal)

**Accion del Sistema:** Rechaza recuperacion

**Mensaje al Usuario:** "Cuenta bloqueada. Contacte al administrador"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-003 Recuperar Password
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

   :Usuario hace clic en\n"Olvide mi password";

   :Mostrar formulario username;

   :Usuario ingresa username;

   :Buscar usuario en BD;

   if (Usuario existe?) then (si)

       if (Tiene pregunta seguridad?) then (si)

           :Mostrar pregunta de seguridad;
           :Usuario ingresa respuesta;

           :Validar respuesta;

           if (Respuesta correcta?) then (si)

               #C8E6C9:Generar password temporal\n(12 caracteres);
               :Hashear con bcrypt;
               :Actualizar password en BD;
               :Activar force_password_change;
               #C8E6C9:Registrar en auditoria\n(BR_008);
               #C8E6C9:Mostrar password en pantalla\n(BR_004);
               :Mostrar "Ir a Login";
               stop

           else (no)
               :Incrementar intentos;

               if (Intentos >= 3?) then (si)
                   #FFCDD2:Bloquear recuperacion\n30 minutos;
                   stop
               else (no)
                   :Mostrar "Respuesta\nincorrecta";
                   note right: Volver a intentar
               endif

           endif

       else (no)
           #FFCDD2:Mostrar "Contacte\nadministrador";
           stop
       endif

   else (no)
       #FFE0B2:Mostrar mensaje generico;
       note right: No revelar si\nusuario existe
       stop
   endif

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
   * - BR_004
     - Comunicaciones Internas
     - Paso 12: Password temporal se muestra en pantalla, NO se envia por email
   * - BR_008
     - Auditoria de Accesos
     - Paso 11: Evento PASSWORD_RECOVERY registrado en audit_log

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-003.01
     - Sistema DEBE mostrar link "Olvide mi password" en pantalla de login
   * - FR-003.02
     - Sistema DEBE mostrar formulario para ingresar username
   * - FR-003.03
     - Sistema DEBE validar existencia de username sin revelar informacion
   * - FR-003.04
     - Sistema DEBE mostrar pregunta de seguridad del usuario
   * - FR-003.05
     - Sistema DEBE validar respuesta (case-insensitive, trim espacios)
   * - FR-003.06
     - Sistema DEBE limitar a 3 intentos de respuesta, bloqueando 30 min
   * - FR-003.07
     - Sistema DEBE generar password temporal de 12 caracteres complejo
   * - FR-003.08
     - Sistema DEBE mostrar password temporal en pantalla (BR_004)
   * - FR-003.09
     - Sistema DEBE activar flag force_password_change
   * - FR-003.10
     - Sistema DEBE registrar evento en auditoria (BR_008)

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_004 (Comunicaciones Internas), BR_008 (Auditoria)
   * - **FR Derivados**
     - FR-003.01 a FR-003.10 (10 requerimientos)
   * - **UC Relacionados**
     - UC-001 (Iniciar Sesion), UC-004 (Cambiar Password)
   * - **Actores RBAC**
     - No aplica (usuario no autenticado)
   * - **Funciones RBAC**
     - No aplica (acceso publico)

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