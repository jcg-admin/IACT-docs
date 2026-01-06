.. meta::
   :artefacto: UC_004
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/auth
   :modulo: MOD_Auth
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-004:

==============================================================================
UC-004: Cambiar Password Propio
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
     - UC-004
   * - **Nombre**
     - Cambiar Password Propio
   * - **Actor Primario**
     - Usuario autenticado
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

Permite a un usuario autenticado cambiar su propio password, validando el
password actual y aplicando politicas de complejidad al nuevo password.
Tras el cambio, se invalidan todas las sesiones activas y se registra
el evento en auditoria (BR_008).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-004 Cambiar Password Propio
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
       usecase "UC-004:\nCambiar\nPassword" as UC004
       usecase "Validar\nComplejidad" as VC
       usecase "Invalidar\nSesiones" as INV
       usecase "Registrar\nEvento" as REG
   }

   U --> UC004
   UC004 ..> VC : <<include>>
   UC004 ..> INV : <<include>>
   UC004 ..> REG : <<include>>
   UC004 --> SA
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario tiene sesion activa (token JWT valido)
2. Usuario conoce su password actual
3. Usuario accede desde menu de perfil o forzado por sistema

4.2 Trigger
^^^^^^^^^^^

- Voluntario: Usuario selecciona "Cambiar Password" en menu de perfil
- Forzado: Sistema detecta flag force_password_change = true tras login

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Nuevo hash de password almacenado en BD (bcrypt, cost >= 12)
2. Flag force_password_change desactivado (si estaba activo)
3. Todas las sesiones del usuario invalidadas
4. Evento PASSWORD_CHANGE registrado en auditoria (BR_008)
5. Usuario redirigido a login para nueva autenticacion

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Password actual nunca se revela en logs
2. Nuevo password cumple politicas de complejidad
3. Cambio es atomico (todo o nada)

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
     - Accede a opcion "Cambiar Password"
     -
   * - 2
     -
     - Muestra formulario con 3 campos
   * - 3
     - Ingresa password actual
     -
   * - 4
     - Ingresa nuevo password
     -
   * - 5
     - Ingresa confirmacion de nuevo password
     -
   * - 6
     - Presiona "Cambiar Password"
     -
   * - 7
     -
     - Valida que password actual sea correcto
   * - 8
     -
     - Valida complejidad del nuevo password
   * - 9
     -
     - Valida que nuevo password coincida con confirmacion
   * - 10
     -
     - Valida que nuevo password sea diferente al actual
   * - 11
     -
     - Genera hash con bcrypt (cost >= 12)
   * - 12
     -
     - Actualiza password_hash en BD
   * - 13
     -
     - Desactiva flag force_password_change
   * - 14
     -
     - Invalida todas las sesiones del usuario
   * - 15
     -
     - Registra evento PASSWORD_CHANGE en auditoria
   * - 16
     -
     - Muestra mensaje de exito
   * - 17
     -
     - Redirige a pantalla de login

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-004 Cambiar Password
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
   participant "PasswordService" as PS #E8F5E9
   participant "UserRepository" as UR #E8F5E9
   participant "SessionService" as SS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   U -> FE: 1. Accede a "Cambiar Password"
   activate FE
   FE --> U: 2. Formulario (actual, nuevo, confirmar)

   U -> FE: 3. Completa formulario
   FE -> FE: 4. Validacion client-side\n(longitud, coincidencia)

   FE -> AC: 5. PUT /api/auth/password\n{current, new, confirm}\nAuthorization: Bearer {token}
   activate AC

   AC -> PS: 6. changePassword(userId, current, new)
   activate PS

   PS -> UR: 7. getPasswordHash(userId)
   activate UR
   UR -> DB: SELECT password_hash FROM users
   DB --> UR: {password_hash}
   deactivate UR

   PS -> PS: 8. bcrypt.checkpw(current, hash)
   note right: Verifica password actual

   PS -> PS: 9. validateComplexity(newPassword)
   note right: Min 8 chars, mayus,\nminus, numero, especial

   PS -> PS: 10. validateNotSameAsCurrent()

   PS -> PS: 11. bcrypt.hashpw(newPassword, cost=12)

   PS -> UR: 12. updatePassword(userId, newHash)
   UR -> DB: UPDATE users SET\npassword_hash = ?,\nforce_password_change = false,\npassword_changed_at = NOW()

   PS -> SS: 13. invalidateAllSessions(userId)
   activate SS
   SS -> DB: UPDATE sessions SET active=false\nWHERE user_id = ?
   SS -> DB: INSERT INTO token_blacklist\n(SELECT token FROM sessions...)
   deactivate SS

   PS -> AUD: 14. logEvent(PASSWORD_CHANGE, userId)
   activate AUD
   AUD -> DB: INSERT INTO audit_log
   note right: BR_008
   deactivate AUD

   PS --> AC: 15. {success: true}
   deactivate PS

   AC --> FE: 16. 200 OK {message}
   deactivate AC

   FE --> U: 17. "Password cambiado exitosamente"
   FE -> FE: 18. Limpiar token local
   FE --> U: 19. Redirect /login
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Password Actual Incorrecto
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 7 del flujo normal

