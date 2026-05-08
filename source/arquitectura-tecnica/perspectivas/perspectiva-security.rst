.. meta::
 :artefacto: AT_PERSPECTIVA_SECURITY
 :tipo: Perspectiva Arquitectonica — Security
 :dominio: arquitectura_tecnica
 :subdominio: Perspectivas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-perspectiva-security:

=====================
Perspectiva Security
=====================

Analisis transversal de la propiedad de calidad **seguridad** en el sistema IACT.
Asegura el acceso controlado a los recursos sensibles: datos de ciudadanos, BD
Operativa IVR y funciones RBAC del sistema.

Esta perspectiva se aplica a las vistas donde la seguridad tiene impacto
arquitectonico directo: Functional, Information, Deployment y Operational.

Aplicacion a vistas
=====================

Vista Functional (Use Case View)
------------------------------------

El acceso a todas las operaciones del sistema esta controlado por RBAC.
No existe endpoint funcional sin funcion atomica asociada.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Tactica
   - Implementacion en IACT
 * - **Autenticacion**
   - JWT emitido por UC-AUTH-01. Token valido durante la sesion activa
     (CNST-002: tiempo maximo configurable). Sin sesion activa = sin acceso.
 * - **Autorizacion granular**
   - 64 funciones atomicas activas organizadas en AccessGroups (AGR-001..012).
     Cada peticion verifica la funcion atomica correspondiente antes de
     ejecutarse. Permisos temporales con rango ``granted_at..expires_at``
     (CNST-031: maximo 6 meses, justificacion documentada).
 * - **Sesion unica**
   - CNST-003: un usuario solo puede tener una sesion activa simultanea.
     Nueva autenticacion invalida la sesion anterior.
 * - **No compartir tokens**
   - CNST-004: tokens JWT no son compartibles. El logout invalida
     el token del usuario (UC-AUTH-04).
 * - **Separacion de funciones**
   - CNST-030: enforcement de separacion en tiempo de asignacion. No es posible
     asignar a un usuario dos funciones en conflicto definidas como
     par de separacion.

Vista Information (Domain Model)
------------------------------------

El control de acceso se implementa a nivel de dato, no solo de endpoint.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Entidad
   - Control de acceso
 * - **User (cuenta)**
   - Solo AGR_ADMIN puede crear, modificar o desactivar. BR-009: nunca
     eliminar — solo desactivar (estado INACTIVE/BLOCKED).
 * - **AuditEvent**
   - CNST-025: append-only. Ninguna entidad del dominio puede modificar
     o eliminar registros de auditoria una vez creados.
 * - **ExceptionalPermission**
   - Solo AGR_ADMIN puede otorgar. Requiere rango temporal obligatorio
     (CNST-031). El sistema verifica automaticamente la expiracion.
 * - **Session**
   - CNST-002: token activo con tiempo maximo de sesion. AGR_ADMIN puede
     cerrar sesiones de otros usuarios (``view_all_active_sessions``).
 * - **BD Operativa IVR**
   - CNST-007: solo credenciales de lectura (GRANT SELECT). P-01: el
     sistema IACT nunca escribe en la BD del IVR. Invariante de diseno.

Vista Deployment (+1)
-----------------------

La distribucion fisica implementa aislamiento de credenciales y separacion
de redes entre la BD propia y la BD Operativa IVR.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Elemento
   - Tactica de seguridad
 * - **Credenciales BD propia**
   - Variables de entorno (``DATABASE_URL``). No hardcoded en codigo.
     Permisos: CREATE TABLE (solo para migraciones), lectura/escritura
     durante operacion normal.
 * - **Credenciales IVR (MariaDB)**
   - Variables de entorno separadas (``IVR_DATABASE_URL``). Solo lectura
     (GRANT SELECT). P-01: si estas credenciales permiten escritura, el
     despliegue viola CNST-007 y debe rechazarse.
 * - **SECRET_KEY (JWT)**
   - Variable de entorno. Nunca comiteada en codigo fuente.
     ``DEBUG=False`` en produccion — impide exposicion de stack traces.
 * - **Aislamiento de red**
   - La BD Operativa IVR no es accesible directamente desde internet.
     Solo el proceso ETL accede a ella desde la red interna.

Vista Operational
-------------------

La administracion operacional implementa controles de seguridad activos.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Operacion
   - Control de seguridad
 * - **Alta de usuario**
   - Asignacion de AccessGroup en el momento de creacion Separacion de deberes verificada
     automaticamente. AuditEvent generado (CNST-025).
 * - **Permisos temporales**
   - Expiracion automatica. AGR_ADMIN puede revocar antes del vencimiento.
     Toda concesion y revocacion genera AuditEvent.
 * - **Incidente de sesion**
   - AGR_ADMIN puede cerrar cualquier sesion activa inmediatamente
     (``view_all_active_sessions``). El token queda invalidado.

Diagrama — control de acceso RBAC
====================================

.. uml::
 :caption: Figura — Flujo de verificacion de acceso RBAC en cada peticion

 @startuml

 skinparam ArrowColor #444444
 skinparam ActivityBorderColor #333333
 skinparam ActivityBackgroundColor #F5F5F5
 skinparam ActivityDiamondBackgroundColor #FFF9C4
 skinparam shadowing false

 start

 :Peticion HTTP con JWT;

 if (¿JWT valido y no expirado?) then (si)
   :Extraer user_id del token;
   if (¿Sesion activa en BD?) then (si)
     :Identificar funcion atomica requerida\npor el endpoint;
     if (¿Usuario tiene la funcion?) then (si)
       if (¿Permiso temporal expirado?) then (no)
         :Ejecutar operacion;
         :Generar AuditEvent (CNST-025);
       else (si)
         :403 Forbidden\n(permiso temporal expirado);
       endif
     else (no)
       :403 Forbidden\n(funcion no asignada);
     endif
   else (no)
     :401 Unauthorized\n(sesion inactiva);
   endif
 else (no)
   :401 Unauthorized\n(JWT invalido o expirado);
 endif

 stop

 @enduml

Restricciones y principios
============================

.. list-table::
 :header-rows: 1
 :widths: 15 85

 * - Ref
   - Descripcion
 * - **P-01**
   - El sistema IACT nunca escribe en la BD Operativa IVR (MariaDB).
     Solo lectura. Invariante de diseno con impacto en seguridad.
 * - **CNST-002**
   - Tiempo maximo de sesion configurable. Sin actividad = expiracion.
 * - **CNST-003**
   - Un usuario, una sesion activa. Nueva autenticacion invalida la anterior.
 * - **CNST-004**
   - Tokens JWT no son compartibles ni reutilizables tras logout.
 * - **CNST-007**
   - Credenciales IVR con GRANT SELECT exclusivo. No credenciales de escritura.
 * - **CNST-030**
   - Separacion evaluada en tiempo de asignacion. Bloquea combinaciones de funciones
     en conflicto para el mismo usuario.
 * - **CNST-031**
   - Permisos temporales requieren rango ``granted_at..expires_at``
     (maximo 6 meses) y justificacion documentada.

.. seealso::

 :doc:`/arquitectura-tecnica/use-case-view/index`
 :doc:`/arquitectura-tecnica/domain-model/index`
 :doc:`/arquitectura-tecnica/operational-view/system-administration`
 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/perspectivas-arquitectonicas`
