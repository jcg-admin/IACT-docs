.. meta::
 :artefacto: METODOLOGIA_ANALISIS_DOMINIO_UC
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
Metodología de Análisis de Dominio para UCs
================================================================

.. note::

 Estándar metodológico que prescribe **cómo extraer clases,
 operaciones y atributos a partir del lenguaje del dominio**
 (entrevistas con clientes y descripciones de casos de uso).

 Aplica al documentar los **97 UCs** del proyecto IACT per
 :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`. Es paso
 **upstream** de
 :doc:`/normativa/estandares/metodologia-oop-para-ucs` —
 primero se descubren las clases, luego se aplican las seis
 dimensiones OOP.

 Diagramas en **PlantUML** (política del proyecto, no Mermaid).

 **Ejemplos canónicos aplicados al dominio IACT:** ver
 :doc:`/requisitos/_metodologia-aplicacion/analisis-dominio/index`
 para la técnica aplicada al dominio real (sustantivos del
 ecosistema call center IVR / RBAC / ETL).

----

1. La técnica — sustantivos, verbos, adjetivos
==============================================

**Principio fundamental** (UML, Schmuller cap. 3):

.. list-table::
 :widths: 30 30 40
 :header-rows: 1

 * - Categoría gramatical
   - Se convierte en
   - Notación PlantUML
 * - **Sustantivos**
   - Clases
   - ``class Nombre``
 * - **Verbos**
   - Operaciones (métodos)
   - ``+ verbo()``
 * - **Adjetivos**
   - Atributos (propiedades)
   - ``- adjetivo : Boolean``

Para los fundamentos de esta técnica ver
:doc:`/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index`
§ "Qué hacen las clases y cómo encontrarlas" (ejemplo del
entrenador de baloncesto).

----

2. Ejemplo completo — sistema de Ecommerce
==========================================

2.1 Conversación con el cliente
-------------------------------

  *"Necesito un sistema donde los clientes pueden ver un
  catálogo de productos, agregar items a un carrito de compras,
  y crear una orden. El cliente puede aplicar un cupón de
  descuento en el checkout. Después de la compra, el sistema
  debe enviar una confirmación por email. El administrador
  puede gestionar productos, reportes y usuarios."*

2.2 Extracción de sustantivos
-----------------------------

::

 Cliente, Catálogo, Producto, Carrito, Compras, Orden,
 Cupón, Descuento, Checkout, Email, Confirmación,
 Administrador, Reportes, Usuarios

→ **Clases candidatas:**

::

 Cliente / Catalogo / Producto / Carrito / Orden / Cupon /
 Descuento / Email / Administrador / Reporte / Usuario

2.3 Extracción de verbos
------------------------

::

 Ver (catálogo)        → +verCatalogo()
 Agregar (al carrito)  → +agregarAlCarrito(producto, cantidad)
 Crear (orden)         → +crearOrden(carrito, direccion)
 Aplicar (cupón)       → +aplicarCupon(codigo)
 Enviar (email)        → +enviarEmail(template, destinatario)
 Gestionar (productos) → +crearProducto() / +editarProducto() / ...
 Comprar               → +procesarCompra()

2.4 Extracción de adjetivos
---------------------------

::

 Activo (usuario)      → is_active : Boolean
 Disponible (producto) → available : Boolean
 Confirmado (orden)    → confirmed : Boolean

2.5 Diagrama de clases del dominio Ecommerce (PlantUML)
-------------------------------------------------------

.. uml::

   @startuml

   class User {
     - id : Integer
     - email : String
     - password_hash : String
     - name : String
     - is_active : Boolean
     - orders : List<Order>
     + register(email, password)
     + login(email, password)
     + logout()
     + changePassword(old, new)
     + viewOrderHistory()
     + createOrder()
   }

   class Catalog {
     - id : Integer
     - name : String
     - products : List<Product>
     - categories : List<Category>
     + viewProducts()
     + searchProduct(term)
     + filterByCategory(category)
     + filterByPrice(min, max)
     + sortResults(field)
   }

   class Product {
     - id : Integer
     - sku : String
     - name : String
     - description : String
     - price : Decimal
     - stock : Integer
     - category : Category
     - reviews : List<Review>
     + getDetails()
     + updateStock(quantity)
     + addReview(text, rating)
   }

   class Category {
     - id : Integer
     - name : String
     - slug : String
     - products : List<Product>
   }

   class Cart {
     - id : Integer
     - owner : User
     - items : List<CartItem>
     - created_at : DateTime
     + addItem(product, quantity)
     + removeItem(product)
     + changeQuantity(product, new_quantity)
     + calculateTotal()
     + emptyCart()
   }

   class CartItem {
     - id : Integer
     - product : Product
     - quantity : Integer
     - unit_price : Decimal
     + calculateSubtotal()
   }

   class Order {
     - id : Integer
     - order_number : String
     - client : User
     - status : String
     - subtotal : Decimal
     - tax : Decimal
     - total : Decimal
     - items : List<OrderItem>
     - payment : Payment
     - shipping_address : ShippingAddress
     - created_at : DateTime
     + createFromCart(cart)
     + calculateTotal()
     + updateStatus(newStatus)
     + requestRefund()
     + downloadInvoice()
   }

   class OrderItem {
     - id : Integer
     - product : Product
     - quantity : Integer
     - unit_price : Decimal
   }

   class Payment {
     - id : Integer
     - order : Order
     - amount : Decimal
     - status : String
     - stripe_charge_id : String
     - processed_at : DateTime
     + processPayment(token)
     + refund()
   }

   class Coupon {
     - id : Integer
     - code : String
     - discount_percent : Decimal
     - expiration_date : DateTime
     - max_uses : Integer
     - current_uses : Integer
     + applyTo(order)
     + validate()
     + incrementUses()
   }

   class ShippingAddress {
     - id : Integer
     - user : User
     - street : String
     - city : String
     - state : String
     - postal_code : String
     - country : String
     + validate()
     + verifyCoverage()
   }

   class Email {
     - id : Integer
     - recipient : String
     - subject : String
     - body : String
     - template : String
     - sent_at : DateTime
     + generate(template, data)
     + send()
     + recordSent()
   }

   class Review {
     - id : Integer
     - author : User
     - product : Product
     - rating : Integer
     - text : String
     - approved : Boolean
     + createReview()
     + acceptReview()
     + rejectReview()
   }

   class Administrator {
     - id : Integer
     - admin_name : String
     - roles : List<Role>
     + createProduct()
     + editProduct(id)
     + deleteProduct(id)
     + viewReports()
     + manageUsers()
   }

   class Report {
     - id : Integer
     - type : String
     - name : String
     - generated_at : DateTime
     + generate()
     + exportCSV()
     + exportPDF()
   }

   User "1" --> "*" Order
   User "1" --> "1" Cart
   Cart "1" --> "*" CartItem
   CartItem "1" --> "1" Product
   Order "1" --> "*" OrderItem
   OrderItem "1" --> "1" Product
   Order "1" --> "1" Payment
   Order "1" --> "1" ShippingAddress
   Product "1" --> "1" Category
   Product "*" --> "*" Review
   Coupon "1" --> "*" Order
   Catalog "1" --> "*" Product
   Catalog "1" --> "*" Category
   User <|-- Administrator
   @enduml

----

3. Estructura UML completa de una clase
=======================================

Una clase completa especifica **atributos, operaciones,
responsabilidades y restricciones**:

.. uml::

   @startuml

   class Usuario {
     .. atributos básicos ..
     - id : Integer
     - email : String
     - password_hash : String
     .. atributos personales ..
     - nombre : String
     - apellido : String
     - telefono : String = "+1234567890"
     .. atributos de estado ..
     - is_active : Boolean = true
     - is_verified : Boolean = false
     - created_at : DateTime
     - updated_at : DateTime
     - last_login : DateTime
     == operaciones de autenticación ==
     + login(email : String, password : String) : Boolean
     + logout()
     + changePassword(old : String, new : String) : void
     + forgotPassword(email : String) : void
     == operaciones de perfil ==
     + updateProfile(nombre, telefono) : void
     + getProfile() : UserProfile
     + deleteAccount() : void
     -- responsabilidades --
     mantener identidad segura del usuario
     facilitar autenticación y autorización
     proteger datos personales
   }
   note right of Usuario
     {email: formato válido RFC5322}
     {password: mínimo 8 caracteres}
     {is_active: true | false}
   end note
   @enduml

**Convención de visibilidad:**

- ``+`` público (cualquier clase puede acceder)
- ``-`` privado (sólo la clase original)
- ``#`` protegido (clase y subclases)

----

4. Descubrimiento por tema (extracto de los 13 docs)
====================================================

4.1 Tema ACCESS (autenticación)
-------------------------------

**Sustantivos:**

::

 Usuario, Contraseña, Sesión, Token, Rol, Permiso, Grupo,
 AuditLog, Email, Verificación

**Clases derivadas:** ``User``, ``Role``, ``Permission``,
``Group``, ``Session``, ``AuditLog``, ``EmailVerification``.

**Verbos:**

::

 Registrarse, Login, Logout, Cambiar contraseña, Recuperar,
 Asignar, Revocar, Bloquear, Auditar

**Operaciones derivadas:** ``+registrarse()``, ``+login()``,
``+logout()``, ``+changePassword()``, ``+forgotPassword()``,
``+assignRole()``, ``+revokeRole()``, ``+blockUser()``,
``+auditChanges()``.

.. uml::

   @startuml

   class User {
     - id : Integer
     - email : String
     - password_hash : String
     - is_active : Boolean
     + login(email, password) : Boolean
     + logout()
     + changePassword(old, new)
   }

   class Role {
     - id : Integer
     - nombre : String
     - permisos : List<Permission>
     + addPermission(perm)
     + removePermission(perm)
   }

   class Permission {
     - id : Integer
     - codigo : String
     - descripcion : String
   }

   class AuditLog {
     - id : Integer
     - user_id : Integer
     - accion : String
     - timestamp : DateTime
     + registrar(user, accion)
   }

   User "1" --> "*" Role
   Role "1" --> "*" Permission
   User "1" --> "*" AuditLog
   @enduml

4.2 Tema CATÁLOGO (productos)
-----------------------------

**Sustantivos:** Producto, Categoría, Descripción, Precio,
Stock, Imagen, Atributo, Variante, Reseña, Rating.

**Clases:** ``Product``, ``Category``, ``ProductImage``,
``ProductAttribute``, ``ProductVariant``, ``Review``, ``Stock``.

**Verbos:** Ver, Buscar, Filtrar, Ordenar, Crear, Editar,
Eliminar, Agregar imagen, Crear variante.

.. uml::

   @startuml

   class Product {
     - id : Integer
     - sku : String
     - nombre : String
     - precio : Decimal
     - stock : Integer
     - categoria : Category
     + getDetalles() : ProductDetail
     + updateStock(qty)
     + addImage(url)
     + createVariant()
   }

   class Category {
     - id : Integer
     - nombre : String
     - productos : List<Product>
   }

   class ProductImage {
     - id : Integer
     - product_id : Integer
     - url : String
     - orden : Integer
   }

   class Stock {
     - id : Integer
     - product_id : Integer
     - cantidad : Integer
     - warehouse : String
     + updateCantidad(qty)
   }

   Product "1" --> "*" ProductImage
   Product "1" --> "*" Stock
   Product "1" --> "1" Category
   @enduml

4.3 Tema ÓRDENES (pedidos)
--------------------------

**Sustantivos:** Orden, Item, Cliente, Estado, Total, Impuesto,
Descuento, Dirección, Entrega, Rastreo.

**Clases:** ``Order``, ``OrderItem``, ``OrderStatus``,
``ShippingAddress``, ``Tracking``, ``Invoice``.

**Verbos:** Crear, Calcular, Actualizar estado, Solicitar
devolución, Descargar factura, Rastrear.

  El descubrimiento detallado de cada uno de los 13 temas vive
  en cada uno de los documentos de
  :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc` (DOC-14..26).

