Política IACT — pipeline de diagramas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **No depender del build local** como
   única ruta de generación. El servidor de
   documentación se actualiza desde el pipeline.
2. **Diagramar el flujo del pipeline** antes de
   modificarlo — el flowchart se versiona
   junto con el ADR del cambio.
3. **Pipeline mínimo** — checkout, install,
   build, publish. Sin pasos accesorios que el
   stack ya cubre.
4. **Cualquier broker de CI externo** o
   herramienta adicional al stack canónico
   (GitHub Actions self-hosted, GitLab CI,
   Jenkins) requiere ADR si modifica las
   garantías del pipeline actual.
5. **Verificación**: cada deploy del sitio de
   documentación debe garantizar que **todos**
   los ``.. uml::`` rinden sin error. Un fallo
   de render bloquea el deploy.
