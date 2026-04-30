.. meta::
 :artefacto: METODOLOGIA_DIAGRAMAS_DISTRIBUCION
 :tipo: Guia-Metodologica
 :dominio: requisitos
 :subdominio: _metodologia-aplicacion
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==========================================================
Diagramas de distribución — despliegue IACT (H13)
==========================================================

Propósito
=========

Modelar **dónde corre cada componente** de IACT: nodos
físicos (o virtuales), dispositivos, redes y protocolos.

Diferencia con H12:

- **Componentes (H12)** → qué piezas existen y qué contratos
  las unen.
- **Distribución (H13)** → en qué nodo se ejecuta cada
  pieza, con qué protocolo se comunica y qué frontera de
  red atraviesa.

Pregunta que responde:

   *Si me siento delante del servidor de IACT, ¿qué hay
   instalado en cada máquina y cómo se comunican?*

Marco metodológico
==================

- Skill principal: ``rm-specification``
- Skill complementario: ``rm-analysis``
- Stack canónico: ADR_DEVOPS_001 → Vagrant + Apache +
  ``mod_wsgi`` + Django + MySQL + Redis. **No** Docker, K8s,
  Nginx, Gunicorn, CDN, multi-region.
- Política de diagramación:
  :doc:`/base-cognitiva/plantuml-guide/guidelines`

Preludio — vista Container (C4 nivel 2)
=======================================

El Context (§ 13 de :doc:`diagramas-componentes`) cubre
la vista a 50 000 pies para audiencias no técnicas.
Pero la mayoría de los ingenieros necesita **más
detalle**: qué partes componen el sistema y cómo se
comunican entre sí. Ese nivel de detalle es la **vista
Container** del modelo C4.

Qué es un container en C4
-------------------------

En C4, **container no es contenedor Docker**: significa
una **unidad desplegable individual**. Ejemplos
canónicos:

- Una aplicación Java empaquetada.
- Una base de datos PostgreSQL.
- Un servidor web Apache + módulos.
- Una instancia Redis.
- Un broker de mensajes (Kafka, RabbitMQ).

Cada container es algo que se despliega como pieza
independiente, con su propio ciclo de vida operativo.

Qué muestra el Container — y qué no
-----------------------------------

- **Sí**: containers, sus tecnologías principales y
  los protocolos entre ellos.
- **Sí**: actores humanos (los mismos del Context) y
  sistemas externos.
- **No**: detalle del código dentro de cada container
  — eso es nivel 3 Component.
- **No**: clases, servicios internos, módulos.

La metáfora del zoom: si el Context era la vista al
sistema completo como una caja, el Container es lo
que se ve al **hacer click** sobre esa caja.

Equivalencia C4 ↔ documentos IACT
---------------------------------

En IACT la vista Container del modelo C4 vive en este
documento (``diagramas-distribucion.rst``):

- Los **nodos físicos** (``vm-iact``,
  ``ldap-corporativo``, ``bd-operativa``,
  ``ivr-host``) son el aspecto **deployment** del
  Container view.
- Los **artefactos dentro de cada nodo**
  (``iact.wsgi``, apps Django, Redis, MySQL,
  ``audit_log``) son los **containers** propiamente
  dichos en lenguaje C4.
- Los **protocolos** (HTTPS intranet, LDAPS, SQL
  read-only, SMB, etc.) corresponden a las flechas
  etiquetadas del Container view.

Containers IACT canónicos
-------------------------

.. list-table::
 :widths: 25 30 45
 :header-rows: 1

 * - Container
   - Tecnología
   - Rol
 * - ``Browser`` del supervisor
   - HTML + JS bundle
   - Cliente de la UI.
 * - ``iact-admin.bundle.js``
   - React (servido por Apache)
   - SPA del panel del supervisor.
 * - ``iact.wsgi``
   - Django + mod_wsgi sobre Apache
   - Backend de aplicación.
 * - ``Redis``
   - Redis local
   - Sesiones (CNST_002), throttling
     (CNST_011).
 * - ``bd_analytics``
   - MySQL local
   - Datos derivados de ETL.
 * - ``audit_log``
   - MySQL local (immutable)
   - Auditoría (CNST_025).
 * - ``etl_runner.py``
   - Python script (cron)
   - ETL nocturno (ventana
     CNST_006/008).
 * - ``ldap-corporativo``
   - LDAP externo
   - Directorio corporativo (read-only).
 * - ``bd-operativa``
   - MySQL externo
   - Origen de datos del call center
     (read-only, CNST_007).
 * - ``ivr-host``
   - IVR externo
   - Eventos de telefonía (read-only,
     CNST_006).

A diferencia del ejemplo del libro (que incluye un
broker de mensajes), IACT **no usa Kafka ni
RabbitMQ** por ADR_DEVOPS_001. La razón por la que
el libro nota que el broker no aparecía en el
Context aplica igual a IACT: es un detalle técnico
que pertenece al Container, no al Context.

Para qué sirve el Container view
--------------------------------

