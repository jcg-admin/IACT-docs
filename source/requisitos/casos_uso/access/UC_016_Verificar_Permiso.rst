cat > /mnt/user-data/outputs/casos_uso_v2/access/UC_016_Verificar_Permiso.rst << 'EOF'
.. meta::
   :artefacto: UC_016
   :tipo: Caso de Uso
   :dominio: requisitos
   :subdominio: casos_uso/access
   :modulo: MOD_Access
   :estado: Aprobado
   :version: 2.0.0
   :fecha_creacion: 2026-01-06
   :autor: Equipo IACT

.. _uc-016:

==============================================================================
UC-016: Verificar Permisos de Usuario
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
     - UC-016
   * - **Nombre**
     - Verificar Permisos de Usuario
   * - **Actor Primario**
     - Sistema (invocado por otros modulos)
   * - **Actores Secundarios**
     - Cache Redis
   * - **Modulo**
     - MOD_Access
   * - **Complejidad**
     - Media
   * - **Prioridad**
     - Critica
   * - **BReq Origen**
     - BReq-004: Control de Acceso

----

2. Descripcion
--------------

Servicio interno que verifica si un usuario tiene una funcion especifica.
Implementa el nucleo del modelo RBAC consultando la cadena: Usuario ->
Roles -> Funciones. Utiliza cache para optimizar rendimiento (BR_033).
Invocado por decoradores/guards en cada endpoint protegido.

----

3. Diagrama de Caso de Uso
--------------------------

.. uml::
   :caption: Diagrama de Caso de Uso - UC-016 Verificar Permiso
   :align: center
   :scale: 90%

   @startuml
   left to right direction
   skinparam actorStyle awesome
   skinparam backgroundColor #FAFAFA
   skinparam usecase {
       BackgroundColor #E3F2FD
       BorderColor #1976D2
   }

   actor "Sistema\n(Modulos)" as SYS
   actor "Cache\nRedis" as CACHE #LightGray

   rectangle "MOD_Access" {
       usecase "UC-016:\nVerificar\nPermiso" as UC016
       usecase "Consultar\nCache" as CC
       usecase "Resolver\nRoles" as RR
       usecase "Resolver\nFunciones" as RF
       usecase "Actualizar\nCache" as AC
   }

   SYS --> UC016
   UC016 ..> CC : <<include>>
   UC016 ..> RR : <<include>>
   UC016 ..> RF : <<include>>
   UC016 ..> AC : <<include>>
   UC016 --> CACHE
   @enduml

----

4. Contexto
-----------

4.1 Precondiciones
^^^^^^^^^^^^^^^^^^

1. Usuario autenticado con sesion valida
2. Token JWT valido con userId
3. Cache Redis disponible (opcional, fallback a BD)

4.2 Trigger
^^^^^^^^^^^

Cualquier request a endpoint protegido con @RequireFunction(code).

4.3 Postcondiciones de Exito
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Retorna true/false segun tenga el permiso
2. Cache actualizado si hubo miss
3. Request continua o rechaza (403)

----

5. Flujo Normal
---------------

.. list-table::
   :widths: 8 46 46
   :header-rows: 1

   * - Paso
     - Sistema Cliente
     - Servicio de Permisos
   * - 1
     - Invoca hasPermission(userId, functionCode)
     -
   * - 2
     -
     - Consulta cache: permissions:{userId}
   * - 3
     -
     - [Cache Hit] Busca functionCode en set
   * - 4
     -
     - Retorna resultado
   * - 5
     - Permite/rechaza request
     -

----

6. Diagrama de Secuencia
------------------------

