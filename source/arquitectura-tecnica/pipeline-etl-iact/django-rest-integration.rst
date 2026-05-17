.. meta::
 :artefacto: AT_PIPELINE_ETL_DJANGO_REST_INTEGRATION
 :tipo: Especificacion de Implementacion — Nivel 6
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :nivel: 6
 :estado: pendiente-implementacion
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_pipeline_etl_django_rest_integration:

==============================================================
Nivel 6 — Integracion Django REST Framework
==============================================================

.. note::

 **Estado:** pendiente de implementacion. Esta seccion
 documenta el diseño de referencia. Los archivos Python
 reales se crearan en el WP de implementacion del modulo
 ``pipeline``.

Capa de integracion entre los SPs de reporte (Nivel 5) y
los endpoints REST. Componentes:

- ``settings.py`` — configuracion ``DATABASES`` dual
  (default + ivr_cliente).
- ``services/ivr_reports.py`` — invocacion de SPs via
  ``cursor.callproc()``.
- ``views/ivr_reports.py`` — viewsets DRF.
- ``urls.py`` — router con los 7 endpoints.

----

``settings.py`` — DATABASES dual
==================================

Dos bases conectadas: la base IACT (``default``) que tiene
``base_ivr_*`` y los SPs ``sp_rpt_*``, y la base del cliente
(``ivr_cliente``) que tiene ``tbl_historico_*`` y se usa solo
durante el ETL.

.. code-block:: python

   DATABASES = {
       'default': {
           'ENGINE':   'django.db.backends.mysql',
           'NAME':     env('IACT_DB_NAME'),
           'USER':     env('IACT_DB_USER'),
           'PASSWORD': env('IACT_DB_PASSWORD'),
           'HOST':     env('IACT_DB_HOST'),
           'PORT':     env('IACT_DB_PORT', default='3306'),
           'OPTIONS':  {'charset': 'utf8mb4'},
       },
       'ivr_cliente': {
           'ENGINE':   'django.db.backends.mysql',
           'NAME':     env('IVR_DB_NAME'),
           'USER':     env('IVR_DB_USER'),     # solo SELECT
           'PASSWORD': env('IVR_DB_PASSWORD'),
           'HOST':     env('IVR_DB_HOST'),
           'PORT':     env('IVR_DB_PORT', default='3306'),
           'OPTIONS':  {'charset': 'utf8mb4'},
       },
   }

   DATABASE_ROUTERS = []   # routing manual via using='ivr_cliente' donde aplica

CNST-ETL-001 obliga a credenciales de solo SELECT en
``ivr_cliente``. El ETL no escribe en esa base.

----

``services/ivr_reports.py`` — invocacion de SPs
=================================================

Capa fina que convierte ``cursor.callproc()`` en
diccionarios serializables.

.. code-block:: python

   from django.db import connection
   from typing import List, Dict


   def _call_report(sp_name: str, quarter: str) -> List[Dict]:
       """Invoca un sp_rpt_* y devuelve filas como dicts."""
       with connection.cursor() as cursor:
           cursor.callproc(sp_name, [quarter])
           columns = [col[0] for col in cursor.description]
           return [dict(zip(columns, row)) for row in cursor.fetchall()]


   def centros_transferencia(quarter: str) -> List[Dict]:
       return _call_report('sp_rpt_centros_transferencia', quarter)

   def centros_xsegmento(quarter: str) -> List[Dict]:
       return _call_report('sp_rpt_centros_xsegmento', quarter)

   def llamadas_abandonadas(quarter: str) -> List[Dict]:
       return _call_report('sp_rpt_llamadas_abandonadas', quarter)

   def menu_redirigidos(quarter: str) -> List[Dict]:
       return _call_report('sp_rpt_menu_redirigidos', quarter)

   def menu_centro(quarter: str) -> List[Dict]:
       return _call_report('sp_rpt_menu_centro', quarter)

   def menu_error(quarter: str) -> List[Dict]:
       return _call_report('sp_rpt_cMENU_ERROR', quarter)

   def clientes(quarter: str) -> List[Dict]:
       return _call_report('sp_rpt_clientes', quarter)

