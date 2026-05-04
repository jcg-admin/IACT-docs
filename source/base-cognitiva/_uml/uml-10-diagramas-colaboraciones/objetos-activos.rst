Objetos activos
---------------

Los **objetos activos** son elementos que tienen la capacidad de
**iniciar y controlar el flujo de interacciones por sí mismos**,
a diferencia de los **objetos pasivos** que solo responden a
mensajes.

La característica principal de un objeto activo es su capacidad
de **operar de manera independiente y tener su propio hilo de
control (thread)**. Un objeto activo controla el flujo de una
secuencia y puede enviar mensajes a objetos pasivos e
interactuar con otros objetos activos.

En una biblioteca, un bibliotecario relaciona las peticiones a
partir de un patrón, verifica la información de referencia en
una base de datos, devuelve una respuesta, asigna personas para
reabastecer los libros, entre otras cosas.

.. admonition:: Ejemplo — Biblioteca moderna

 En una biblioteca, múltiples bibliotecarios realizan tareas
 simultáneas: mientras uno procesa préstamos, otro actualiza la
 base de datos y un tercero reabastece estantes — todos
 operando concurrentemente.

 La interacción entre bibliotecarios demuestra otro aspecto
 clave de la concurrencia: la **comunicación y coordinación**
 entre procesos. Por ejemplo, deben sincronizarse para evitar
 que dos bibliotecarios intenten reubicar el mismo libro o
 atender la misma solicitud.

Al proceso de que **dos o más objetos activos hagan sus tareas
al mismo tiempo** se le conoce como **concurrencia**. Trabajar
en paralelo: por ejemplo, mientras un proceso espera datos de
la red, otro puede estar realizando cálculos.

La concurrencia también introduce desafíos como la
**sincronización de recursos compartidos** y la prevención de
**condiciones de carrera** (*race conditions*). Por esto, el
diseño de sistemas concurrentes requiere una planificación
cuidadosa.

El diagrama de colaboraciones representa a un objeto activo de
la misma manera que a cualquier otro objeto, **excepto que su
borde será grueso y más oscuro**.

.. uml::

   @startuml
   allowmixing

   object ":Bibliotecario1" as B1 <<active>>
   object ":Bibliotecario2" as B2 <<active>>
   object ":BaseDeDatos"   as BD
   object ":Estante"       as E

   B1 -> BD : "1: consultarReferencia()"
   B1 -> E  : "2: ubicarLibro()"
   B2 -> BD : "3: actualizarRegistros()"
   B1 -> B2 : "4: coordinar()"
   @enduml
