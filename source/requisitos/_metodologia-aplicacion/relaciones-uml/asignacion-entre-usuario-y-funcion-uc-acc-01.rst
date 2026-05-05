9.2 Asignacion entre Usuario y Funcion (UC_ACC_01)
--------------------------------------------------

.. uml::

   @startuml

   class Usuario
   class Funcion

   class Asignacion {
     - fecha_inicio : DateTime
     - fecha_fin : DateTime
     - aprobador : Usuario
     - es_temporal : Boolean
     - justificacion : String
     + revocar()
     + extender(nueva_fecha)
   }

   Usuario "0..*" -- "0..*" Funcion : asignado
   (Usuario, Funcion) .. Asignacion
   note right of Asignacion
     Cuando es_temporal = true,
     CNST_031 obliga
     fecha_fin ≤ fecha_inicio + 6
     meses y justificación con
     ≥ 20 caracteres.
   end note
   @enduml