.. uml::
   :caption: Secuencia - UC-016 Verificar Permiso
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA
   skinparam sequenceMessageAlign center

   participant "API Guard" as GUARD #E3F2FD
   participant "PermissionService" as PS #E8F5E9
   participant "Redis" as REDIS #FFCDD2
   database "PostgreSQL" as DB #FFF3E0

   GUARD -> PS: 1. hasPermission(userId, 'RPT-001')
   activate PS

   PS -> REDIS: 2. GET permissions:{userId}

   alt Cache Hit
       REDIS --> PS: 3a. ['USR-001', 'RPT-001', 'RPT-002', ...]
       PS -> PS: 4a. functionCode IN cachedSet?
       PS --> GUARD: 5a. true
   else Cache Miss
       REDIS --> PS: 3b. null

       PS -> DB: 4b. SELECT DISTINCT f.code\nFROM functions f\nJOIN role_functions rf ON f.id = rf.function_id\nJOIN user_roles ur ON rf.role_id = ur.role_id\nWHERE ur.user_id = ?\nAND ur.valid_from <= NOW()\nAND (ur.valid_until IS NULL OR ur.valid_until >= NOW())\nAND f.status = 'ACTIVE'
       DB --> PS: [functionCodes]

       PS -> REDIS: 5b. SETEX permissions:{userId}\n{codes} TTL=300
       REDIS --> PS: OK

       PS -> PS: 6b. functionCode IN codes?
       PS --> GUARD: 7b. true/false
   end
   deactivate PS

   alt Tiene permiso
       GUARD -> GUARD: Continua request
   else Sin permiso
       GUARD --> GUARD: 403 Forbidden
   end
   @enduml

----

7. Flujos Alternos
------------------

7.1 FA-1: Cache Expirado
^^^^^^^^^^^^^^^^^^^^^^^^

Sistema recarga permisos desde BD y actualiza cache.

7.2 FA-2: Redis No Disponible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sistema consulta directamente a BD sin cache (degradacion graceful).

7.3 FA-3: Usuario Sin Roles
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retorna false para cualquier funcion.

----

8. Excepciones
--------------

8.1 EX-1: Usuario No Existe
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Accion:** Retorna false, log de advertencia.

8.2 EX-2: Error de Conexion BD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Accion:** Retorna false, log de error, alerta a monitoreo.

----

9. Diagrama de Actividad
------------------------

.. uml::
   :caption: Actividad - UC-016 Verificar Permiso
   :align: center

   @startuml
   skinparam backgroundColor #FAFAFA

   start
   :Recibe hasPermission(userId, code);

   :Consultar cache Redis;

   if (Cache hit?) then (si)
       :Obtener permisos cacheados;
   else (miss)
       :Consultar BD;

       if (BD disponible?) then (si)
           :Resolver roles activos;
           :Resolver funciones de roles;
           :Guardar en cache (TTL 5min);
       else (no)
           #FFCDD2:Log error;
           :Retornar false;
           stop
       endif
   endif

   if (code IN permisos?) then (si)
       #C8E6C9:Retornar true;
   else (no)
       #FFE0B2:Retornar false;
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
     - Aplicacion
   * - BR_033
     - Cache Permisos
     - TTL de 5 minutos para balance rendimiento/actualizacion
   * - BR_029
     - Vigencia Rol
     - Solo roles dentro de valid_from/valid_until

----

11. Requerimientos Funcionales Derivados
----------------------------------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - FR
     - Descripcion
   * - FR-016.01
     - Verificar permiso en menos de 10ms (con cache)
   * - FR-016.02
     - Implementar cache con TTL configurable
   * - FR-016.03
     - Fallback a BD si cache no disponible
   * - FR-016.04
     - Considerar vigencia temporal de roles
   * - FR-016.05
     - Solo evaluar funciones activas
   * - FR-016.06
     - Invalidar cache al modificar roles/funciones

----

12. Trazabilidad
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **BReq Origen**
     - BReq-004
   * - **BR Aplicables**
     - BR_029, BR_033
   * - **FR Derivados**
     - FR-016.01 a FR-016.06
   * - **UC Relacionados**
     - Todos los UC que requieren autorizacion

----

13. Historial de Cambios
------------------------

.. list-table::
   :widths: 12 12 76
   :header-rows: 1

   * - Version
     - Fecha
     - Cambios
   * - 2.0.0
     - 2026-01-06
     - Version completa. Cache Redis. Vigencia temporal.
