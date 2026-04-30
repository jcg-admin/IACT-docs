.. meta::
 :artefacto: METODOLOGIA_PATRONES_DISENO
 :tipo: Guia-Metodologica
 :dominio: requisitos
 :subdominio: _metodologia-aplicacion
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-04-30
 :ultimo_cambio: 2026-04-30
 :autor: NestorMonroy
 :clasificacion: Interno

==========================================================
Patrones de diseño aplicados a IACT (GoF + Django/Python)
==========================================================

Propósito
=========

Catálogo de patrones del *Gang of Four* aplicados al stack
IACT (Django + Python + MySQL + Redis). Cada patrón se
presenta con: problema, solución, diagrama UML PlantUML,
implementación Python alineada al dominio (UC_*, BR_*,
CNST_*).

No se introducen ejemplos genéricos (ecommerce, Stripe,
PayPal). Toda implementación debe poder caer en un módulo
``services.py`` de una de las apps Django de IACT (ver H12).

Marco metodológico
==================

- Skill principal: ``rm-specification``
- Skill complementario: ``rm-analysis``
- Lenguaje: Python (Django apps de IACT).
- Diagramas: PlantUML class diagrams (no Mermaid).
- Política: cualquier patrón aplicado debe respetar
  ADR_DEVOPS_001 (sin librerías externas que rompan el
  stack canónico) y los CNST_* del proyecto.

1. Mapa de patrones útiles en IACT
==================================

.. list-table::
 :widths: 22 28 50
 :header-rows: 1

 * - Categoría
   - Patrón
   - Uso típico en IACT
 * - Creacional
   - Singleton
   - Acceso a configuración runtime (umbrales de alerta).
 * - Creacional
   - Factory
   - Construcción de reportes según tipo (UC_RPT_*).
 * - Creacional
   - Builder
   - Configuración de exportaciones (UC_RPT_04).
 * - Estructural
   - Adapter
   - Mapear ``ldap-corporativo`` → ``User`` interno.
 * - Estructural
   - Facade
   - Orquestar export end-to-end (UC_RPT_04).
 * - Estructural
   - Decorator
   - Validar permiso/throttling antes de ejecutar.
 * - Comportamiento
   - Observer
   - ``audit_log`` reaccionando a eventos (CNST_025).
 * - Comportamiento
   - Strategy
   - Formato de export (CSV/XLSX/JSON).
 * - Comportamiento
   - State
   - Ciclo de vida de ``Sesion`` y ``AlertaCritica`` (H8).

Patrones que **no** se usan en IACT por restricciones del
proyecto: Prototype (no se clonan entidades de auditoría),
Flyweight (volumen de objetos no lo justifica), Interpreter
(reglas de alerta se modelan con Strategy + State, no DSL).

2. Singleton — ConfiguracionAlertas
====================================

**Problema.** ``alr_app`` necesita umbrales de alerta
consistentes en toda la aplicación (BR_016/017/018).

**Solución.** Una única instancia de
``ConfiguracionAlertas`` cargada al arrancar el WSGI.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class ConfiguracionAlertas {
     - {static} _instancia : ConfiguracionAlertas
     - umbrales : dict
     - __init__()
     + {static} obtener() : ConfiguracionAlertas
     + umbral(metrica : str) : float
   }
   ConfiguracionAlertas --> ConfiguracionAlertas : _instancia
   @enduml

.. code-block:: python

   class ConfiguracionAlertas:
       _instancia = None

       def __new__(cls):
           if cls._instancia is None:
               cls._instancia = super().__new__(cls)
               cls._instancia._cargar()
           return cls._instancia

       def _cargar(self):
           # Cargar umbrales BR_016/017/018 desde DB o settings
           self.umbrales = {"abandono": 0.10, "ttr_seg": 30}

       def umbral(self, metrica):
           return self.umbrales[metrica]

Notas IACT:

- En Django, ``django.conf.settings`` ya es un singleton de
  facto. Usar este patrón solo para configuración **mutable
  en runtime** (recargable sin redeploy).
- Cualquier mutación debe quedar en ``audit_log``
  (CNST_025).

