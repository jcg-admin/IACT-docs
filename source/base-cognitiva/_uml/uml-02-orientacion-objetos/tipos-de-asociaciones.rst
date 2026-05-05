Tipos de asociaciones
---------------------

**Cardinalidad** — Especifica cuántos objetos pueden participar
en una asociación. Esto puede variar de uno a uno, uno a muchos o
muchos a muchos, y es fundamental para definir la cantidad de
interacciones posibles entre objetos en un sistema. **Define
cuántos objetos pueden participar en la asociación.**

**Asociación Unidireccional** — En esta relación, un objeto
conoce a otro, pero el segundo objeto no tiene conocimiento del
primero. Se puede pensar como una conexión en una sola dirección.
**Solo un objeto conoce al otro.**

Ejemplos:

- Un profesor enseña a un estudiante.
- Un objeto ``Cliente`` tiene un ``Pedido``. El ``Pedido`` no
  necesita saber quién es el ``Cliente``.
- ``Cliente → Pedido`` (el cliente conoce el pedido, pero el
  pedido no conoce al cliente).

.. uml::

   @startuml

   class Cliente
   class Pedido
   Cliente --> Pedido : tiene
   @enduml

**Agregación** — Representa una relación "todo/parte", donde la
parte puede existir independientemente del todo. La vida de la
parte no está controlada por el todo. **Relación en la que un
objeto es parte de otro, pero ambos pueden existir de forma
independiente.**

Características:

- Las partes pueden ser compartidas por múltiples "todo".
- El ciclo de vida de las partes no está ligado al del todo.
- Se conoce como una relación de **"parte-todo"**.

Ejemplos:

- "Un coche tiene llantas". Si el coche es destruido, las llantas
  pueden existir por separado.
- ``Biblioteca ⟶ Libro`` (la biblioteca puede tener libros, pero
  los libros pueden existir independientemente de la biblioteca).
- **Universidad y Estudiantes:** una universidad tiene
  estudiantes, pero los estudiantes pueden existir sin la
  universidad.
- **Equipo de Fútbol y Jugadores:** un equipo está compuesto por
  jugadores, pero los jugadores pueden jugar en otros equipos.
- **Carro y Componentes:** un carro está compuesto por motor,
  ruedas y asientos, pero estos componentes pueden existir
  independientemente del carro.
- **Casa y Habitaciones:** una casa está formada por varias
  habitaciones, pero cada habitación puede ser parte de otra casa
  o existir como unidad independiente.

.. uml::

   @startuml

   class Biblioteca
   class Libro
   Biblioteca o-- "0..*" Libro
   @enduml

**Composición** — Es un tipo más fuerte de agregación donde la
parte no puede existir sin el todo. Si el todo es destruido,
también lo son sus partes. **Relación en la que un objeto depende
completamente de otro para existir.**

Características:

- Si el "todo" se destruye, las partes también lo hacen.
- Relación de propiedad exclusiva.
- El ciclo de vida de las partes está estrictamente ligado al
  ciclo de vida del todo.

Ejemplos:

- Un objeto ``Casa`` y un objeto ``Habitacion``. Una habitación
  no tiene sentido fuera de la casa.
- "Una casa tiene habitaciones". Si la casa es destruida, las
  habitaciones también dejan de existir.
- ``Equipo ⟶ Miembro`` (si el equipo es destruido, también lo son
  sus miembros, en el contexto del equipo específico).
- Un libro y sus capítulos: si el libro deja de existir, los
  capítulos también desaparecen.

.. uml::

   @startuml

   class Casa
   class Habitacion
   Casa *-- "1..*" Habitacion
   @enduml

**Dependencia** — Relación temporal en la que un objeto depende
de otro para realizar una tarea o función específica, pero la
relación no es permanente. **Relación temporal entre objetos,
donde uno depende del otro para realizar una tarea.**

Características:

- Es una relación temporal donde un objeto depende de otro para
  realizar una tarea específica.
- No implica propiedad.
- Cuando un objeto utiliza o invoca un servicio de otro objeto,
  la relación se da en el momento en que el objeto dependiente
  necesita al proveedor para realizar su función.
- Es una relación débil y temporal.
- Cuando un objeto se ve afectado por un cambio en otro objeto:
  cualquier modificación en el objeto proveedor puede impactar al
  objeto dependiente.
- Esta relación es menos formal y más efímera que las otras
  asociaciones.

Ejemplos:

- **Cliente y Pedido:** un cliente hace un pedido a una tienda;
  el cliente depende del sistema de pedidos para completar la
  acción.
- **Usuario y Aplicación:** un usuario utiliza una aplicación
  para obtener información; la aplicación es necesaria para que
  el usuario acceda a esa información.
- **Cliente y Catálogo de Productos:** si el catálogo de productos
  se actualiza, el cliente puede ver diferentes opciones
  disponibles.
