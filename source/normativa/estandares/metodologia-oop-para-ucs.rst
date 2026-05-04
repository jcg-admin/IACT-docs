.. meta::
 :artefacto: METODOLOGIA_OOP_UC
 :tipo: Estándar
 :dominio: normativa
 :subdominio: estandares
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

================================================================
Metodología OOP para Casos de Uso (UCs)
================================================================

.. note::

 Estándar metodológico que prescribe **cómo razonar un caso de
 uso aplicando lentes OOP** (abstracción, herencia,
 polimorfismo, encapsulamiento, envío de mensajes, asociaciones).

 Aplica al documentar los **97 UCs** del proyecto IACT per
 :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`, y se utiliza
 con la plantilla canónica
 :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`.

 **Es paso downstream** de
 :doc:`/normativa/estandares/metodologia-analisis-dominio-ucs` —
 primero se descubren las clases (sustantivos→clases,
 verbos→operaciones), luego se aplican las seis dimensiones
 OOP que define este estándar.

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 **Ejemplos canónicos aplicados al dominio IACT:** ver
 :doc:`/requisitos/_metodologia-aplicacion/orientacion-objetos` para los
 6 principios aplicados al dominio real (jerarquía de usuarios
 IACT — Operador, Supervisor, Admin, Auditor; polimorfismo
 sobre métricas BR_016/017/018; encapsulamiento de Reporte con
 segmentación CNST_008; etc.).

----

1. Propósito
============

Cada UC documentado en el proyecto debe analizarse con seis
**dimensiones OOP**. Esto produce documentación de **mayor
calidad arquitectónica**: separa lo que el usuario percibe (UC
abstracto) de cómo se implementa (clases, mensajes,
componentes), y obliga a explicitar reutilización y
encapsulamiento.

Las seis dimensiones obligatorias son:

1. **Abstracción** — qué se oculta y qué se expone.
2. **Herencia** — qué reutiliza el UC de otro.
3. **Polimorfismo** — variaciones de comportamiento bajo el
   mismo nombre.
4. **Encapsulamiento** — interfaz pública vs lógica privada.
5. **Envío de mensajes** — secuencia de comunicación entre
   componentes.
6. **Asociaciones** — relaciones formales con otros UCs
   (``<<include>>``, ``<<extend>>``, generalización).

  Para los fundamentos UML/OOP en sí, consulte la serie
  pedagógica :doc:`/base-cognitiva/_uml/index` (en particular
  :doc:`/base-cognitiva/_uml/uml-02-orientacion-objetos/index`).

----

2. Las seis dimensiones OOP aplicadas a UCs
===========================================

2.1 Abstracción en el UC
------------------------

La abstracción consiste en **eliminar detalles innecesarios** y
mantener sólo lo esencial.

**Antipatrón** (demasiados detalles):

::

 UC: Ver Catálogo
 Detalles:
 - Conectarse a servidor
 - Resolver DNS
 - Establecer conexión TLS
 - Autenticarse con token JWT
 - Enviar headers HTTP
 - Parsear respuesta JSON
 - Serializar objetos Python
 - Renderizar componentes React
 - ... y 50 pasos más

**Patrón correcto** (sólo lo esencial):

::

 UC: Ver Catálogo
 Flujo:
 1. Cliente solicita catálogo
 2. Sistema valida usuario
 3. Sistema retorna lista de productos
 4. Sistema muestra catálogo

**Por qué abstraer en UC:**

- **Claridad** — usuarios entienden el flujo sin tecnicismos.
- **Mantenibilidad** — cambios internos no afectan el UC.
- **Reusabilidad** — el UC puede implementarse de múltiples
  formas.
- **Comunicación** — denominador común entre stakeholders.

  Cada UC debe documentarse en al menos **dos niveles de
  abstracción** (usuario / desarrollo) cuando la implementación
  no sea trivial. Ver § 3 (ejemplo UC_ORD_01).

2.2 Herencia en modelos de datos
--------------------------------

La herencia permite crear **jerarquías de clases** donde
subclases heredan características de superclases.

**Ejemplo — jerarquía de usuarios:**

.. uml::

   @startuml

   class User {
     - id : Integer
     - email : String
     - password_hash : String
     - is_active : Boolean
     + login(email, password)
     + logout()
     + changePassword(old, new)
   }

   class ClienteUser {
     - nombre : String
     - telefono : String
     - ordenes : List<Order>
     + crearOrden()
     + verHistorial()
     + dejarReseña()
   }

   class AdminUser {
     - nombre_admin : String
     - roles : List<Role>
     - permisos : List<Permission>
     + crearProducto()
     + editarProducto()
     + verReportes()
   }

   class ModeradorUser {
     - departamento : String
     + aceptarReseña()
     + rechazarReseña()
     + responderReseña()
   }

   User <|-- ClienteUser
   User <|-- AdminUser
   User <|-- ModeradorUser
   @enduml