3. Factory — ReporteFactory
===========================

**Problema.** UC_RPT_* abarca varios tipos (volumen,
abandono, SoD compliance). Cada tipo tiene su propio
agregador, pero comparte la interfaz ``IReporte``.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   interface IReporte {
     + generar() : Resultado
   }
   class ReporteVolumen
   class ReporteAbandono
   class ReporteSoDCompliance
   class ReporteFactory {
     + {static} crear(tipo : str, params) : IReporte
   }
   IReporte <|.. ReporteVolumen
   IReporte <|.. ReporteAbandono
   IReporte <|.. ReporteSoDCompliance
   ReporteFactory ..> IReporte : crea
   @enduml

.. code-block:: python

   class ReporteFactory:
       _registro = {}

       @classmethod
       def registrar(cls, tipo, clase):
           cls._registro[tipo] = clase

       @classmethod
       def crear(cls, tipo, params):
           if tipo not in cls._registro:
               raise ValueError(f"Tipo de reporte desconocido: {tipo}")
           return cls._registro[tipo](params)

   ReporteFactory.registrar("volumen", ReporteVolumen)
   ReporteFactory.registrar("abandono", ReporteAbandono)
   ReporteFactory.registrar("sod", ReporteSoDCompliance)

4. Builder — ConfiguracionExport
================================

**Problema.** UC_RPT_04 (exportar) tiene muchos parámetros
opcionales: rango (CNST_031, máximo 6 meses), formato,
incluir agregaciones, destinatarios del buzón interno
(CNST_001).

.. code-block:: python

   class ConfiguracionExport:
       def __init__(self, reporte_id):
           self.reporte_id = reporte_id
           self.rango = None
           self.formato = "csv"
           self.incluir_agregados = False
           self.destinatarios = []

   class ConfiguracionExportBuilder:
       def __init__(self, reporte_id):
           self._cfg = ConfiguracionExport(reporte_id)

       def rango(self, desde, hasta):
           if (hasta - desde).days > 183:  # CNST_031
               raise ValueError("rango supera 6 meses (CNST_031)")
           self._cfg.rango = (desde, hasta)
           return self

       def formato(self, fmt):
           if fmt not in ("csv", "xlsx", "json"):
               raise ValueError(f"formato no soportado: {fmt}")
           self._cfg.formato = fmt
           return self

       def con_agregados(self):
           self._cfg.incluir_agregados = True
           return self

       def destinatario_buzon(self, user_id):
           self._cfg.destinatarios.append(user_id)
           return self

       def build(self):
           if self._cfg.rango is None:
               raise ValueError("rango es obligatorio")
           if not self._cfg.destinatarios:
               raise ValueError("al menos un destinatario CNST_001")
           return self._cfg

5. Adapter — LDAPUserAdapter
============================

**Problema.** ``auth_app`` consulta ``ldap-corporativo`` que
expone atributos LDAP estándar (``cn``, ``mail``,
``memberOf``); el dominio interno usa ``User`` con
``username``, ``email``, ``grupos[]``.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class LDAPEntry {
     + cn : str
     + mail : str
     + memberOf : list
   }
   class User {
     + username : str
     + email : str
     + grupos : list
   }
   class LDAPUserAdapter {
     - entry : LDAPEntry
     + a_user() : User
   }
   LDAPUserAdapter --> LDAPEntry
   LDAPUserAdapter ..> User : produce
   @enduml

.. code-block:: python

   class LDAPUserAdapter:
       def __init__(self, ldap_entry):
           self.entry = ldap_entry

       def a_user(self):
           return User(
               username=self.entry.cn,
               email=self.entry.mail,
               grupos=[g.split(",")[0].split("=")[1]
                       for g in self.entry.memberOf],
           )

Solo cambia el adapter si LDAP cambia de schema; el resto de
``auth_app`` permanece estable.

6. Facade — ExportarReporteFacade (UC_RPT_04)
==============================================

