.. meta::
 :artefacto: AT_PERSPECTIVA_REGULATION
 :tipo: Perspectiva Arquitectonica — Regulation
 :dominio: arquitectura_tecnica
 :subdominio: Perspectivas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-perspectiva-regulation:

========================
Perspectiva Regulation
========================

Analisis transversal de la propiedad de calidad **conformidad regulatoria** en
el sistema IACT. Cubre auditoria de acceso, trazabilidad de acciones ciudadanas,
separacion de funciones y cumplimiento de restricciones institucionales.

IACT gestiona datos de ciudadanos y registros de llamadas IVR. Toda operacion
sobre estos datos debe ser auditable, trazable y conforme a los requisitos
regulatorios institucionales.

Aplicacion a vistas
=====================

Vista Functional (Use Case View)
------------------------------------

Las regulaciones imponen restricciones sobre que operaciones son permitidas
y como deben registrarse.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Requisito regulatorio
   - Implementacion en IACT
 * - **Auditoria de toda operacion**
   - CNST-025: toda operacion de escritura o acceso a datos sensibles
     genera un ``AuditEvent`` inmutable (append-only). Sin excepciones.
 * - **SoD institucional**
   - CNST-030: separacion de funciones aplicada en tiempo de asignacion.
     Los pares de funciones en conflicto (p. ej. crear + aprobar) no
     pueden coexistir en el mismo usuario.
 * - **Permisos temporales auditados**
   - CNST-031: toda concesion y revocacion de permiso temporal genera
     AuditEvent. La justificacion documentada es obligatoria.
 * - **Soft-delete obligatorio**
   - BR-009 v2.0.0: los usuarios y registros regulatorios no se eliminan.
     Se desactivan. El historial permanece para auditorias posteriores.
 * - **Exportacion auditada**
   - Los reportes exportados son registrados. AGR_AUDITOR tiene funcion
     ``export_audit_log`` restringida a su rol.

Vista Information (Domain Model)
------------------------------------

Los modelos de datos garantizan la trazabilidad regulatoria por diseno.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Entidad
   - Garantia regulatoria
 * - **AuditEvent**
   - Append-only por diseno (CNST-025). Campos obligatorios: usuario,
     accion, timestamp, entidad afectada, estado anterior y posterior.
     No modificable ni eliminable.
 * - **SeparationRule**
   - Pares de funciones en conflicto definidos explicitamente. El motor
     RBAC evalua estas reglas en cada asignacion (CNST-030).
 * - **ExceptionalPermission**
   - Trazabilidad completa: quien otorgo, cuando, por cuanto tiempo y
     con que justificacion. Expiracion automatica (CNST-031).
 * - **ETLEjecucion**
   - Registro de cada run del pipeline: timestamp de inicio y fin,
     estado (exitoso/fallido), volumen procesado, errores. Permite
     auditar la cadena de custodia de los datos del IVR.
 * - **Call / Campaign**
   - Datos de llamadas y campanas del IVR accedidos via ETL. Son
     datos de ciudadanos — acceso auditado via AuditEvent.

Vista Operational
-------------------

Los procedimientos operacionales implementan los controles de auditoria.

.. list-table::
 :header-rows: 1
 :widths: 30 70

 * - Operacion
   - Trazabilidad regulatoria
 * - **Toda accion de AGR_ADMIN**
   - Alta de usuario, asignacion de grupo, permiso temporal, cierre de
     sesion — todas generan AuditEvent (CNST-025).
 * - **Consulta y exportacion de audit log**
   - Solo AGR_AUDITOR puede exportar (``export_audit_log``). La exportacion
     misma es registrada. Permite cumplir requerimientos de auditorias
     externas sin exponer funciones de escritura.
 * - **Retry del pipeline ETL**
   - La solicitud de retry por AGR_OPERADOR genera AuditEvent. Cada
     nueva ejecucion queda registrada con su resultado.
 * - **Desactivacion de usuario**
   - Estado INACTIVE o BLOCKED. El registro permanece en BD con historial
     de todas las acciones del usuario (BR-009 v2.0.0).

Diagrama — cadena de auditoria
=================================

.. uml::
 :caption: Figura — Cadena de auditoria regulatoria en IACT

 @startuml

 skinparam sequence {
   ArrowColor #444444
   ParticipantBorderColor #333333
   ParticipantBackgroundColor White
   LifeLineBorderColor #888888
 }
 skinparam shadowing false

 participant "Usuario\n(cualquier rol)" as USUARIO
 participant "DRF\nAPI" as DRF_API
 participant "RBAC\nMiddleware" as RBAC_MIDDLEWARE
 participant "Business\nLogic" as BUSINESS_LOGIC
 participant "AuditEvent\n(append-only)" as AUDIT_EVENT

 USUARIO -> DRF_API : peticion con JWT
 DRF_API -> RBAC_MIDDLEWARE : verificar funcion atomica
 RBAC_MIDDLEWARE -> BUSINESS_LOGIC : autorizado
 BUSINESS_LOGIC -> AUDIT_EVENT : generar AuditEvent\n(usuario, accion, timestamp,\nentidad, estado anterior/nuevo)
 AUDIT_EVENT --> BUSINESS_LOGIC : AuditEvent persistido\n(CNST-025: inmutable)
 BUSINESS_LOGIC --> DRF_API : respuesta
 DRF_API --> USUARIO : resultado

 note over AUDIT_EVENT
   Append-only.
   No UPDATE, no DELETE.
   Auditable por AGR_AUDITOR.
 end note

 @enduml

Restricciones y principios
============================

.. list-table::
 :header-rows: 1
 :widths: 15 85

 * - Ref
   - Descripcion
 * - **BR-009 v2.0.0**
   - Soft-delete obligatorio. Usuarios y registros regulatorios se
     desactivan — nunca se eliminan. Historial siempre disponible.
 * - **CNST-025**
   - AuditEvent inmutable (append-only). Toda operacion de acceso
     o modificacion genera un AuditEvent. Sin excepciones.
 * - **CNST-029**
   - Datos de ciudadanos con restricciones de privacidad. Acceso
     auditado. Solo los roles con funcion especifica pueden consultar
     datos de llamadas individuales.
 * - **CNST-030**
   - Separacion de funciones evaluada en tiempo de asignacion. Los
     conflictos son bloqueados por el motor RBAC.
 * - **CNST-031**
   - Permisos temporales: rango obligatorio ``granted_at..expires_at``
     (maximo 6 meses), justificacion documentada, auditados.
 * - **CNST-032**
   - Exportaciones de reportes registradas. El acto de exportar es
     auditable.
 * - **CNST-033**
   - Cambios a las reglas SoD deben ser registrados con justificacion
     y aprobacion de AGR_ADMIN.

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/audit-event`
 :doc:`/arquitectura-tecnica/operational-view/system-administration`
 :doc:`/arquitectura-tecnica/operational-view/system-support`
 :doc:`/normativa/restricciones/index`
 :doc:`/base-cognitiva/_uml/uml-14-uml-vistas-arquitectonicas/perspectivas-arquitectonicas`