**Aplicación en UC_ACC:**

::

 UC_ACC_01 (Registrarse)         → Crea instancia de ClienteUser
 UC_ACC_07 (Asignar Funciones)   → Convierte ClienteUser en AdminUser
 UC_ACC_08 (Revocar Funciones)   → Revierte a ClienteUser

2.3 Polimorfismo en acciones
----------------------------

El polimorfismo permite que **métodos con el mismo nombre actúen
diferente** según el objeto.

**Ejemplo — método** ``getPrecio()``:

.. uml::

   @startuml

   class Product {
     - precio_base : Decimal
     + getPrecio() : Decimal
   }
   class ProductoConDescuento {
     - descuento_percent : Decimal
     + getPrecio() : Decimal
   }
   class ProductoVIP {
     - is_vip : Boolean
     - descuento_vip : Decimal
     + getPrecio() : Decimal
   }
   Product <|-- ProductoConDescuento
   Product <|-- ProductoVIP
   @enduml

Mismo método, comportamiento diferente:

::

 Product.getPrecio()              → return $100
 ProductoConDescuento.getPrecio() → return $100 * (1 - 0.20) = $80
 ProductoVIP.getPrecio()          → return $100 * (1 - desc_vip)  = $75

**Aplicación en UCs:**

- ``UC_PAG_03`` (Aplicar Cupón) — polimorfismo en cálculo de
  precio.
- ``UC_PRO_01`` (Crear Promoción) — diferentes tipos de
  promociones.
- ``UC_INV_01`` (Actualizar Stock) — diferentes tipos de
  ajuste.

2.4 Encapsulamiento en operaciones
----------------------------------

El encapsulamiento **oculta la complejidad interna** y muestra
sólo interfaz pública.

**Antipatrón** (expone detalles internos):

.. code-block:: python

 # Cliente tiene acceso a TODO
 order = Order()
 order.items = [item1, item2]
 order.subtotal = 99.99
 order.tax = 9.99
 order.total = 109.98
 order.status = "pending"
 order.stripe_charge_id = "ch_123abc"
 order.audit_log.append(...)        # acceso directo
 order.payment.attempt_count = 0    # manipulación

**Patrón correcto** (interfaz limpia):

.. code-block:: python

 # Cliente sólo usa interfaz pública
 order = OrderService.create_order(cart, address, payment_token)
 order.get_total()    # 109.98
 order.get_status()   # "pending"
 order.can_cancel()   # Boolean

 # Internos protegidos
 order._calculate_tax()    # privado
 order._process_payment()  # privado
 order._save_audit_log()   # privado

**Aplicación en arquitectura:**

::

 Frontend ←→ API (Interfaz Pública)
                ↓
         Django Backend (Lógica Privada)
                ↓
         Base de Datos

2.5 Envío de mensajes entre UCs
-------------------------------

Los UCs se comunican mediante **mensajes** (llamadas a
métodos/endpoints).

**Ejemplo — flujo de órdenes:**

.. uml::

   @startuml

   participant "UC_CAT_06\nVer Detalles"     as UC1
   participant "UC_CAR_01\nAgregar Carrito"  as UC2
   participant "UC_ORD_01\nCrear Orden"      as UC3
   participant "UC_PAG_01\nProcesar Pago"    as UC4
   participant "UC_LOG_01\nConsultar Envío"  as UC5

   UC1 -> UC2 : 1. producto seleccionado
   UC2 -> UC3 : 2. carrito listo para checkout
   UC3 -> UC5 : 3. consultar opciones envío
   UC5 --> UC3 : 4. opciones disponibles
   UC3 -> UC4 : 5. procesar pago
   UC4 --> UC3 : 6. pago autorizado
   UC3 --> UC2 : 7. orden creada
   @enduml

2.6 Asociaciones entre UCs
--------------------------

Las asociaciones representan **relaciones formales** entre UCs.

**Tipos:**

