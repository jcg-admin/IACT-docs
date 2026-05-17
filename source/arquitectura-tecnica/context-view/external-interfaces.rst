.. meta::
 :artefacto: AT_CONTEXT_VIEW_EXTERNAL_INTERFACES
 :tipo: Diagrama Arquitectonico — Context View
 :dominio: arquitectura_tecnica
 :subdominio: ContextView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-context-external-interfaces:

===================
Interfaces Externas
===================

Definicion de las interfaces entre el sistema IACT y sus entidades externas.
Cada interfaz especifica: entidad, protocolo, direccion de datos y restricciones.

Catalogo de interfaces externas
=================================

.. list-table::
 :header-rows: 1
 :widths: 20 15 12 53

 * - Interfaz
   - Protocolo
   - Direccion
   - Descripcion y restricciones
 * - **IVR-01** — BD Operativa IVR
   - SQL (MariaDB)
   - IVR → IACT
   - Fuente de datos de llamadas (tablas ``tbl_historico_*``).
     **Solo lectura** — P-01: IACT nunca escribe en la BD operativa.
     CNST-007: acceso de lectura exclusivo al esquema IVR.
     El ETL extrae datos en ventana de 6-12 horas (CNST-008)
     y los carga en el Almacen de Datos propio de IACT.
 * - **SCH-01** — APScheduler / Cron
   - Llamada de proceso interno
   - SCH → IACT
   - Disparador automatico del pipeline ETL. APScheduler es
     infraestructura interna del servicio ETL de IACT — no
     es un sistema externo en sentido estricto, pero actua
     como actor independiente en el modelo de contexto.
     El schedule expression se configura via ``system-configuration``
     (ver Operational View).
 * - **USR-01** — Usuarios IACT (browser/cliente HTTP)
   - HTTPS / JWT
   - IACT ↔ Usuario
   - Interfaz de usuario web autenticada con JWT (CNST-002,
     CNST-003). Todos los grupos RBAC acceden via esta interfaz.
     No existe registro publico: las cuentas son creadas
     exclusivamente por AGR_ADMIN.

Restriccion fundamental — P-01
================================

.. admonition:: Principio P-01 — IVR es fuente de datos de solo lectura

 El sistema IACT **nunca realiza operaciones de escritura** sobre la
 base de datos operativa del Sistema IVR (MariaDB / BD Operativa).
 Esta restriccion es absoluta y no admite excepciones.

 - **Fundamento**: integridad operacional del call center. Cualquier
   escritura accidental corromperia los registros de llamadas de los
   que dependen las operaciones institucionales.
 - **Implementacion**: la conexion a MariaDB esta configurada con
   credenciales de solo lectura (``GRANT SELECT``). No existe ORM
   write-path hacia tablas IVR.
 - **Trazabilidad**: G-01 (driver) → B-01 (principio de negocio) →
   T-01 (principio tecnico) → D-01 (decision arquitectonica).
 - **Referencias**: CNST-007, ADR-GOB-* de integracion IVR.

Flujo de datos entre interfaces
=================================

.. uml::
 :caption: Figura — Interfaces externas del sistema IACT

 @startuml

 skinparam rectangle {
   BackgroundColor White
   BorderColor #333333
   RoundCorner 8
 }
 skinparam database {
   BackgroundColor #EEF4FF
   BorderColor #336699
 }
 skinparam arrowColor #444444
 skinparam shadowing false

 database "BD Operativa IVR\n(MariaDB)\ntbl_historico_*" as BDOperativa
 rectangle "APScheduler\n/ Cron" as Scheduler
 rectangle "Usuarios IACT\n(browser)" as Usuarios

 rectangle "Sistema IACT" as SISTEMA_IACT {
   rectangle "ETL Service" as SERVICIO_ETL
   rectangle "IACT App\n(Django REST Framework)" as App
   database "Almacen de Datos\n(PostgreSQL IACT)" as BDPropia
 }

 BDOperativa -right-> SERVICIO_ETL : <<IVR-01>>\nSELECT solo lectura\n(CNST-007, P-01)
 Scheduler -down-> SERVICIO_ETL  : <<SCH-01>>\ndisparo SERVICIO_ETL\n(CNST-008: 6-12h)
 SERVICIO_ETL -right-> BDPropia  : INSERT / UPDATE\n(datos propios SISTEMA_IACT)
 BDPropia -right-> App  : consultas SISTEMA_IACT
 Usuarios <-right-> App : <<USR-01>>\nHTTPS + JWT\n(CNST-002, CNST-003)

 note bottom of BDOperativa
   P-01: SISTEMA_IACT no escribe aqui.
   Credenciales: GRANT SELECT.
 end note

 @enduml

.. seealso::

 :doc:`context-diagram`
 :doc:`stakeholders`
 :doc:`/arquitectura-tecnica/deploy-view/index`