- **Ingenieros que entran al proyecto** — entender en
  10 minutos cómo se despliega IACT antes de tocar
  código.
- **Operaciones / SRE** — saber qué procesos viven en
  cada nodo y qué protocolos atraviesa cada
  llamada.
- **Diseño de cambios de infraestructura** — discutir
  el reemplazo de un container o la adición de uno
  nuevo.
- **Aprobaciones arquitectónicas** — material de
  soporte para presentaciones técnicas.

Las secciones siguientes (§§ 1-9 de este documento)
detallan cada container IACT con sus protocolos, su
configuración canónica y sus restricciones.

----

1. Nodo, dispositivo y conexión
===============================

En UML un **nodo** es un recurso de cómputo donde se
ejecutan componentes; un **dispositivo** es un recurso que
no ejecuta artefactos pero participa en el sistema (lector,
impresora, sensor). En IACT los nodos típicos son:

- ``vm-iact`` — VM Vagrant (en dev) o servidor corporativo
  (en prod) que aloja Apache + ``mod_wsgi`` + Redis + MySQL.
- ``ldap-corporativo`` — servidor LDAP de la organización.
- ``bd-operativa`` — origen read-only del call center
  (CNST_007).
- ``ivr-host`` — sistema IVR consultado por la ETL en modo
  read-only (CNST_006/008).
- ``puesto-supervisor`` — equipo del usuario final en la
  intranet, con navegador.

No hay CDN, balanceador, ni nodos en otras regiones. La
arquitectura de despliegue es deliberadamente simple.

2. Vista de despliegue global IACT
==================================

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   node "puesto-supervisor\n<<computadora>>" as PS {
     artifact "Navegador (intranet)" as BR
   }

   node "vm-iact\n<<servidor>>" as VM {
     node "Apache + mod_wsgi" as APACHE {
       artifact "iact.wsgi" as WSGI
       artifact "auth_app, perm_app,\nrpt_app, alr_app,\npip_app, aud_app, log_app" as APPS
     }
     node "Redis" as REDIS
     database "bd_analytics\n(MySQL)" as BDA
     database "audit_log\n(MySQL,\nimmutable CNST_025)" as AUDIT
     artifact "etl_runner.py\n(cron, ventana\nCNST_006/008)" as ETL
     artifact "iact-admin.bundle.js" as UIBUNDLE
   }

   node "ldap-corporativo\n<<servidor>>" as LDAP

   database "bd-operativa\n(read-only,\nCNST_007)" as BDO

   node "ivr-host\n<<servidor>>" as IVR

   BR -down-> APACHE : HTTPS (intranet)
   APACHE -down-> UIBUNDLE : sirve estaticos
   APPS -right-> REDIS : sesiones (CNST_002)\nthrottling (CNST_011)
   APPS -down-> BDA : lectura/escritura
   APPS -down-> AUDIT : append-only
   APPS -right-> LDAP : LDAPS (auth)
   ETL -left-> BDO : SQL read-only
   ETL -left-> IVR : protocolo IVR
   ETL -down-> BDA : insert agregados
   @enduml

3. Conexiones y protocolos
==========================

.. list-table::
 :widths: 25 25 50
 :header-rows: 1

 * - Origen
   - Destino
   - Protocolo / nota
 * - ``puesto-supervisor``
   - ``vm-iact`` / Apache
   - HTTPS sobre intranet corporativa.
 * - Apps Django
   - Redis
   - TCP local — sesiones (CNST_002), throttling
     (CNST_011).
 * - Apps Django
   - ``bd_analytics``
   - TCP local — escritura controlada por ``services.py``.
 * - Apps Django
   - ``audit_log``
   - TCP local — append-only (CNST_025).
 * - ``auth_app``
   - ``ldap-corporativo``
   - LDAPS — solo lectura de directorio.
 * - ``etl_runner``
   - ``bd-operativa``
   - SQL **read-only** (CNST_007).
 * - ``etl_runner``
   - ``ivr-host``
   - Protocolo proporcionado por IVR — read-only,
     ventana CNST_006/008.

No existe canal de salida hacia internet pública en runtime.
Cualquier nuevo destino externo requiere ADR explícito.

4. Diferencia entre dev (Vagrant) y prod
========================================

Ambos entornos comparten **la misma topología lógica**: el
diagrama de despliegue es el mismo. Las diferencias son de
implementación, no de arquitectura:

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Aspecto
   - Dev (Vagrant)
   - Prod (servidor corporativo)
 * - Host de ``vm-iact``
   - VM provisionada por Vagrant.
   - VM o bare-metal corporativo.
 * - Apache + mod_wsgi
   - Idéntico al de prod (por ADR_DEVOPS_001).
   - Idéntico.
 * - ``ldap-corporativo``
   - Mock o LDAP de pruebas.
   - LDAP real (read-only).
 * - ``bd-operativa``
   - Snapshot o réplica de prueba.
   - Réplica read-only en producción.
 * - ``ivr-host``
   - Stub de pruebas.
   - IVR real (read-only).