- **Sistema de Notificaciones y Configuración de Usuario:** si un
  usuario cambia sus preferencias de notificación, el sistema de
  notificaciones depende de esos cambios para funcionar
  correctamente.
- **Interfaz y Clase Concreta:** una clase concreta implementa
  una interfaz; si la interfaz cambia, la clase concreta puede
  verse afectada.
- **Módulos de Sistema y Bibliotecas Externas:** un módulo de
  software puede depender de una biblioteca externa para funciones
  específicas; cambios en la biblioteca pueden afectar el módulo.

.. uml::

   @startuml

   class Cliente
   class CatalogoProductos
   Cliente ..> CatalogoProductos : <<usa>>
   @enduml

**Herencia (Generalización)** — Relación jerárquica entre clases
en la que una clase (subclase o clase derivada) hereda atributos
y comportamientos de otra clase (superclase o clase base). Esta
relación permite **reutilizar el código** y crear una estructura
de clases más organizada y comprensible.

Características:

- **Herencia Simple:** una clase hereda de una sola superclase,
  manteniendo una estructura jerárquica simple.
- **Herencia Múltiple:** una clase puede heredar de múltiples
  superclases. Esto permite combinar características de diferentes
  clases, pero puede complicar la jerarquía y la resolución de
  conflictos.
- **Herencia Jerárquica:** varias clases derivadas heredan de una
  sola superclase, formando una estructura jerárquica donde una
  clase base tiene múltiples subclases.

Ejemplos:

- **Animal y Perro:** la clase ``Perro`` hereda de la clase
  ``Animal``, adquiriendo sus atributos y métodos.
- **Animal y Perro, Gato:** la clase ``Animal`` tiene dos
  subclases (``Perro`` y ``Gato``), cada una heredando de
  ``Animal``.
- **Vehículo y Coche:** la clase ``Coche`` hereda de la clase
  ``Vehiculo``.
- **Ave y Volador:** la clase ``Pajaro`` puede heredar de ``Ave``
  y de ``Volador`` (herencia múltiple).
- **Estudiante y Trabajador:** la clase ``EstudianteTrabajador``
  hereda de las clases ``Estudiante`` y ``Trabajador``,
  combinando las características de ambas.
- **Vehículo y Coche, Motocicleta:** la clase ``Vehiculo`` tiene
  subclases ``Coche`` y ``Motocicleta``.

.. uml::

   @startuml

   class Animal
   class Perro
   class Gato
   Animal <|-- Perro
   Animal <|-- Gato
   @enduml

**Cardinalidad (o Multiplicidad)** — Define **cuántos objetos**
pueden participar en la asociación.

Se puede definir como:

- **Uno a uno (1:1):** un objeto A está relacionado con un solo
  objeto B. Ejemplo: "Un pasaporte pertenece a una persona".
- **Uno a muchos (1:\*):** un objeto A puede estar relacionado
  con muchos objetos B. Ejemplo: "Un profesor enseña a muchos
  estudiantes".
- **Muchos a muchos (\*:\*):** muchos objetos A pueden estar
  relacionados con muchos objetos B. Ejemplo: "Un autor puede
  escribir varios libros, y un libro puede tener varios autores".

**Asociación Bidireccional** — Ambos objetos son conscientes de
la relación y pueden interactuar entre sí. Cada objeto conoce al
otro. **Ambos objetos se conocen y pueden interactuar.**

Ejemplos:

- Un objeto ``Profesor`` y un objeto ``Curso``. Un ``Curso``
  conoce a su ``Profesor`` y viceversa.
- Una persona posee un automóvil.
- ``Profesor ↔ Curso`` (ambos objetos se conocen y pueden
  interactuar).

.. uml::

   @startuml

   class Profesor
   class Curso
   Profesor "1" -- "1..*" Curso
   @enduml

**Asociación Binaria** — Relación entre exactamente dos objetos.

Ejemplos:

- **Cliente y Pedido:** un cliente puede realizar múltiples
  pedidos, pero un pedido pertenece a un solo cliente.
- **Estudiante y Curso:** un estudiante puede estar inscrito en
  varios cursos, pero un curso puede tener muchos estudiantes.

**Asociación Unaria** — Relación de un objeto consigo mismo.

Ejemplos:

- **Empleado y Supervisor:** un empleado puede supervisar a otros
  empleados.
- **Árbol y Rama:** una rama puede tener subramas, que también son
  ramas.

.. uml::

   @startuml

   class Empleado
   Empleado "1" -- "0..*" Empleado : supervisa
   @enduml

**Asociación N-aria** — Relación entre tres o más objetos.

Ejemplos:

- **Proyecto, Empleado y Rol:** un proyecto puede involucrar a
  múltiples empleados, cada uno con un rol específico en el
  proyecto.
- **Pedido, Producto y Cantidad:** un pedido puede incluir varios
  productos, y cada producto puede tener una cantidad específica
  en ese pedido.