**Problema.** UC_RPT_04 toca ``perm_app``, ``rpt_app``,
``log_app`` y ``aud_app``. Sin facade, los callers tendrían
que conocer todas las dependencias.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   class ExportarReporteFacade {
     - perm
     - rpt
     - log
     - aud
     + ejecutar(user, cfg) : ResultadoExport
   }
   ExportarReporteFacade --> perm_app
   ExportarReporteFacade --> rpt_app
   ExportarReporteFacade --> log_app
   ExportarReporteFacade --> aud_app
   @enduml

.. code-block:: python

   class ExportarReporteFacade:
       def __init__(self, perm, rpt, log, aud):
           self.perm = perm
           self.rpt = rpt
           self.log = log
           self.aud = aud

       def ejecutar(self, user, cfg):
           if not self.perm.verificar(user, "exportar_reporte"):
               self.aud.registrar(user, "export_denegado", cfg)
               raise PermisoDenegado()
           if not self.rpt.cuota_disponible(user):  # CNST_020
               raise CuotaAgotada()
           tarea_id = self.rpt.encolar_export(cfg)  # CNST_019 async
           self.log.notificar_buzon(cfg.destinatarios,
                                    f"export {tarea_id} encolado")
           self.aud.registrar(user, "export_iniciado",
                              {"tarea": tarea_id})
           return tarea_id

7. Decorator — @requiere_permiso
=================================

**Problema.** Toda vista de IACT debe validar permiso y SoD
(CNST_030) antes de ejecutar lógica de negocio.

.. code-block:: python

   from functools import wraps

   def requiere_permiso(funcion_id):
       def deco(view):
           @wraps(view)
           def wrapper(request, *args, **kwargs):
               if not perm_app.verificar(request.user, funcion_id):
                   aud_app.registrar(request.user,
                                     "acceso_denegado",
                                     {"funcion": funcion_id})
                   return HttpResponseForbidden()
               return view(request, *args, **kwargs)
           return wrapper
       return deco

   @requiere_permiso("exportar_reporte")
   def vista_exportar(request):
       ...

Variantes IACT:

- ``@requiere_sod(rol_a, rol_b)`` para CNST_030.
- ``@throttle(5, "5min")`` para CNST_011.

Cada decorator es transversal y registra en ``aud_app`` —
nunca silencia un denegado.

8. Observer — AuditLog como observer de eventos
================================================

**Problema.** CNST_025 exige audit immutable y completo. En
lugar de que cada UC llame ``aud_app.registrar`` por
duplicado, los eventos de dominio se publican y
``audit_log`` se suscribe.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   interface Observer {
     + notificar(evento)
   }
   class Bus {
     - observers : list
     + suscribir(o : Observer)
     + publicar(evento)
   }
   class AuditObserver {
     + notificar(evento)
   }
   class MetricasObserver {
     + notificar(evento)
   }
   Observer <|.. AuditObserver
   Observer <|.. MetricasObserver
   Bus --> Observer
   @enduml

.. code-block:: python

   class Bus:
       _instance = None
       def __new__(cls):
           if cls._instance is None:
               cls._instance = super().__new__(cls)
               cls._instance.observers = []
           return cls._instance
       def suscribir(self, observer):
           self.observers.append(observer)
       def publicar(self, evento):
           for o in self.observers:
               o.notificar(evento)

   class AuditObserver:
       def notificar(self, evento):
           AuditLog.objects.create(**evento.to_dict())

   bus = Bus()
   bus.suscribir(AuditObserver())

Regla IACT: ``AuditObserver`` no se puede desuscribir en
runtime — eso violaría CNST_025.

9. Strategy — formato de exportación
=====================================

**Problema.** UC_RPT_04 puede entregar CSV, XLSX o JSON. El
algoritmo de serialización cambia, el resto del flujo no.

.. uml::

   @startuml
   !include ../../_static/plantuml-styles.puml
   interface FormatoExport {
     + serializar(datos) : bytes
   }
   class CSVExport
   class XLSXExport
   class JSONExport
   FormatoExport <|.. CSVExport
   FormatoExport <|.. XLSXExport
   FormatoExport <|.. JSONExport
   class ExportadorReporte {
     - formato : FormatoExport
     + ejecutar(datos)
   }
   ExportadorReporte --> FormatoExport
   @enduml

