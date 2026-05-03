.. meta::
 :artefacto: INDEX_AT_UC
 :tipo: Indice
 :dominio: arquitectura_tecnica
 :subdominio: uc
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at-uc-index:

=============================================
Vista de Casos de Uso — Arquitectura Técnica
=============================================

Diagramas arquitectónicos por UC siguiendo el modelo **4+1 de Kruchten**
(variante 5+1 con Domain Model). Cada archivo documenta un UC desde
las 6 perspectivas arquitectónicas.

Modelo 4+1 (variante 5+1)
--------------------------

.. list-table::
 :widths: 20 20 60
 :header-rows: 1

 * - Vista
   - Tipo
   - Descripción
 * - **Domain Model**
   - Vista Lógica
   - Entidades del dominio y relaciones para el UC.
     Diagrama de clases (conceptual) + estados.
 * - **Design View**
   - Vista de Diseño
   - Clases con detalle de diseño, secuencias, colaboración.
     Cómo el sistema resuelve el UC técnicamente.
 * - **Implementation View**
   - Vista de Implementación
   - Componentes y paquetes. Organización del código.
 * - **Use Case View**
   - Vista de Casos de Uso
   - Diagrama UC con actores RBAC, includes y extends.
     Une todas las demás vistas.
 * - **Process View**
   - Vista de Procesos
   - Actividades y secuencias. Concurrencia, sincronización.
 * - **Deployment View**
   - Vista de Despliegue
   - Distribución física. Nodos, artefactos, comunicación.

----

MOD_Auth — Autenticación (5 UCs)
----------------------------------

.. toctree::
 :maxdepth: 1

 uc-auth-01
 uc-auth-02
 uc-auth-03
 uc-auth-04
 uc-auth-05

MOD_Users — Gestión Usuarios (4 UCs)
--------------------------------------

.. toctree::
 :maxdepth: 1

 uc-usr-01
 uc-usr-02
 uc-usr-03
 uc-usr-04

MOD_Access — Control Acceso (7 UCs)
-------------------------------------

.. toctree::
 :maxdepth: 1

 uc-acc-01
 uc-acc-02
 uc-acc-03
 uc-acc-04
 uc-acc-05
 uc-acc-08
 uc-acc-09

MOD_Permissions — Gestión RBAC (10 UCs)
-----------------------------------------

.. toctree::
 :maxdepth: 1

 uc-perm-01
 uc-perm-02
 uc-perm-03
 uc-perm-04
 uc-perm-05
 uc-perm-06
 uc-perm-07
 uc-perm-08
 uc-perm-09
 uc-perm-10

MOD_Reports — Reportería (16 UCs)
-----------------------------------

.. toctree::
 :maxdepth: 1

 uc-inc-rpt-01
 uc-rpt-01
 uc-rpt-02
 uc-rpt-03
 uc-rpt-04
 uc-rpt-07
 uc-rpt-08
 uc-rpt-09
 uc-rpt-10
 uc-rpt-11
 uc-rpt-12
 uc-rpt-13
 uc-rpt-14
 uc-rpt-15
 uc-rpt-16
 uc-rpt-17

MOD_Alerts — Alertas (5 UCs)
------------------------------

.. toctree::
 :maxdepth: 1

 uc-alr-01
 uc-alr-02
 uc-alr-03
 uc-alr-04
 uc-alr-05

MOD_Pipeline — Supervisión ETL (4 UCs)
----------------------------------------

.. toctree::
 :maxdepth: 1

 uc-pip-01
 uc-pip-02
 uc-pip-03
 uc-pip-04

MOD_Audit — Auditoría (4 UCs)
-------------------------------

.. toctree::
 :maxdepth: 1

 uc-aud-01
 uc-aud-02
 uc-aud-03
 uc-aud-04

MOD_Logs — Bitácoras (7 UCs)
------------------------------

.. toctree::
 :maxdepth: 1

 uc-log-01
 uc-log-02
 uc-log-03
 uc-log-04
 uc-log-05
 uc-log-06
 uc-log-07

MOD_Operator — Operación Agente (10 UCs)
------------------------------------------

.. toctree::
 :maxdepth: 1

 uc-opr-01
 uc-opr-02
 uc-opr-03
 uc-opr-04
 uc-opr-05
 uc-opr-06
 uc-opr-07
 uc-opr-08
 uc-opr-09
 uc-opr-10

MOD_Supervision — Supervisión Tiempo Real (3 UCs)
---------------------------------------------------

.. toctree::
 :maxdepth: 1

 uc-sup-01
 uc-sup-02
 uc-sup-03

MOD_Caller — Llamante Externo (5 UCs)
---------------------------------------

.. toctree::
 :maxdepth: 1

 uc-cli-01
 uc-cli-02
 uc-cli-03
 uc-cli-04
 uc-cli-05