.. uml::

   @startuml

   left to right direction
   usecase "UC_ACC_02\nLogin"                  as UcAcc02Login
   usecase "UC_ACC_04\nRenovar Token"          as UcAcc04RenovarToken
   usecase "UC_ORD_01\nCrear Orden"            as UcOrd01CrearOrden
   usecase "UC_PAG_01\nProcesar Pago"          as UcPag01ProcesarPago
   usecase "UC_ORD_06\nSolicitar Devolución"   as UcOrd06SolicitarDevolucion
   usecase "UC_LOG_06\nCrear Devolución"       as UcLog06CrearDevolucion
   usecase "UC_CAT_06\nVer Detalles"           as UcCat06VerDetalles
   usecase "UC_CAT_01\nVer Catálogo"           as UcCat01VerCatalogo

   UcAcc02Login ..> UcAcc04RenovarToken : <<include>>
   UcOrd01CrearOrden ..> UcPag01ProcesarPago : <<include>>
   UcOrd06SolicitarDevolucion ..> UcLog06CrearDevolucion : <<extend>>
   UcCat06VerDetalles --> UcCat01VerCatalogo : depende de
   @enduml

----

3. Patrones OOP en diagramas — referencia rápida
================================================

Para la fundamentación detallada de cada patrón, ver:

- :doc:`/base-cognitiva/_uml/uml-02-orientacion-objetos/index`
  (herencia, polimorfismo, encapsulamiento, mensajes,
  asociaciones, agregación, composición).
- :doc:`/base-cognitiva/_uml/uml-04-uso-relaciones/index`
  (asociación binaria, reflexiva, calificada, generalización,
  dependencia).

Resumen para uso en UCs del proyecto:

.. list-table::
 :widths: 20 35 45
 :header-rows: 1

 * - Patrón
   - Símbolo PlantUML
   - Cuándo usarlo en un UC del proyecto
 * - **Herencia**
   - ``A <|-- B``
   - El UC reutiliza estructura/comportamiento de otro UC
 * - **Composición**
   - ``A *-- B``
   - El componente no tiene sentido sin el todo (Order ↔
     OrderItem)
 * - **Agregación**
   - ``A o-- B``
   - Las partes pueden existir sin el todo (Department ↔
     Employee)
 * - **Asociación**
   - ``A -- B``
   - Relación genérica (User ↔ Cart)
 * - **Dependencia**
   - ``A ..> B``
   - Una clase usa a otra temporalmente
 * - **Realización**
   - ``A ..|> B``
   - Implementación de interfaz

----

4. Ejemplo completo — UC_ORD_01 Crear Orden
===========================================

Este ejemplo aplica las seis dimensiones a un UC crítico.

4.1 Abstracción — tres niveles
------------------------------

**Nivel 0 (USUARIO):**

::

 "Quiero crear una orden"

**Nivel 1 (PRODUCTO):**

::

 UC_ORD_01: Crear Orden
 1. Cliente selecciona productos
 2. Sistema calcula total
 3. Cliente confirma orden

**Nivel 2 (DESARROLLO):**

::

 UC_ORD_01: Crear Orden
 1. POST /api/orders {cart_id, address_id, payment_token}
 2. Validar carrito (cantidad, disponibilidad)
 3. Validar dirección (formato, cobertura logística)
 4. Consultar logística (opciones envío)
 5. Procesar pago (Stripe)
 6. Crear orden + items + payment en BD (transacción ACID)
 7. Auditar cambio
 8. Enviar notificación
 9. Retornar {order_id, status, total}

4.2 Encapsulamiento — capas
---------------------------

.. uml::

   @startuml

   package "INTERFAZ PÚBLICA (Frontend)" as Front {
     component "Formulario Checkout" as FormularioCheckout
     component "Botón Confirmar"     as Btn
   }

   package "LÓGICA PRIVADA (Backend)" as Back {
     component "Validar datos"        as Val
     component "Calcular totales"     as Calc
     component "Guardar en BD"        as GuardarEnBd
     component "Registrar auditoría"  as Aud
   }

   package "SERVICIOS EXTERNOS" as Ext {
     component "Stripe API"  as StripeApi
     component "Email Service" as EmailService
   }

   FormularioCheckout -> Btn : submit
   Btn -> Back : llama (interfaz pública)
   Back ..> Val  : <<protegido>>
   Back ..> Calc : <<protegido>>
   Back ..> GuardarEnBd   : <<protegido>>
   Back ..> Aud  : <<protegido>>
   Back -> StripeApi : HTTPS
   Back -> EmailService : HTTPS
   @enduml

4.3 Envío de mensajes — secuencia
---------------------------------

.. uml::

   @startuml

   actor Cliente
   participant ":Frontend" as Frontend
   participant ":Backend"  as Backend
   participant ":Logística" as LogStica
   participant ":Stripe"   as Stripe
   participant ":Email"    as Email

   Cliente -> Frontend : confirmar compra
   Frontend -> Backend       : POST /orders
   Backend -> LogStica       : consultar envío
   LogStica --> Backend      : opciones disponibles
   Backend -> Stripe       : procesar pago
   Stripe --> Backend      : pago aprobado
   Backend -> Backend       : crear orden (interno)
   Backend -> Email       : enviar confirmación
   Email --> Backend      : email enviado
   Backend --> Frontend      : orden creada
   Frontend --> Cliente : mostrar confirmación
   @enduml