Este principio bloquea fragmentación: un cambio que solo
funciona en dev por usar Docker o Nginx contradice
ADR_DEVOPS_001.

5. Componentes dentro de los nodos
==================================

Vista de detalle de ``vm-iact`` mostrando los artefactos que
contiene y a qué interfaz corresponden (cruce con H12).

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   node "vm-iact" as VM {
     node "Apache + mod_wsgi" {
       artifact "iact.wsgi"
       artifact "auth_app — IAutenticacion"
       artifact "perm_app — ISecurity"
       artifact "rpt_app — IReporte"
       artifact "alr_app — IAlerta"
       artifact "pip_app — IETL"
       artifact "aud_app — IAuditLog"
       artifact "log_app — INotificacion"
     }
     node "Redis"
     database "bd_analytics"
     database "audit_log"
     artifact "etl_runner.py"
   }
   @enduml

6. UCs IACT y sus nodos
=======================

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - UC
   - Nodos involucrados
   - Notas
 * - UC_AUTH_01 Login
   - puesto-supervisor → vm-iact (auth_app) →
     ldap-corporativo
   - LDAPS, sesión en Redis (CNST_002).
 * - UC_PERM_07 Verificar permiso
   - vm-iact (perm_app + aud_app)
   - Local; sin salida externa.
 * - UC_RPT_04 Exportar reporte
   - vm-iact (rpt_app + log_app + aud_app + bd_analytics)
   - Async (CNST_019), buzón interno (CNST_001).
 * - UC_RPT_07 Reporte programado
   - vm-iact (scheduler + rpt_app + bd_analytics)
   - Disparado tras ventana ETL.
 * - UC_PIP_01 Carga ETL
   - vm-iact (etl_runner) ↔ bd-operativa, ivr-host →
     bd_analytics
   - Lectura read-only de operativa e IVR (CNST_007).
 * - UC_ALR_03 Reconocer alerta
   - vm-iact (alr_app + aud_app + log_app)
   - Sin salida externa.

7. Cuándo usar diagramas de distribución
========================================

.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Usar cuando…
   - No usar cuando…
 * - Documentamos el deployment para operaciones.
   - Solo cambia código dentro de un componente.
 * - Hay un cambio de host, protocolo o frontera de red.
   - El cambio es solo lógico (clases, OOP).
 * - Se evalúa un nuevo destino externo (otra BD, otro
     servicio).
   - El UC ya está cubierto con secuencias o componentes.
 * - Se prepara una revisión de seguridad de red.
   - El equipo solo necesita el flujo dinámico (usar
     secuencias o actividades).

8. Buenas prácticas
===================

1. Mantener un único diagrama global de despliegue por
   entorno; los detalles van en sub-diagramas (sección 5).
2. Etiquetar siempre el protocolo en cada conexión —
   "TCP/IP" sin más es poco informativo en una revisión de
   seguridad.
3. Marcar explícitamente las fronteras read-only
   (``bd-operativa``, ``ivr-host``).
4. Evitar nodos imaginarios: si no hay CDN, balanceador o
   multi-región, no aparecen en el diagrama.
5. Cualquier nodo nuevo en producción requiere ADR
   correspondiente (``adr-devops-*``).
6. Cuando cambien los protocolos o las fronteras, abrir un
   WP de revisión y actualizar este diagrama antes de
   ejecutar el cambio.

9. Capas finales del diseño UML aplicado a IACT
===============================================

.. list-table::
 :widths: 22 78
 :header-rows: 1

 * - Capa
   - Documentos en este cajón
 * - Conceptual
   - :doc:`orientacion-objetos`,
     :doc:`analisis-dominio`,
     :doc:`relaciones-uml`,
     :doc:`agregacion-interfaces`
 * - Casos de uso
   - :doc:`casos-uso-especificacion`,
     :doc:`casos-uso-diagramas`
 * - Comportamiento
   - :doc:`diagramas-estados`,
     :doc:`diagramas-secuencias`,
     :doc:`diagramas-colaboraciones`,
     :doc:`diagramas-actividades`
 * - Físico
   - :doc:`diagramas-componentes` (H12),
     :doc:`diagramas-distribucion` (H13)

Trazabilidad
============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill principal**
   - ``rm-specification``
 * - **Skill complementario**
   - ``rm-analysis``
 * - **Diagrama hermano (vista lógica física)**
   - :doc:`diagramas-componentes`
 * - **Stack canónico**
   - ADR_DEVOPS_001 (Vagrant + Apache + mod_wsgi + Django
     + MySQL + Redis)
 * - **Restricciones aplicadas**
   - CNST_001 buzón interno, CNST_002 sesión única,
     CNST_006/007/008 fronteras de la BD operativa e IVR,
     CNST_011 throttling, CNST_019/020 export async,
     CNST_025 audit immutable
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
 * - **Teoría UML**
   - :doc:`/base-cognitiva/_uml/index`