----

5. Paquetes UML — organización arquitectónica
=============================================

Los **paquetes** organizan clases en grupos lógicos
(``Authentication``, ``Catalog``, ``Orders``, ``Payments``,
``Notifications``).

.. uml::

   @startuml

   package "Authentication" {
     class User
     class Role
     class Permission
   }

   package "Catalog" {
     class Product
     class Category
     class Stock
   }

   package "Orders" {
     class Order
     class OrderItem
     class Shipment
   }

   package "Payments" {
     class Payment
     class Transaction
     class Invoice
   }

   package "Notifications" {
     class Email
     class SMS
     class Notification
   }
   @enduml

**Nombres de ruta** (*fully qualified names*):

::

 Authentication::User
 Authentication::Role
 Catalog::Product
 Catalog::Category
 Orders::Order
 Payments::Payment
 Notifications::Email

----

6. Metodología de cinco pasos por UC
====================================

6.1 Paso 1 — extraer sustantivos del UC
---------------------------------------

Identificar **todos los sustantivos** en la descripción del UC.
Cada sustantivo es una clase candidata.

**Ejemplo — UC_ORD_01 (Crear orden):**

  *"El cliente selecciona productos del carrito, proporciona
  dirección de envío, aplica cupón si tiene, y procesa el pago
  para crear la orden."*

