5.1 Ejemplo IACT — permiso temporal con vencimiento (UC_PERM_03)
----------------------------------------------------------------

.. uml::

   @startuml

   [*] --> Solicitado

   Solicitado --> Aprobado : aprobador_aprueba()\n[justificacion >= 20 chars]\n/ activar_permiso() + auditar()

   Solicitado --> Rechazado : aprobador_rechaza()\n/ notificar_solicitante()

   Aprobado --> Activo : / aplicar_a_usuario()

   Activo --> Vencido : timer [duracion >= 6_meses(CNST_031)]\n/ revocar_automaticamente() + auditar()

   Activo --> Revocado : aprobador_revoca()\n/ revocar_anticipadamente() + auditar()

   Vencido --> [*]
   Revocado --> [*]
   Rechazado --> [*]

   note right of Activo
     CNST_031 — vigencia
     máxima 6 meses (180 días).
     Sin auto-renovación; cada
     extensión requiere nueva
     solicitud.
   end note
   @enduml
