.. _arq-mod-006-casos-uso:

================================================
ARQ_MOD_006 — Casos de Uso y Requisitos
================================================

.. contents:: Contenido
 :local:
 :depth: 1

----

Casos de Uso Asociados
=======================

Especificaciones completas: :doc:`/requisitos/casos-uso/alerts/index`

.. list-table::
 :widths: 12 40 48
 :header-rows: 1

 * - UC ID
   - Nombre
   - Descripcion
 * - UC_036
   - Configurar_Alerta_Operativa
   - Tipo, severidad, destinatarios, frecuencia
 * - UC_037
   - Recibir_Notificacion_Buzon
   - InternalMessage generico reutilizable
 * - UC_038
   - Consultar_Bandeja_Notificaciones
   - Filtrar por severidad, tipo, estado
 * - UC_039
   - Silenciar_Posponer_Alerta
   - Snooze 1h, 8h, 24h, personalizado
 * - UC_040
   - Confirmar_Cerrar_Alerta
   - Marcar como atendida

----

Requisitos Funcionales Derivados
==================================

.. list-table::
 :widths: 12 45 20 23
 :header-rows: 1

 * - FR ID
   - Nombre
   - Deriva de
   - Descripcion
 * - FR_027
   - Crear_Configuracion_Alerta
   - UC_036
   - CRUD alertas
 * - FR_028
   - Enviar_Notificacion_Interna
   - UC_037
   - Via InternalMessage
 * - FR_029
   - Listar_Notificaciones
   - UC_038
   - Con filtros
 * - FR_030
   - Aplicar_Snooze_Alerta
   - UC_039
   - Tiempos predefinidos
