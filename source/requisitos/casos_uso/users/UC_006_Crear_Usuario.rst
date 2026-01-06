.. meta::
   :artefacto: UC_006
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/users
   :modulo: MOD_Users
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-006:

==============================================================================
UC-006: Crear Usuario
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
     - UC-006
   * - **Nombre**
     - Crear Usuario
   * - **Actor Primario**
     - Administrador de Usuarios
   * - **Actores Secundarios**
     - Sistema de Auditoria
   * - **Modulo**
     - MOD_Users
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Alta
   * - **BReq Origen**
     - BReq-004: Cumplimiento de Seguridad

----

2. Descripcion
--------------

Permite a un administrador crear nuevas cuentas de usuario en el sistema IACT.
El nuevo usuario recibe un password temporal que debe cambiar en su primer
login. El sistema valida unicidad de username y email, y registra la creacion
en auditoria (BR_008).

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-006 Crear Usuario
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

   actor "Administrador\nUsuarios" as ADM
   actor "Sistema\nAuditoria" as SA #LightGray
   actor "Nuevo\nUsuario" as NU #LightGray

   rectangle "MOD_Users" {
       usecase "UC-006:\nCrear\nUsuario" as UC006
       usecase "Generar\nPassword\nTemporal" as GPT
       usecase "Validar\nDatos" as VD
       usecase "Registrar\nEvento" as REG
       usecase "UC-010:\nAsignar\nFunciones" as UC010
   }

   ADM --> UC006
   UC006 ..> GPT : <<include>>
   UC006 ..> VD : <<include>>
   UC006 ..> REG : <<include>>
   UC006 .> UC010 : <<extends>>\n[asignar permisos]
   UC006 --> SA
   UC006 --> NU : notifica
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Administrador tiene sesion activa
2. Administrador tiene funcion USR-001 (Crear Usuario)
3. Administrador pertenece a agrupador con permiso de gestion de usuarios

4.2 Trigger
^^^^^^^^^^^

Administrador selecciona "Nuevo Usuario" en modulo de gestion de usuarios.

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Usuario creado con estado ACTIVO
2. Password temporal generado y mostrado al administrador
3. Flag force_password_change = true
4. Evento USER_CREATED registrado en auditoria (BR_008)
5. Usuario puede autenticarse con password temporal

4.4 Garantias Minimas
^^^^^^^^^^^^^^^^^^^^^

1. Username y email son unicos en el sistema
2. Password temporal cumple politicas de complejidad
3. Operacion es atomica (todo o nada)

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
     - Accede a "Gestion de Usuarios"
     -
   * - 2
     -
     - Verifica permiso USR-001
   * - 3
     - Hace clic en "Nuevo Usuario"
     -
   * - 4
     -
     - Muestra formulario de creacion
   * - 5
     - Ingresa datos del usuario (*)
     -
   * - 6
     - Presiona "Crear Usuario"
     -
   * - 7
     -
     - Valida formato de campos
   * - 8
     -
     - Valida unicidad de username
   * - 9
     -
     - Valida unicidad de email
   * - 10
     -
     - Genera password temporal (12 chars)
   * - 11
     -
     - Hashea password con bcrypt
   * - 12
     -
     - Crea registro en tabla users
   * - 13
     -
     - Configura pregunta de seguridad por defecto
   * - 14
     -
     - Registra USER_CREATED en auditoria (BR_008)
   * - 15
     -
     - Muestra password temporal al administrador
   * - 16
     -
     - Muestra mensaje de exito

(*) Datos: username, email, nombre, apellido, telefono (opcional)

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - Flujo Normal UC-006 Crear Usuario
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

   actor "Admin\nUsuarios" as ADM
   participant "Frontend\n(React)" as FE #E3F2FD
   participant "UserController\n(DRF)" as UC #E8F5E9
   participant "RBACService" as RBAC #E8F5E9
   participant "UserService" as US #E8F5E9
   participant "PasswordService" as PS #E8F5E9
   participant "AuditService" as AUD #E8F5E9
   database "PostgreSQL" as DB #FFF3E0

   ADM -> FE: 1. Clic "Nuevo Usuario"
   activate FE
   FE --> ADM: 2. Formulario de creacion

   ADM -> FE: 3. Completa datos y envia
   FE -> FE: 4. Validacion client-side

   FE -> UC: 5. POST /api/users\n{username, email, nombre, apellido}\nAuthorization: Bearer {token}
   activate UC

   UC -> RBAC: 6. checkPermission(adminId, 'USR-001')
   activate RBAC
   RBAC -> DB: SELECT * FROM user_functions\nWHERE user_id=? AND function='USR-001'
   DB --> RBAC: {authorized: true}
   RBAC --> UC: authorized
   deactivate RBAC

   UC -> US: 7. createUser(userData)
   activate US

   US -> US: 8. validateFields(userData)

   US -> DB: 9. SELECT id FROM users\nWHERE username = ?
   DB --> US: null (no existe)

   US -> DB: 10. SELECT id FROM users\nWHERE email = ?
   DB --> US: null (no existe)

   US -> PS: 11. generateTempPassword()
   activate PS
   PS --> US: tempPassword (12 chars)
   deactivate PS

   US -> PS: 12. hashPassword(tempPassword)
   PS --> US: hashedPassword

   US -> DB: 13. INSERT INTO users\n(username, email, nombre, apellido,\npassword_hash, status='ACTIVO',\nforce_password_change=true,\ncreated_at, created_by)
   DB --> US: {id: newUserId}

   US -> AUD: 14. logEvent(USER_CREATED,\nadminId, newUserId, userData)
   activate AUD
   AUD -> DB: INSERT INTO audit_log
   note right: BR_008:\nRegistra quien creo\nel usuario
   AUD --> US: OK
   deactivate AUD

   US --> UC: 15. {user, tempPassword}
   deactivate US

   UC --> FE: 16. 201 Created\n{user, temp_password}
   deactivate UC

   FE --> ADM: 17. Modal: "Usuario creado"\n"Password temporal: XXXX"
   note right: Admin debe comunicar\npassword al nuevo usuario\n(BR_004)
   deactivate FE
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Username Ya Existe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 8 del flujo normal