.. code-block:: python

   class CSVExport:
       def serializar(self, datos):
           ...
   class XLSXExport:
       def serializar(self, datos):
           ...
   class ExportadorReporte:
       def __init__(self, formato):
           self.formato = formato
       def ejecutar(self, datos):
           return self.formato.serializar(datos)

Agregar un nuevo formato no toca ``ExportadorReporte``,
``rpt_app`` ni el facade — solo se registra una nueva
estrategia.

10. State — sesión y alerta crítica
====================================

Documentado en :doc:`diagramas-estados`. El patrón State
se materializa con clases ``EstadoSesion`` /
``EstadoAlerta`` que encapsulan las transiciones legales y
disparan eventos al ``Bus`` para que el ``AuditObserver``
los persista.

.. code-block:: python

   class EstadoAlerta:
       def reconocer(self, alerta, user): raise NotImplementedError
       def cerrar(self, alerta, user): raise NotImplementedError

   class AlertaPublicada(EstadoAlerta):
       def reconocer(self, alerta, user):
           alerta.cambiar_estado(AlertaReconocida(user))
           bus.publicar(EventoReconocida(alerta, user))
       def cerrar(self, alerta, user):
           raise TransicionInvalida("publicada → cerrada no permitida")

   class AlertaReconocida(EstadoAlerta):
       def reconocer(self, alerta, user):
           raise TransicionInvalida("ya reconocida")
       def cerrar(self, alerta, user):
           alerta.cambiar_estado(AlertaCerrada(user))
           bus.publicar(EventoCerrada(alerta, user))

11. Patrones vs principios SOLID
================================

Los patrones **aplican** los principios; no son sustitutos.

.. list-table::
 :widths: 25 35 40
 :header-rows: 1

 * - Patrón
   - Principio dominante
   - Cómo se ve en IACT
 * - Singleton
   - Single Responsibility
   - Una clase posee la configuración runtime.
 * - Factory
   - Open/Closed
   - Agregar tipo de reporte sin tocar callers.
 * - Adapter
   - Open/Closed + Dependency Inversion
   - Cambiar LDAP no rompe ``auth_app``.
 * - Facade
   - Single Responsibility
   - Una clase orquesta UC_RPT_04 completo.
 * - Decorator
   - Open/Closed
   - Permisos/throttling sin modificar la vista.
 * - Observer
   - Single Responsibility
   - ``aud_app`` no se mezcla con la lógica del UC.
 * - Strategy
   - Open/Closed
   - Nuevo formato export sin tocar el flujo.

12. Cuándo no aplicar un patrón
===============================

- El patrón **agrega complejidad** y solo hay un caso. Un
  ``if`` cumple sin Strategy.
- El patrón rompe restricciones del proyecto (e.g. un
  Observer que mande email viola CNST_001).
- El patrón requiere librería externa que rompe
  ADR_DEVOPS_001.
- El patrón hace que una mutación auditable (CNST_025)
  pase por capas que pueden silenciar el evento.

Ante la duda: **no aplicar**. Documentar la decisión en un
ADR del subdominio afectado.

Trazabilidad
============

.. list-table::
 :widths: 25 75
 :header-rows: 0

 * - **Skill principal**
   - ``rm-specification``
 * - **Skill complementario**
   - ``rm-analysis``
 * - **Diagramas relacionados**
   - :doc:`relaciones-uml`,
     :doc:`agregacion-interfaces`,
     :doc:`diagramas-estados`,
     :doc:`diagramas-componentes`
 * - **Stack canónico**
   - ADR_DEVOPS_001 (Vagrant + Apache + mod_wsgi + Django
     + MySQL + Redis)
 * - **Restricciones aplicadas**
   - CNST_001 buzón interno, CNST_011 throttling,
     CNST_019/020 export async, CNST_025 audit immutable,
     CNST_030 SoD, CNST_031 rango 6 meses
 * - **Política de diagramación**
   - :doc:`/base-cognitiva/plantuml-guide/guidelines`
 * - **Teoría UML**
   - :doc:`/base-cognitiva/_uml/index`
