Sincronización
--------------

Un objeto sólo puede enviar un mensaje **después de que otros
mensajes han sido enviados**. Es decir, el objeto debe
"sincronizar" todos los mensajes en el orden debido.

- La sincronización establece el **orden específico** en que los
  mensajes deben ser enviados entre objetos durante una
  interacción.
- Garantiza que las operaciones se ejecuten en la secuencia
  correcta.
- Cuando un objeto necesita esperar a que se completen varios
  mensajes antes de poder enviar el suyo, esto se denomina
  **punto de sincronización** (*synchronization point*).
- Su propósito principal es prevenir condiciones de carrera y
  mantener la consistencia.
- La lista de elementos se separa mediante una **coma**, y
  finaliza con una **diagonal** (``/``).
- Se representa mediante una barra pequeña horizontal conectada
  a las flechas de los mensajes que deben completarse antes de
  proceder.

Suponga que sus objetos son personas en un corporativo
ocupados en la campaña de un nuevo producto:

1. El vicepresidente de comercialización pide al de ventas que
   cree una campaña.
2. El vicepresidente de ventas crea la campaña y la asigna al
   gerente.
3. El gerente de ventas instruye a un agente para que venda.
4. El agente hace llamadas a clientes en potencia.
5. **Después de que se completen los pasos 2 y 3** (esto es,
   el VP de ventas dio la comisión y el gerente expidió la
   directiva), un especialista en RP llama al periódico para
   colocar un anuncio.

En lugar de anteceder este mensaje con una etiqueta numérica,
se antecede con una lista de mensajes que tendrán que completarse
antes (sintaxis: ``2,3 / mensaje()``).

.. uml::

   @startuml
   allowmixing

   object ":VicepComerc"      as VC
   object ":VicepVentas"      as VV
   object ":GerenteVentas"    as GV
   object ":Vendedor"         as V
   object ":Cliente"          as C
   object ":EspecialistaRP"   as RP
   object ":Periodico"        as PER

   VC -> VV : "1: crear(campana, producto)"
   VV -> GV : "2: asignar(campana, producto)"
   GV -> V  : "3: vender(campana, producto)"
   V  -> C  : "*[clientes asignados]\n4: llamadaVentas(campana, producto)"
   RP -> PER : "2,3 / 5: colocarAnuncio(campana, producto)"
   note bottom of PER
     "2,3 / 5" indica
     sincronización: el mensaje
     5 espera a que terminen
     los mensajes 2 y 3.
   end note
   @enduml
