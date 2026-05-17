.. _uc-usr-05-parte-09:

==========================================
Parte 9 — Requisitos no funcionales
==========================================

9.1 Performance
================

P50
  Latencia P50 de la transaccion completa ≤ 250 ms para
  un User con hasta 5 Sessions ACTIVE y 5 tokens vivos.

P99
  Latencia P99 ≤ 800 ms, incluyendo escritura del
  AuditEvent.

Throughput
  El endpoint soporta hasta 10 RPS sostenidos sin
  degradacion (operacion poco frecuente — admin manual).

9.2 Disponibilidad
===================

UC_USR_05 NO es operacion critica para disponibilidad
del sistema. Si el endpoint esta caido, el bloqueo manual
no puede ejecutarse pero BR-015 (automatico) sigue
funcionando para casos de credencial comprometida.

9.3 Concurrencia
=================

Locking
  La transaccion adquiere row-lock en ``User`` para
  prevenir actualizaciones concurrentes.

Idempotencia
  Si dos admins simultaneamente bloquean al mismo User,
  el segundo recibe ``200 OK`` con ``already_blocked =
  true`` (flujo alterno A1). NO hay lock explicito mas
  alla del de fila.

9.4 Auditabilidad
==================

Inmutabilidad
  AuditEvent ``USER_BLOCKED`` es immutable per CNST-025.

Sin PII
  payload del AuditEvent NO contiene email, full_name,
  o cualquier identificador personal del User. CNST-026.

Trazabilidad reversa
  UC_USR_06 (desbloqueo) emite AuditEvent
  ``USER_UNBLOCKED`` con referencia al ``USER_BLOCKED``
  original (atributo ``original_block_event_id``).

9.5 Seguridad
==============

Authn
  Endpoint requiere JWT vigente.

Authz
  AuthorizationGuard verifica funcion ``block_users``
  activa.

Rate-limiting
  No aplica especificamente — operacion infrecuente; el
  rate-limiter generico de la API es suficiente.

Audit failure
  Si el AuditEvent NO se persiste (paso 6 sub-step 4),
  la transaccion completa hace rollback. Sin AuditEvent
  no hay bloqueo.

9.6 Localizacion
=================

El campo ``reason`` es texto libre del admin. El sistema
NO traduce ni valida idioma — preserva el texto tal cual
se ingreso.

Los mensajes de error (``ACCOUNT_BLOCKED``,
``PERMISSION_DENIED``, etc.) son codigos i18n estables;
la UI los traduce a presentacion local.
