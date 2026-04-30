.. meta::
 :artefacto: METODOLOGIA_DIAGRAMAS_ACTIVIDADES
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
Diagramas de actividades — flujos y procesos en IACT (H11)
==========================================================

Propósito
=========

Modelar **los pasos** que recorre una operación de IACT:
secuencia, decisiones, paralelismo y responsabilidades.

Diferencia clave con otros diagramas:

- **Estados** → en qué estados está un objeto.
- **Actividades** → qué pasos realiza para llegar a esos estados.
- **Secuencias** → quién envía qué mensaje y cuándo.
- **Colaboraciones** → quién está conectado con quién en el espacio.

Pregunta que responde un diagrama de actividades:

   *¿Cuáles son los pasos, decisiones y flujos dentro de
   esta operación?*

Marco metodológico
==================

- Skill principal: ``rm-specification``
- Skill complementario: ``rm-analysis`` (modelado de flujo)
- Política de diagramación:
  :doc:`/base-cognitiva/plantuml-guide/guidelines`
- Estilos centralizados:
  ``source/_static/plantuml-styles.puml``

1. Componentes básicos
======================

Un diagrama de actividades de UML usa:

- **Nodo inicial** — círculo relleno.
- **Actividad** — rectángulo redondeado.
- **Decisión / merge** — rombo.
- **Fork / join** — barra horizontal.
- **Nodo final** — diana.

Forma canónica en PlantUML
--------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   start
   :Actividad 1;
   :Actividad 2;
   if (condicion?) then (si)
     :Actividad 3;
   else (no)
     :Actividad 4;
   endif
   stop
   @enduml

2. Decisiones (bifurcaciones)
=============================

Las **condiciones son mutuamente exclusivas**: solo una rama
se ejecuta. Etiquetar siempre la guarda entre corchetes o
con el texto de la decisión.

Ejemplo IACT — UC_AUTH_01 (Login)
---------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   start
   :Recibir credenciales;
   :Validar usuario en LDAP;
   if (credenciales validas?) then ([si])
     if (sesion previa activa?) then ([no])
       :Crear sesion (CNST_002);
       :Registrar acceso en AuditLog (CNST_025);
       stop
     else ([si])
       :Cerrar sesion previa;
       :Crear sesion nueva;
       stop
     endif
   else ([no])
     :Incrementar contador throttling (CNST_011);
     :Registrar intento fallido;
     stop
   endif
   @enduml

3. Rutas concurrentes (fork / join)
===================================

Cuando varias actividades pueden ejecutarse **al mismo
tiempo**, se usa fork/join. La reunificación espera a que
**todas** las ramas paralelas terminen.

Ejemplo IACT — UC_RPT_07 (Reporte programado)
---------------------------------------------

Al cierre de la ventana ETL (CNST_006/007/008), tres tareas
arrancan en paralelo: cálculo de métricas, persistencia y
notificación al solicitante.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   start
   :Detectar fin de ventana ETL;
   :Cargar configuracion del reporte;
   fork
     :Calcular metricas BR_016/017/018;
     :Persistir resultados en BDAnalytics;
   fork again
     :Generar archivo de exportacion (async, CNST_019);
     :Subir a almacen temporal;
   fork again
     :Componer notificacion;
     :Publicar en buzon interno (CNST_001);
   end fork
   :Marcar reporte como entregado;
   :Registrar evento en AuditLog;
   stop
   @enduml

4. Señales (eventos)
====================

Una actividad puede **enviar** una señal y otra **recibirla**
asincrónicamente. En PlantUML se modela con ``->`` entre
swimlanes o con notas explícitas.

Ejemplo IACT — Alerta crítica (UC_ALR_03)
-----------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   start
   :EvaluadorAlertas detecta umbral excedido;
   :Emitir senal "AlertaCritica";
   note right
     senal asincronica
     hacia el supervisor
   end note
   :Registrar emision en AuditLog;
   stop
   @enduml

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   start
   :Esperar senal "AlertaCritica";
   :Recibir senal;
   :Mostrar alerta en panel del supervisor;
   :Habilitar accion "reconocer";
   stop
   @enduml

5. Marcos de responsabilidad (swimlanes)
========================================

Los swimlanes muestran **quién** ejecuta cada actividad. En
IACT los carriles típicos son: Supervisor, Backend Django,
BD Operativa (read-only, CNST_007), BDAnalytics, Componente
ETL, Scheduler.

