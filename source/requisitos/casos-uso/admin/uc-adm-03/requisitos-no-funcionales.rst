.. _uc-adm-03-parte-06:

==========================================
Parte 6 — Requisitos no funcionales
==========================================

- Performance: operacion ≤ 300 ms;
  recalculo effective_set ≤ 5 s (puede ser
  asincrono para AGR con mas de 100 usuarios).
- Confiabilidad: ≥ 99.9%; afecta effective_set
  de todos los usuarios del AGR.
- Seguridad: solo AGR-009. No accesible por
  operadores ni administradores funcionales.
- Auditabilidad: cada cambio de composicion
  auditado con alta criticidad (CNST-025).
- Impacto controlado: vista /impact/ disponible
  antes de confirmar cambio.
- Consistencia: SoD verificado antes de persistir
  (CNST-030).
