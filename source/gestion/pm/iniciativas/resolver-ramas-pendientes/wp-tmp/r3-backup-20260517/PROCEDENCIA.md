Procedencia: rama integration/backup-20260517_021658 (R3)
Commit unico: bc112cfd "portar delta de backup 20260517_021658
(21 nuevos + 92 modificados)"
Estrategia: copia masiva de TODO lo cambiado para preservar
contenido y poder borrar la rama sin perder trabajo. El analisis
de que integrar se hace despues sobre estos archivos.

Alcance copiado (79 archivos, hash verificado identico a R3):
- 76 archivos source/ (8 nuevos + 68 que difieren de develop;
  R3 mas reciente en todos los que difieren, 17-mayo)
- 3 no-source que difieren: .gitignore, pyproject.toml, uv.lock

NO copiados (decision/correcto):
- 34 archivos identicos a develop (mismo hash, ruido)
- ROADMAP.md (identico a develop, no cambiado)

IMPORTANTE — no-source son SOLO preservacion para analisis:
.gitignore, pyproject.toml y uv.lock NO son candidatos a
integracion. develop ya los tiene en estado correcto y mas
reciente por trabajo de esta sesion (PR #23 bumps anyio/ruamel
regenero uv.lock/pyproject; B-01 toco pyproject). Integrar las
versiones de R3 (backup 17-mayo) seria RETROCESO. Se conservan
aqui unicamente para trazabilidad del backup, no para portar.

Contenido source/ destacado (candidato real a analisis de
integracion, modelo verificado VIGENTE v5.4.0):
- arquitectura-tecnica/rbac/modelo-rbac-iact.rst (2897 lineas,
  :version: 5.4.0 M2M, NUEVO ausente en develop)
- normativa/restricciones/cnst-030-...-sod.rst (334, NUEVO)
- 6 diagramas-uml.rst de casos-uso access/permissions (NUEVOS)
- 68 archivos donde R3 es mas reciente que develop

wp-tmp/ es pasajero: git log y documentos de la iniciativa, no
develop ni build. Integracion real = fase posterior con su
analisis de sustancia (sustantivo vs trivial por archivo).
