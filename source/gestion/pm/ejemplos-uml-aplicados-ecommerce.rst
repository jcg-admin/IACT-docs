.. meta::
 :artefacto: EJEMPLOS_UML_APLICADOS
 :tipo: Guia
 :dominio: gestion
 :subdominio: pm
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==================================================================
Ejemplos UML aplicados al dominio ecommerce IACT (PlantUML)
==================================================================

.. note::

 Compañero del :doc:`/gestion/pm/plan-documentacion-uc-con-uml`.
 Muestra cómo lucen los **9 diagramas UML** cuando se aplican al
 dominio específico del proyecto IACT (97 UCs, stack
 React + Django + MySQL, integraciones Stripe/SendGrid/Logística).

 Sirve como **referencia de precedente** para los autores que
 generen los 13 documentos del plan: cada diagrama del plan debe
 lucir similar a estos ejemplos en estilo y nivel de detalle.

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 Para la teoría genérica de cada diagrama ver
 :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama` (cheat-
 sheet) y la serie pedagógica :doc:`/base-cognitiva/_uml/index`
 (UML_01..UML_13).

----

1. Diagrama de clases — entidad ``Producto`` (UC_CAT)
=====================================================

**Caso aplicado:** la clase canónica ``Producto`` del catálogo,
referenciada por UC_CAT_01..13.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   class Producto {
     - id : Integer
     - sku : String
     - nombre : String
     - descripcion : String
     - precio : Decimal
     - stock : Integer
     - categoria : Category
     + getDetalles() : String
     + updateStock(cantidad : Integer) : void
     + aplicarDescuento(porcentaje : Decimal) : Decimal
     + crearVariante(atributos : String) : Producto
   }
   @enduml

**Aplicación en el plan:**

- UC_CAT_06 (Ver detalles) consume ``getDetalles()``.
- UC_INV_01 (Actualizar stock) llama a ``updateStock()``.
- DOC-24 (Clases consolidadas) integra ésta con todas las demás.

**Perspectiva:** ESTÁTICA. **Audiencia:** Devs / Arquitectos.

----

2. Diagrama de objetos — instancia ``laptop_dell``
==================================================

**Caso aplicado:** instancia concreta de ``Producto`` para
casos de prueba.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   object "laptop_dell : Producto" as L {
     id = 1001
     sku = "SKU-DELL-XPS-2024"
     nombre = "Dell XPS 13"
     descripcion = "Laptop ultraportátil 13'' Intel i7"
     precio = 1299.99
     stock = 45
     categoria = "Electrónica > Laptops"
   }
   @enduml

**Aplicación en el plan:** los casos de prueba (sección 8 de la
plantilla) deben usar instancias concretas como ésta.

----

3. Diagrama de casos de uso — UC_CAT (catálogo, 13 UCs)
=======================================================

**Caso aplicado:** los 13 UCs de ``UC_CAT`` con sus actores
(Cliente, Administrador) y relaciones ``<<include>>``.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   left to right direction
   actor Cliente
   actor Administrador as Admin

   rectangle "UC_CAT — Catálogo (13 UCs)" {
     usecase "UC_CAT_01\nVer Catálogo"      as U01
     usecase "UC_CAT_02\nBuscar"            as U02
     usecase "UC_CAT_03/04\nFiltrar"        as U0304
     usecase "UC_CAT_05\nOrdenar"           as U05
     usecase "UC_CAT_06\nVer Detalles"      as U06
     usecase "UC_CAT_07\nGalería"           as U07
     usecase "UC_CAT_08\nCrear Producto"    as U08
     usecase "UC_CAT_09\nEditar"            as U09
     usecase "UC_CAT_10\nEliminar"          as U10
     usecase "UC_CAT_11\nCrear Categoría"   as U11
     usecase "UC_CAT_12\nEditar Categoría"  as U12
     usecase "UC_CAT_13\nReordenar"         as U13
   }

   Cliente --> U01
   Cliente --> U02
   Cliente --> U0304
   Cliente --> U05
   Cliente --> U06
   Cliente --> U07

   Admin   --> U08
   Admin   --> U09
   Admin   --> U10
   Admin   --> U11
   Admin   --> U12
   Admin   --> U13

   U01 ..> U0304 : <<include>>
   U02 ..> U05   : <<include>>
   @enduml

**Aplicación en el plan:** DOC-15 (UC_CAT) usa este diagrama
como vista global de su dominio.

**Perspectiva:** DINÁMICA (POV usuario). **Audiencia:**
Clientes / Product Owners / Analistas.

----

4. Diagrama de estados — ciclo de vida de ``Orden`` (UC_ORD)
============================================================

**Caso aplicado:** los estados por los que pasa una ``Orden``,
desde Draft hasta Completada, con notas que referencian los UCs.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   [*] --> Draft

   Draft --> CarritoPendiente : agregarItems()
   CarritoPendiente --> CarritoPendiente : modificarCantidad()
   CarritoPendiente --> Checkout : iniciarCheckout()

   Checkout --> PagoPendiente : ingresarDireccion()
   PagoPendiente --> PagoRechazado : stripe.decline()
   PagoRechazado --> PagoPendiente : reintentar()
   PagoRechazado --> CarritoPendiente : volver()

   PagoPendiente --> PagoAprobado : stripe.approve()
   PagoAprobado --> OrdenConfirmada : confirmarOrden()

   OrdenConfirmada --> PreparandoEnvio : validarInventario()
   PreparandoEnvio --> ListaEnvio : empacar()
   ListaEnvio --> Enviada : generarEtiqueta()

   Enviada --> EnTransito : logistics.update()
   EnTransito --> Entregada : cliente.recibe()

   Entregada --> Completada : timeout 30 días
   Completada --> [*]

   note right of CarritoPendiente
     Cliente puede modificar
     antes de checkout.
     UCs: UC_CAR_01, UC_CAR_02
   end note

   note right of PagoPendiente
     Esperando Stripe.
     Timeout: 15 min.
     UC: UC_PAG_01
   end note

   note right of Enviada
     Tracking activo.
     Notificaciones: UC_NOT
   end note

   note right of Entregada
     Ventana de devolución: 30 días
     UC: UC_ORD_06
   end note
   @enduml

**Aplicación en el plan:** DOC-17 (UC_ORD).

----

5. Diagrama de secuencias — UC_ORD_01 (crear orden)
===================================================

**Caso aplicado:** flujo completo de checkout con bifurcación
pago aprobado / rechazado, integrando Logística y Stripe.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Cliente
   participant ":Frontend\n(React)"  as F
   participant ":Backend\n(Django)"  as B
   participant ":Logística"          as L
   participant ":Stripe"             as S
   participant ":MySQL"              as DB

   Cliente -> F  : 1. Click Confirmar Compra
   F -> B        : 2. POST /api/orders/

   B -> DB       : 3. SELECT carrito
   DB --> B      : 4. carrito válido

   B -> L        : 5. POST /quote
   L --> B       : 6. opciones envío

   B -> S        : 7. POST /charges

   alt Pago aprobado
     S --> B     : 8a. {charge_id, status: succeeded}
     B -> DB     : 9.  BEGIN TRANSACTION
     B -> DB     : 10. INSERT Order, OrderItems, Payment
     B -> DB     : 11. UPDATE Product.stock
     B -> DB     : 12. INSERT AuditLog
     B -> DB     : 13. COMMIT
     B --> F     : 14. {order_id, total, status}
     F --> Cliente : 15. ✓ Orden #12345 confirmada
   else Pago rechazado
     S --> B     : 8b. {error: card_declined}
     B -> DB     : 9.  INSERT AuditLog
     B --> F     : 14. {error}
     F --> Cliente : 15. ✗ Pago rechazado
   end
   @enduml

**Aplicación en el plan:** DOC-25 (Secuencias críticas).

----

6. Diagrama de actividades — flujo completo de checkout
=======================================================

**Caso aplicado:** UC_ORD_01 con todas las decisiones
(carrito válido, dirección, pago aprobado, reintento).

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   start
   :Inicio: crear orden\n(UC_ORD_01);
   :Validar carrito\n(UC_CAR_02);

   if ([carrito válido]) then (sí)
   else (no)
     :Mostrar error;
     stop
   endif

   repeat
     :Validar dirección\n(UC_ORD_02);
   repeat while ([dirección inválida]) is (sí — sugerir correcciones)
   ->no;

   :Consultar logística\n(UC_LOG_01);
   :Mostrar opciones de envío;
   :Cliente elige método;

   repeat
     :Procesar pago\n(UC_PAG_01);
     if ([pago aprobado]) then (sí)
       break
     else (no)
       :Mostrar razón de rechazo;
       if ([reintentar]) then (sí)
       else (no)
         stop
       endif
     endif
   repeat while ([volver a intentar]) is (sí)
   ->no;

   :✓ Pago aprobado;
   :Crear orden en BD;
   :Auditar cambio (UC_ACC_11);
   :Enviar email (UC_NOT_01);
   :Generar etiqueta (UC_LOG_02);
   :Mostrar confirmación;
   :Fin: orden creada;
   stop
   @enduml

**Aplicación en el plan:** DOC-17 (UC_ORD) y otros UCs
complejos.

----

7. Diagrama de colaboraciones — UC_ORD_01 entre dominios
========================================================

**Caso aplicado:** cómo colaboran 7 actores/objetos para crear
una orden.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   actor Cliente
   object ":Carrito\n(UC_CAR)"      as Car
   object ":Orden\n(UC_ORD_01)"     as Ord
   object ":Pago\n(UC_PAG_01)"      as Pag
   object ":Logística\n(UC_LOG_01)" as Log
   object ":Stripe API"             as Stripe
   object ":Notificación\n(UC_NOT_01)" as Notif

   Cliente -> Car  : "1: selecciona items"
   Cliente -> Ord  : "2: inicia"
   Car     -> Ord  : "3: pasa items"
   Ord     -> Pag  : "4: crea pago"
   Pag     -> Stripe : "5: contacta"
   Stripe  -> Pag  : "6: autoriza"
   Pag     -> Ord  : "7: confirma pago"
   Ord     -> Log  : "8: solicita envío"
   Log     -> Ord  : "9: opciones disponibles"
   Ord     -> Notif : "10: dispara notificación"
   @enduml

**Aplicación en el plan:** DOC-25.

----

8. Diagrama de componentes — arquitectura del sistema
=====================================================

**Caso aplicado:** arquitectura de software del proyecto IACT —
React + Django + MySQL + servicios externos.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   package "Frontend (React 18 + Redux)" {
     component "UI Components\nPages, Forms"        as UI
     component "Redux Store\nState Management"      as Redux
     component "HTTP Client\nAxios + Interceptors"  as HTTP
   }

   package "Backend (Django 4 + DRF)" {
     component "REST API\nViewSets"                 as REST
     component "Auth Service\nJWT, Permisos"        as Auth
     component "Order Service\nCrear, Actualizar"   as OrdSvc
     component "Payment Service\nStripe"            as PaySvc
     component "Notification Service\nEmail, SMS"   as NotifSvc
   }

   database "MySQL 8\nUsers, Products,\nOrders, Audit" as DB

   package "External APIs" {
     component "Stripe API\n(Pagos)"        as StripeAPI
     component "SendGrid\n(Email)"          as SendGrid
     component "Logística API\n(Envíos)"    as LogAPI
   }

   UI    --> Redux : state
   UI    --> HTTP  : fetch / post
   HTTP  --> REST  : REST

   REST  --> Auth     : usa
   REST  --> OrdSvc   : usa
   REST  --> PaySvc   : usa
   REST  --> NotifSvc : usa

   Auth    --> DB : queries
   OrdSvc  --> DB : queries
   PaySvc  --> DB : queries

   PaySvc   --> StripeAPI : HTTPS
   NotifSvc --> SendGrid  : HTTPS
   OrdSvc   --> LogAPI    : HTTPS
   @enduml

**Aplicación en el plan:** DOC-26 (Componentes + Distribución).

----

9. Diagrama de distribución — despliegue en producción
======================================================

**Caso aplicado:** topología de producción del proyecto
(Apache + mod_wsgi + MySQL master/replica + Redis,
**sin** Docker / Kubernetes / Nginx / Gunicorn per restricciones
del proyecto).

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml

   node "Cliente Web" <<dispositivo>> as Browser {
     component "Chrome / Firefox"
   }

   node "Load Balancer" <<procesador>> as LB {
     component "HTTPS / SSL\nPort 443"
   }

   node "Web Server 1" <<procesador>> as W1 {
     component "Apache 2.4"
     component "mod_wsgi"
     component "Django 4"
   }

   node "Web Server 2" <<procesador>> as W2 {
     component "Apache 2.4"
     component "mod_wsgi"
     component "Django 4"
   }

   node "Redis" <<procesador>> as Cache {
     component "Sessions"
     component "Data Cache"
   }

   node "MySQL Master" <<procesador>> as M {
     database "Write ops\nPort 3306"
   }
   node "MySQL Replica" <<procesador>> as R {
     database "Read ops\nPort 3306"
   }

   cloud "Stripe"           as Stripe
   cloud "SendGrid"         as SendGrid
   cloud "Logística API"    as LogCloud

   Browser -- LB    : HTTPS / SSL
   LB      -- W1    : TCP 8000\n(round robin)
   LB      -- W2    : TCP 8000\n(round robin)

   W1 -- Cache : TCP 6379
   W2 -- Cache : TCP 6379

   W1 -- M : TCP 3306 (write)
   W2 -- R : TCP 3306 (read)
   M  -- R : replicación

   W1 -- Stripe    : HTTPS
   W1 -- SendGrid  : HTTPS
   W1 -- LogCloud  : HTTPS
   @enduml

**Aplicación en el plan:** DOC-26 (Componentes + Distribución).

----

10. Tabla resumen — qué diagrama va en qué documento
====================================================

.. list-table::
 :widths: 22 16 32 30
 :header-rows: 1

 * - Diagrama
   - Tipo
   - Propósito
   - DOC del plan
 * - Clases
   - Estático
   - Estructura
   - DOC-24
 * - Objetos
   - Estático
   - Instancias
   - Casos de prueba (cada UC)
 * - Casos de uso
   - Dinámico
   - Requisitos
   - DOC-14..DOC-23
 * - Estados
   - Dinámico
   - Ciclo de vida
   - DOC-17 (Órdenes)
 * - Secuencias
   - Dinámico
   - Interacciones
   - DOC-25 (críticas)
 * - Actividades
   - Dinámico
   - Flujos
   - UCs complejos
 * - Colaboraciones
   - Dinámico
   - Arquitectura
   - DOC-25
 * - Componentes
   - Estático
   - Módulos
   - DOC-26
 * - Distribución
   - Estático
   - Infraestructura
   - DOC-26

----

11. Trazabilidad
================

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``pm-planning`` (PMBOK — Planning, supporting examples)
 * - **Origen del documento**
   - Adaptado de "GUÍA-UML-DIAGRAMAS-FUNDAMENTALES — Aplicados al
     dominio E-commerce" (cheat-sheet aplicado interno),
     reescrito en PlantUML.
 * - **Cheat-sheet genérica complementaria**
   - :doc:`/base-cognitiva/_uml/cuando-usar-cada-diagrama`
 * - **Lecciones completas (Schmuller)**
   - :doc:`/base-cognitiva/_uml/index`
 * - **Plan de documentación que aplica estos ejemplos**
   - :doc:`plan-documentacion-uc-con-uml`
 * - **Plantilla canónica de UC**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Metodologías relacionadas**
   - :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs`
   - :doc:`/normativa/estandares/metodologia-oop-para-ucs`
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