4.4 Polimorfismo — variantes de Order
-------------------------------------

.. uml::

   @startuml

   abstract class Order {
     + calculateTotal() : Decimal
     + getDiscount() : Decimal
   }
   class OrderRegular {
     + calculateTotal() : Decimal
     + getDiscount() : Decimal
   }
   class OrderVIP {
     + calculateTotal() : Decimal
     + getDiscount() : Decimal
   }
   class OrderBlackFriday {
     + calculateTotal() : Decimal
     + getDiscount() : Decimal
   }
   Order <|-- OrderRegular
   Order <|-- OrderVIP
   Order <|-- OrderBlackFriday
   @enduml

Mismo método, comportamiento diferente:

::

 OrderRegular.calculateTotal()      → $100 + $10 tax           = $110
 OrderVIP.calculateTotal()          → $100 + $10 tax - $20 VIP = $90
 OrderBlackFriday.calculateTotal()  → $100 + $10 tax - $50 BF  = $60

----

5. Aplicación a los 13 documentos del plan
==========================================

Cada UC documentado per
:doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc` debe incluir:

- ✓ **Abstracción** — niveles de detalle (mínimo: usuario,
  producto; añadir desarrollo si es complejo).
- ✓ **Encapsulamiento** — interfaz pública vs lógica privada.
- ✓ **Herencia** — UCs que reutilizan código.
- ✓ **Polimorfismo** — variaciones documentadas.
- ✓ **Envío de mensajes** — diagramas de secuencias.
- ✓ **Asociaciones** — relaciones ``<<include>>`` /
  ``<<extend>>`` / generalización.

**Ejemplo de aplicación — DOC-14 (UC_ACC):**

::

 UC_ACC_01: Registrarse
 ├─ Abstracción: oculta hashing, validación email
 ├─ Encapsulamiento: interfaz pública (email, password)
 ├─ Polimorfismo: tipos de registro (social, email)
 ├─ Envío de mensajes: Usuario → Frontend → Backend → BD
 └─ Diagramas PlantUML: UC, Clases, Secuencias, Actividades

 UC_ACC_02: Login
 ├─ Abstracción: oculta JWT, cookies, sessions
 ├─ Encapsulamiento: interfaz limpia (email, password)
 ├─ Herencia: reutiliza código de UC_ACC_01
 ├─ Envío de mensajes: diagrama de secuencias con tokens
 └─ Diagramas PlantUML: UC, Secuencias [CRÍTICO], Estados

----

6. Checklist de calidad OOP
===========================

Para cada UC documentado, validar las **seis dimensiones**:

**Abstracción:**

- [ ] El UC muestra sólo lo necesario (sin tecnicismos)
- [ ] Detalles internos ocultos en diagramas privados
- [ ] Niveles de abstracción claros (mínimo dos)

**Encapsulamiento:**

- [ ] Interfaz pública claramente definida
- [ ] Datos privados protegidos (``-`` o ``#``)
- [ ] Cambios internos no afectan al UC externo

**Herencia:**

- [ ] Reutilización de código identificada
- [ ] Jerarquía de UCs clara
- [ ] No hay duplicación de pasos entre UCs

**Polimorfismo:**

- [ ] Variaciones de comportamiento documentadas
- [ ] Mismo nombre, diferente implementación
- [ ] Reglas de negocio por tipo

**Envío de mensajes:**

- [ ] Flujo de comunicación claro
- [ ] Orden de mensajes correcto
- [ ] Respuestas esperadas documentadas

**Asociaciones:**

- [ ] Relaciones ``<<include>>`` claras
- [ ] Relaciones ``<<extend>>`` claras
- [ ] Dependencias documentadas

----

7. Trazabilidad
===============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``ba-requirements-analysis`` (BABOK — Requirements Analysis
     and Design Definition)
 * - **Origen del estándar**
   - Adaptado de "INTEGRACIÓN UML + OOP + MERMAID v3.0.0"
     (propuesta interna), reescrito para PlantUML.
 * - **Fundamentos UML/OOP**
   - :doc:`/base-cognitiva/_uml/uml-02-orientacion-objetos/index`,
     :doc:`/base-cognitiva/_uml/uml-04-uso-relaciones/index`
 * - **Plantilla aplicable**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Plan de aplicación**
   - :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
