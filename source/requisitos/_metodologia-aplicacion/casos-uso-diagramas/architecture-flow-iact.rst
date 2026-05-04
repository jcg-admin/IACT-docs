15.4 Architecture flow IACT
---------------------------

Vista navegacional condensada — desde la entrada
hasta la salida del sistema, mostrando los
clusters de UCs accesibles:

.. uml::

   @startuml
   title IACT — Architecture flow (vista navegacional)

   start

   :Login;
   note right
     UC_AUTH_01
     LDAP + sesion unica (CNST_002)
   end note

   if (autenticado?) then ([si])
     :Panel del supervisor;
     note right
       Punto de entrada autenticado.
       Acceso filtrado por RBAC
       (CNST_030 SoD).
     end note

     fork
       :Consultar dashboards
       (UC_RPT_*);
     fork again
       :Reconocer alertas
       (UC_ALR_*);
     fork again
       :Monitorear ETL
       (UC_PIP_*);
     fork again
       :Consultar auditoria
       (UC_AUD_*);
     fork again
       :Gestionar RBAC
       (UC_PERM_*);
     fork again
       :Consultar buzon
       (UC_LOG_*);
     end fork

     :Logout;
     note right
       UC_AUTH_02 o
       caducidad CNST_002
     end note
   else ([no])
     :Registrar intento fallido;
     note right
       Audit (CNST_025) +
       throttling (CNST_011)
     end note
   endif

   stop
   @enduml

Lectura del flujo
~~~~~~~~~~~~~~~~~

- **Una sola entrada** — Login. No hay registro
  público porque los usuarios provienen del
  LDAP corporativo (decisión arquitectónica).
- **Bifurcación tras autenticarse** — el
  supervisor puede operar cualquiera de los seis
  clusters principales. Cada nodo del fork
  agrupa varios UCs del catálogo.
- **Audit transversal** — cualquier rama puede
  generar eventos en ``audit_log``; está
  implícito por CNST_025 y no aparece como nodo
  separado.
- **Salida única** — Logout o caducidad
  automática.