::

 Cliente   → class Cliente (heredar de User)
 Carrito   → class Carrito (ya existe)
 Producto  → class Producto (ya existe)
 Dirección → class DireccionEnvio (nueva)
 Cupón     → class Cupon (nueva)
 Pago      → class Pago (nueva)
 Orden     → class Orden (nueva)

6.2 Paso 2 — extraer verbos del UC
----------------------------------

::

 Seleccionar  → Product.select()
 Proporcionar → Cliente.provideDireccion()
 Aplicar      → Cupon.aplicar(orden)
 Procesar     → Pago.procesarPago()
 Crear        → Orden.crear(cliente, carrito, pago)

6.3 Paso 3 — diagrama de clases involucradas
--------------------------------------------

.. uml::

   @startuml

   class User {
     - id : Integer
     - email : String
   }

   class Cliente {
     - nombre : String
     - direccion : DireccionEnvio
     + crearOrden(carrito) : Orden
   }

   class Carrito {
     - items : List<CartItem>
     - total : Decimal
     + getTotal() : Decimal
   }

   class Orden {
     - numero : String
     - cliente : Cliente
     - items : List<OrdenItem>
     - pago : Pago
     - status : String
     + crear(cliente, carrito) : Orden
     + calcularTotal() : Decimal
   }

   class Pago {
     - monto : Decimal
     - status : String
     - stripe_id : String
     + procesarPago(token) : Boolean
   }

   class Cupon {
     - codigo : String
     - descuento : Decimal
     + aplicar(orden) : void
   }

   User <|-- Cliente
   Orden "1" --> "1" Pago
   Orden "1" --> "*" CartItem
   Cupon "1" --> "1" Orden
   @enduml