Ejemplo IACT — UC_RPT_04 (Exportar reporte)
-------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   |Supervisor|
   start
   :Seleccionar reporte y rango (max 6 meses, CNST_031);
   :Solicitar exportacion;
   |Backend|
   :Validar permiso (CNST_030 SoD);
   if (permiso ok?) then ([si])
     :Verificar throttling export (CNST_020);
     if (cuota disponible?) then ([si])
       :Encolar tarea async (CNST_019);
       |Worker Export|
       :Leer agregados de BDAnalytics;
       :Generar archivo CSV/XLSX;
       :Subir a almacen temporal;
       |Backend|
       :Notificar via buzon interno (CNST_001);
       |Supervisor|
       :Recibir notificacion;
       :Descargar archivo;
       stop
     else ([no])
       |Backend|
       :Responder "cuota agotada";
       stop
     endif
   else ([no])
     :Registrar intento denegado en AuditLog;
     stop
   endif
   @enduml

6. Ciclos
=========

Los ciclos se modelan con ``while``/``repeat``. En IACT
aparecen típicamente en lectura paginada de la BD operativa
y en reintentos controlados de ETL.

Ejemplo IACT — Carga ETL paginada (CNST_006/008)
------------------------------------------------

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   start
   :Inicializar offset = 0;
   :Definir tamano_lote;
   while (existen mas filas?) is ([si])
     :Leer lote desde BD operativa (readonly);
     :Transformar registros;
     :Insertar en BDAnalytics;
     :Avanzar offset;
     if (ventana ETL agotada?) then ([si])
       :Marcar carga como incompleta;
       break
     else ([no])
     endif
   endwhile ([no])
   :Cerrar carga;
   :Registrar resumen en AuditLog;
   stop
   @enduml

7. Diagramas híbridos
=====================

PlantUML permite combinar elementos de actividades con notas
de objeto, anclas a casos de uso o referencias a estados.
Usarlo con moderación: un solo diagrama no debe sustituir a
los demás, sino complementarlos donde el flujo lo requiera.

Recomendación IACT:

- Si el énfasis es **flujo del proceso** → actividades.
- Si el énfasis es **interacción** → secuencias o
  colaboraciones (:doc:`diagramas-secuencias`,
  :doc:`diagramas-colaboraciones`).
- Si el énfasis es **ciclo de vida del objeto** → estados
  (:doc:`diagramas-estados`).

8. Cuándo usar diagramas de actividades
=======================================

.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Usar cuando…
   - No usar cuando…
 * - El UC tiene flujo con **decisiones múltiples**.
   - Solo hay un par de pasos secuenciales.
 * - Hay **paralelismo** o concurrencia entre subsistemas.
   - El foco es estructura estática (usar clases).
 * - Conviene mostrar **responsabilidades** entre actores.
   - El foco es interacción mensaje a mensaje (usar
     secuencias).
 * - Documentamos **proceso de negocio** para no técnicos.
   - El UC ya quedó claro con la especificación textual.

9. UCs de IACT con diagrama de actividades obligatorio
======================================================

.. list-table::
 :widths: 28 32 40
 :header-rows: 1

 * - UC
   - Por qué
   - Elementos típicos
 * - ``UC_AUTH_01`` Login
   - Decisiones (credenciales, sesión previa) + throttling.
   - Decisión, ciclo de reintento, swimlane Backend/LDAP.
 * - ``UC_RPT_04`` Exportar reporte
   - Async + throttling + notificación.
   - Fork (export + notify), swimlanes Supervisor/Backend/Worker.
 * - ``UC_RPT_07`` Reporte programado
   - Concurrencia post-ETL.
   - Fork de tres ramas, join al final.
 * - ``UC_PIP_01`` Carga ETL
   - Ciclo paginado + ventana temporal CNST_006/008.
   - Loop, decisión por tiempo, swimlane ETL/BD.
 * - ``UC_ALR_03`` Reconocer alerta crítica
   - Señales + sincronización con auditoría/notificación.
   - Send/receive signal, fork/join.
 * - ``UC_PERM_07`` Verificar permiso
   - Decisión SoD (CNST_030).
   - Decisiones encadenadas, swimlane SecRules/AuditLog.

10. Buenas prácticas
====================

1. **Identificar inicio y fin** explícitos antes de dibujar.
2. **Listar pasos** en orden secuencial primero; introducir
   paralelismo solo donde realmente exista.
3. **Etiquetar guardas** ``[condicion]`` en cada salida del
   rombo. Sin guarda, el diagrama miente.
4. **Mantener un nivel de abstracción**: no mezclar
   actividades de negocio con llamadas HTTP en el mismo
   diagrama.
5. **Cerrar todos los joins** que abrieron forks.
6. **Validar caminos** recorriendo manualmente cada rama
   hasta un nodo final.
7. **Vincular** cada actividad relevante a su BR/CNST/UC en
   el texto adyacente, no dentro del diagrama.

Trazabilidad
============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill principal**
   - ``rm-specification``
 * - **Skill complementario**
   - ``rm-analysis``
 * - **Diagramas hermanos**
   - :doc:`diagramas-secuencias`,
     :doc:`diagramas-colaboraciones`,
     :doc:`diagramas-estados`
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
 * - **Plantilla de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Teoría UML**
   - :doc:`/base-cognitiva/_uml/index`