**Condicion:** Password actual no coincide con hash almacenado

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 7.1
     - Sistema muestra error "Password actual incorrecto"
   * - 7.2
     - Usuario permanece en formulario para reintentar

**Retorno:** Paso 3 del flujo normal

7.2 FA-2: Nuevo Password No Cumple Complejidad
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 8 del flujo normal

**Condicion:** Nuevo password no cumple politicas de complejidad

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 8.1
     - Sistema muestra requisitos no cumplidos
   * - 8.2
     - Mensaje detalla: "Debe incluir mayuscula, minuscula, numero, simbolo"

**Retorno:** Paso 4 del flujo normal

7.3 FA-3: Confirmacion No Coincide
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 9 del flujo normal

**Condicion:** Campo confirmacion != campo nuevo password

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 9.1
     - Sistema muestra "Las contraseñas no coinciden"

**Retorno:** Paso 5 del flujo normal

7.4 FA-4: Cambio Forzado Post-Login
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Antes del paso 1

**Condicion:** flag force_password_change = true (post UC-003)

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 0.1
     - Sistema detecta flag tras login exitoso
   * - 0.2
     - Sistema redirige automaticamente a formulario de cambio
   * - 0.3
     - Usuario no puede navegar hasta cambiar password

**Retorno:** Paso 2 del flujo normal

----

8. Excepciones
--------------

8.1 EX-1: Nuevo Password Igual al Actual
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Usuario intenta usar el mismo password

**Accion del Sistema:** Rechaza el cambio

**Mensaje al Usuario:** "El nuevo password debe ser diferente al actual"

8.2 EX-2: Sesion Expirada Durante Cambio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Token expira mientras usuario completa formulario

**Accion del Sistema:** Retorna 401 Unauthorized

**Mensaje al Usuario:** "Sesion expirada. Inicie sesion nuevamente"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-004 Cambiar Password
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

   if (force_password_change?) then (si)
       :Redirigir automaticamente\nal formulario;
       note right: Post UC-003
   else (no)
       :Usuario accede a\n"Cambiar Password";
   endif

   :Mostrar formulario\n(actual, nuevo, confirmar);

   :Usuario completa campos;

   :Validar password actual;

   if (Password actual correcto?) then (si)

       :Validar complejidad;

       if (Cumple complejidad?) then (si)

           if (Nuevo = Confirmacion?) then (si)

               if (Nuevo != Actual?) then (si)

                   :Generar hash bcrypt;
                   :Actualizar password en BD;
                   :Desactivar force_password_change;
                   #C8E6C9:Invalidar todas las sesiones;
                   #C8E6C9:Registrar en auditoria\n(BR_008);
                   :Mostrar mensaje exito;
                   :Redirigir a login;
                   stop

               else (no)
                   #FFE0B2:Error: "Debe ser\ndiferente al actual";
               endif

           else (no)
               #FFE0B2:Error: "No coinciden";
           endif

       else (no)
           #FFE0B2:Error: Mostrar requisitos\nno cumplidos;
       endif

   else (no)
       #FFE0B2:Error: "Password\nactual incorrecto";
   endif

   :Volver al formulario;

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
   * - BR_008
     - Auditoria de Accesos
     - Paso 15: Evento PASSWORD_CHANGE registrado en audit_log

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-004.01
     - Sistema DEBE mostrar opcion "Cambiar Password" en menu de perfil
   * - FR-004.02
     - Sistema DEBE mostrar formulario con 3 campos (actual, nuevo, confirmar)
   * - FR-004.03
     - Sistema DEBE validar password actual contra BD (bcrypt)
   * - FR-004.04
     - Sistema DEBE validar complejidad: min 8 chars, mayus, minus, num, simbolo
   * - FR-004.05
     - Sistema DEBE validar que nuevo password coincida con confirmacion
   * - FR-004.06
     - Sistema DEBE validar que nuevo password sea diferente al actual
   * - FR-004.07
     - Sistema DEBE hashear nuevo password con bcrypt cost >= 12
   * - FR-004.08
     - Sistema DEBE desactivar flag force_password_change
   * - FR-004.09
     - Sistema DEBE invalidar todas las sesiones del usuario
   * - FR-004.10
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
     - BR_008 (Auditoria de Accesos)
   * - **FR Derivados**
     - FR-004.01 a FR-004.10 (10 requerimientos)
   * - **UC Relacionados**
     - UC-001 (Iniciar Sesion), UC-003 (Recuperar Password)
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