6.4 Paso 4 — especificar responsabilidades
------------------------------------------

::

 Orden:
   - Representar una compra completada del cliente.
   - Garantizar que contenga todos los detalles de la
     transacción.
   - Mantener integridad de datos de pago.
   - Permitir rastreo del envío.

 Pago:
   - Procesar transacciones monetarias con seguridad.
   - Comunicarse con Stripe de forma segura.
   - Mantener cumplimiento PCI-DSS.
   - Registrar cambios en auditoría.

6.5 Paso 5 — especificar restricciones
--------------------------------------

.. uml::

   @startuml

   class Orden {
     - numero_orden : String
     - status : OrderStatus
     - total : Decimal
   }
   note right of Orden
     {numero_orden: único, autoincremental}
     {status: PENDING|CONFIRMED|SHIPPED|DELIVERED|CANCELLED}
     {total: >= 0.00}
     {cada OrdenItem.cantidad >= 1}
     {total = SUM(OrdenItem.precio_unitario × cantidad) + tax}
   end note

   class Pago {
     - monto : Decimal
     - status : PaymentStatus
   }
   note right of Pago
     {monto: > 0}
     {status: PENDING|AUTHORIZED|CAPTURED|REFUNDED|FAILED}
     {monto == Orden.total}
   end note
   @enduml