----

``views/ivr_reports.py`` — viewsets DRF
=========================================

Vistas de solo lectura (``list``) parametrizadas por
``quarter``. Sin paginacion — el result-set ya esta acotado
por el grain agregado.

.. code-block:: python

   from rest_framework import status
   from rest_framework.response import Response
   from rest_framework.views import APIView
   from rest_framework.permissions import IsAuthenticated

   from . import services as svc


   QUARTER_RE = r'^Q0[1-4]_\d{2}$'


   class _BaseReportView(APIView):
       permission_classes = [IsAuthenticated]
       service_fn = None       # override

       def get(self, request):
           quarter = request.query_params.get('quarter')
           if not quarter or not re.match(QUARTER_RE, quarter):
               return Response(
                   {'detail': 'quarter requerido (formato Q0N_YY)'},
                   status=status.HTTP_400_BAD_REQUEST,
               )
           data = type(self).service_fn(quarter)
           return Response({'quarter': quarter, 'rows': data})


   class CentrosTransferenciaView(_BaseReportView):
       service_fn = staticmethod(svc.centros_transferencia)

   class CentrosXSegmentoView(_BaseReportView):
       service_fn = staticmethod(svc.centros_xsegmento)

   class LlamadasAbandonadasView(_BaseReportView):
       service_fn = staticmethod(svc.llamadas_abandonadas)

   class MenuRedirigidosView(_BaseReportView):
       service_fn = staticmethod(svc.menu_redirigidos)

   class MenuCentroView(_BaseReportView):
       service_fn = staticmethod(svc.menu_centro)

   class MenuErrorView(_BaseReportView):
       service_fn = staticmethod(svc.menu_error)

   class ClientesView(_BaseReportView):
       service_fn = staticmethod(svc.clientes)

----

``urls.py`` — router
======================

.. code-block:: python

   from django.urls import path
   from . import views

   urlpatterns = [
       path('ivr/centros-transferencia/', views.CentrosTransferenciaView.as_view()),
       path('ivr/centros-xsegmento/',     views.CentrosXSegmentoView.as_view()),
       path('ivr/llamadas-abandonadas/',  views.LlamadasAbandonadasView.as_view()),
       path('ivr/menu-redirigidos/',      views.MenuRedirigidosView.as_view()),
       path('ivr/menu-centro/',           views.MenuCentroView.as_view()),
       path('ivr/menu-error/',            views.MenuErrorView.as_view()),
       path('ivr/clientes/',              views.ClientesView.as_view()),
   ]

----

Flujo end-to-end de un request
================================

.. code-block:: text

   GET /api/ivr/centros-transferencia/?quarter=Q02_26
        │
        ▼
   CentrosTransferenciaView.get()
        │
        ├── valida quarter (Q0[1-4]_YY)
        │
        ▼
   svc.centros_transferencia('Q02_26')
        │
        ▼
   cursor.callproc('sp_rpt_centros_transferencia', ['Q02_26'])
        │
        ▼
   sp_rpt_centros_transferencia
        │  SELECT ... FROM base_ivr_detalle WHERE trimestre = 'Q02_26' ...
        │  (lectura por indice — instantanea)
        │
        ▼
   result-set → dicts → Response 200 OK

Sin scan a ``tbl_historico_*`` en ningun punto del request.
El costo de scan ya fue pagado por el ETL nocturno
(``evt_etl_diario`` 02:00 AM).

----

.. seealso::

 - :doc:`report-procedures` — los 7 SPs invocados.
 - :doc:`triggers` — ``manage.py run_etl`` (Django) que
   complementa el MySQL Event.
 - :doc:`/arquitectura-tecnica/implementation-view/pipeline/index` —
   capas API/service/repository del modulo pipeline.
