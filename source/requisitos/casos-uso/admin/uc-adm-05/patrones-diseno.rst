.. meta::
 :artefacto: UC_ADM_05_PAT
 :tipo: Caso de Uso (seccion)
 :dominio: requisitos
 :subdominio: casos_uso/admin
 :estado: Borrador
 :version: 1.0.0

==============================
10. Patrones de Diseno
==============================

10.1 State Machine explicita
============================

UC_ADM_05 implementa una maquina de estados con
transiciones validadas en el servicio de aplicacion.
Patron classic State Machine + Guard Conditions.

Frente al patron "estado como string libre con UPDATE
arbitrario", UC_ADM_05 valida cada transicion contra la
tabla del flujo principal §3.1.

10.2 Default safe action + explicit opt-out (gap #3)
====================================================

El sistema **archiva por defecto** a los 90 dias en
DEPRECATED. Quien quiere preservar el item debe activar
el flag ``block_auto_archive=True`` con justificacion.

Patron classic *secure default*: el comportamiento
preferido del sistema es el default; el alternativo
requiere accion explicita y trazable.

Trade-off aceptado: un admin puede mantener un item
bloqueado para siempre, pero ahora con responsabilidad
trazable (audit log + block_reason + block_set_by).

10.3 Idempotencia del job
=========================

El job del Planificador es idempotente: ejecutar dos veces
el mismo dia produce el mismo resultado. Se logra porque
la transicion DEPRECATED → ARCHIVED solo aplica si
``status=DEPRECATED`` (re-ejecutar despues del archive
encuentra ``status=ARCHIVED`` y omite).

10.4 Capability bypass (AP-2b)
==============================

Identico a UC_ADM_04: ``manage_menu_lifecycle.is_critical=True``
fuerza verificacion DB-direct. Strong consistency en cada
transicion.

10.5 Audit log dual: transicion + flag
======================================

Las transiciones de estado y los cambios al flag generan
eventos separados en audit log. Razon: las dos cosas
tienen politicas de retencion y consulta diferentes.

- Transiciones: alta frecuencia, importantes para timeline.
- Flag: baja frecuencia, importantes para gobernanza.

10.6 Pattern reference
======================

- UC_ADM_04 — predecesor (creacion del item).
- UC_PERM_06 — mismo patron de invalidacion de cache
  post-COMMIT.
- ADR-BACK-008 — modelo MenuItem con campos de lifecycle.
- ADR-BACK-009 — politica de cache (degraded mode).