----

7. Formato de cada documento UC
===============================

Cada documento generado per
:doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc` debe contener:

::

 DOC-XX: UC_[TEMA] (nombre)

 ├─ 1. DESCUBRIMIENTO DE DOMINIO
 │    ├─ Sustantivos identificados
 │    ├─ Verbos identificados
 │    └─ Adjetivos / restricciones
 │
 ├─ 2. DIAGRAMA DE CLASES UML (PlantUML)
 │    ├─ Clases involucradas
 │    ├─ Atributos por clase
 │    ├─ Operaciones por clase
 │    └─ Relaciones entre clases
 │
 ├─ 3. PAQUETES Y ORGANIZACIÓN
 │    └─ Nombre de ruta completo (Package::Class)
 │
 ├─ 4. RESPONSABILIDADES
 │    ├─ Por clase
 │    └─ Por UC
 │
 ├─ 5. RESTRICCIONES Y REGLAS
 │    ├─ Restricciones (notación informal {…})
 │    └─ Reglas de negocio
 │
 ├─ 6. ESPECIFICACIÓN DEL CASO DE USO
 │    ├─ Precondiciones
 │    ├─ Flujo principal
 │    ├─ Flujos alternativos
 │    └─ Postcondiciones
 │
 ├─ 7. DIAGRAMAS PLANTUML
 │    ├─ Diagrama de casos de uso
 │    ├─ Diagrama de clases
 │    ├─ Diagrama de secuencias
 │    ├─ Diagrama de actividades
 │    └─ Diagrama de estados (si aplica)
 │
 └─ 8. CASOS DE PRUEBA DERIVADOS
      ├─ Por clase
      ├─ Por operación
      └─ Por restricción

----

8. Checklist de calidad — análisis de dominio
=============================================

**Análisis de dominio:**

- [ ] Sustantivos identificados correctamente
- [ ] Verbos mapeados a operaciones
- [ ] Adjetivos convertidos en atributos
- [ ] Clases organizadas en paquetes

**Diseño de clases:**

- [ ] Cada clase tiene responsabilidad clara
- [ ] Atributos con tipos correctos
- [ ] Operaciones con firma completa (parámetros + tipo de
  retorno)
- [ ] Relaciones entre clases documentadas (asociación,
  composición, agregación, herencia)

**Diagramas UML (PlantUML):**

- [ ] Diagrama de casos de uso con actores
- [ ] Diagrama de clases con paquetes
- [ ] Diagrama de secuencias para flujos críticos
- [ ] Diagrama de estados para transiciones (si aplica)
- [ ] Diagrama de actividades para flujos complejos (si
  aplica)

**Calidad:**

- [ ] Coherencia con otros UCs del mismo paquete
- [ ] Nomenclatura consistente: ``PascalCase`` para clases,
  ``camelCase`` para atributos y operaciones
- [ ] Restricciones explícitas en notas o entre llaves ``{…}``
- [ ] Documentación completa según la plantilla canónica

----

9. Trazabilidad
===============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill aplicada**
   - ``ba-elicitation`` (BABOK — Elicitation and Collaboration)
 * - **Origen del estándar**
   - Adaptado de "INTEGRACIÓN UML + OOP + ANÁLISIS DE DOMINIO +
     MERMAID v4.0.0" (propuesta interna), reescrito para
     PlantUML.
 * - **Fundamento UML**
   - :doc:`/base-cognitiva/_uml/uml-03-uso-orientacion-objetos/index`
     (técnica original de Schmuller con el ejemplo del
     entrenador de baloncesto)
 * - **Metodología hermana (OOP)**
   - :doc:`/normativa/estandares/metodologia-oop-para-ucs`
 * - **Plantilla aplicable**
   - :doc:`/normativa/estandares/plantillas/tpl-uc-spec-con-diagramas-uml`
 * - **Plan de aplicación**
   - :doc:`/requisitos/_metodologia-aplicacion/plan-documentacion-uc`
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
