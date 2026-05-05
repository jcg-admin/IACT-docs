9.1 Suscripcion entre Usuario y Alerta (UC_ALR_05)
--------------------------------------------------

.. uml::

   @startuml

   class Usuario
   class Alerta

   class Suscripcion {
     - fecha_inscripcion : DateTime
     - canal : Enum
     - severidad_minima : Enum
     - silenciada_hasta : DateTime
     + actualizar(canal, severidad)
     + silenciar(hasta)
   }

   Usuario "0..*" -- "0..*" Alerta : suscrito_a
   (Usuario, Alerta) .. Suscripcion
   note right of Suscripcion
     Atributos propios de la
     suscripción: fecha, canal
     (sólo buzón interno per
     CNST_001), severidad mínima
     y silenciamiento temporal.
   end note
   @enduml