**Condicion:** Username ya registrado en sistema

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 8.1
     - Sistema detecta username duplicado
   * - 8.2
     - Sistema muestra "El username ya esta en uso"
   * - 8.3
     - Admin corrige username

**Retorno:** Paso 5 del flujo normal

7.2 FA-2: Email Ya Existe
^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 9 del flujo normal

**Condicion:** Email ya registrado en sistema

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 9.1
     - Sistema detecta email duplicado
   * - 9.2
     - Sistema muestra "El email ya esta registrado"
   * - 9.3
     - Admin corrige email

**Retorno:** Paso 5 del flujo normal

7.3 FA-3: Asignar Funciones Inmediatamente
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Punto de bifurcacion:** Paso 16 del flujo normal

**Condicion:** Admin desea asignar funciones al nuevo usuario

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Paso
     - Descripcion
   * - 16.1
     - Admin hace clic en "Asignar Funciones"
   * - 16.2
     - Sistema navega a UC-010 con usuario preseleccionado

**Retorno:** Continua en UC-010

----

8. Excepciones
--------------

8.1 EX-1: Sin Permiso de Creacion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Administrador no tiene funcion USR-001

**Accion del Sistema:** Retorna 403 Forbidden

**Mensaje al Usuario:** "No tiene permisos para crear usuarios"

8.2 EX-2: Error de Base de Datos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Condicion:** Falla INSERT en tabla users

**Accion del Sistema:** Rollback de transaccion, registra error

**Mensaje al Usuario:** "Error al crear usuario. Intente nuevamente"

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - Flujos y Decisiones UC-006 Crear Usuario
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

   :Admin accede a\n"Nuevo Usuario";

   :Verificar permiso USR-001;

   if (Tiene permiso?) then (si)

       :Mostrar formulario;

       :Admin ingresa datos;

       :Validar formato de campos;

       if (Formato valido?) then (si)

           :Verificar unicidad username;

           if (Username disponible?) then (si)

               :Verificar unicidad email;

               if (Email disponible?) then (si)

                   #C8E6C9:Generar password temporal;
                   :Hashear con bcrypt;
                   :Crear usuario en BD;
                   :Configurar force_password_change;
                   #C8E6C9:Registrar en auditoria\n(BR_008);
                   :Mostrar password temporal;
                   #C8E6C9:Usuario creado exitosamente;

                   if (Asignar funciones ahora?) then (si)
                       :Ir a UC-010;
                   else (no)
                   endif

                   stop

               else (no)
                   #FFE0B2:Error: "Email ya registrado";
               endif

           else (no)
               #FFE0B2:Error: "Username en uso";
           endif

       else (no)
           #FFE0B2:Mostrar errores de validacion;
       endif

       :Volver al formulario;

   else (no)
       #FFCDD2:403 Forbidden;
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
     - Paso 15: Password se muestra en pantalla, admin lo comunica manualmente
   * - BR_008
     - Auditoria de Accesos
     - Paso 14: USER_CREATED registrado con admin creador y datos del usuario

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-006.01
     - Sistema DEBE verificar permiso USR-001 antes de mostrar formulario
   * - FR-006.02
     - Sistema DEBE mostrar formulario con campos: username, email, nombre, apellido, telefono
   * - FR-006.03
     - Sistema DEBE validar formato de username (3-50 chars, alfanumerico)
   * - FR-006.04
     - Sistema DEBE validar formato de email (RFC 5322)
   * - FR-006.05
     - Sistema DEBE validar unicidad de username
   * - FR-006.06
     - Sistema DEBE validar unicidad de email
   * - FR-006.07
     - Sistema DEBE generar password temporal de 12 caracteres complejo
   * - FR-006.08
     - Sistema DEBE crear usuario con estado ACTIVO
   * - FR-006.09
     - Sistema DEBE activar flag force_password_change
   * - FR-006.10
     - Sistema DEBE registrar evento en auditoria (BR_008)
   * - FR-006.11
     - Sistema DEBE mostrar password temporal al administrador

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Origen (BReq)**
     - BReq-004: Cumplimiento de Seguridad
   * - **BR Aplicables**
     - BR_004 (Comunicaciones), BR_008 (Auditoria)
   * - **FR Derivados**
     - FR-006.01 a FR-006.11 (11 requerimientos)
   * - **UC Relacionados**
     - UC-010 (Asignar Funciones)
   * - **Actores RBAC**
     - AGR-007: admin_usuarios
   * - **Funciones RBAC**
     - USR-001: Crear Usuario

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