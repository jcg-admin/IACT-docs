2. Singleton — ConfiguracionAlertas
====================================

**Problema.** ``alr_app`` necesita umbrales de alerta
consistentes en toda la aplicación (BR_016/017/018).

**Solución.** Una única instancia de
``ConfiguracionAlertas`` cargada al arrancar el WSGI.

.. uml::

   @startuml
   class ConfiguracionAlertas {
     - {static} _instancia : ConfiguracionAlertas
     - umbrales : dict
     - __init__()
     + {static} obtener() : ConfiguracionAlertas
     + umbral(metrica : str) : float
   }
   ConfiguracionAlertas --> ConfiguracionAlertas : _instancia
   @enduml

.. note::

 La implementacion del patron sigue la estructura mostrada en el
 diagrama UML. Los detalles de codigo van en el repositorio fuente,
 no en la especificacion.

Notas IACT:

- En Django, ``django.conf.settings`` ya es un singleton de
  facto. Usar este patrón solo para configuración **mutable
  en runtime** (recargable sin redeploy).
- Cualquier mutación debe quedar en ``audit_log``
  (CNST_025).
