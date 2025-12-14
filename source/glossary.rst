.. _glossary:

########
Glosario
########

.. glossary::
   :sorted:

   **access path**
      Un **access path** es la forma en que una consulta recupera filas a partir de un conjunto de filas devueltas por un paso de un **execution plan** (row source). A continuación se muestra una lista de posibles **access paths** (consulta la lista completa en la documentación oficial de Oracle):

      * **full table scan**
      * **table access by ROWID**
      * **sample table scan**
      * **index unique scan**
      * **index range scan**
      * **index full scan**
      * **index fast full scan**
      * **index skip scan**
      * **index join scan**
      * **bitmap index single value**
      * **bitmap index range scan**
      * **bitmap merge**
      * **bitmap index range scan**
      * **cluster scan**
      * **hash scan**

   **anonymous block**
      La unidad básica de un programa fuente **PL/SQL** es un **block**. Cada bloque debe contener al menos una sentencia ejecutable. Las secciones de declaración y manejo de excepciones son opcionales. Cuando un bloque no tiene nombre, se conoce como **anonymous block**. Los **anonymous blocks** se compilan cada vez que se cargan en memoria, típicamente mediante las siguientes fases:

      1. Revisión de sintaxis: verificación de la sintaxis **PL/SQL** y generación del **parse tree**.
      2. Revisión semántica: verificación de tipos y procesamiento del **parse tree**.
      3. Generación de código.

   **CGA**
      La **Call Global Area (CGA)** es una parte de la :term:`PGA`. Existe únicamente durante la duración de una llamada, es decir, mientras el proceso está en ejecución. Los **anonymous blocks** y los datos de módulos de nivel superior (por ejemplo, funciones y procedimientos) residen en la **CGA**. Los datos a nivel de paquete se almacenan en la :term:`UGA`.

   **context switch**
      Cada vez que el control se pasa del **SQL engine** al **PL/SQL engine** o en sentido inverso, se produce un **context switch**. El código procedimental se ejecuta en el **PL/SQL engine**, mientras que todas las sentencias **SQL** se ejecutan en el **SQL statement executor** o **SQL engine**. Cuando se intercambia el control de procesamiento, **Oracle** debe guardar el estado del proceso del hilo en ejecución antes de transferir el control a otro hilo o proceso. La sobrecarga de los **context switches** puede ser significativa, especialmente al iterar sobre grandes volúmenes de datos.

      Los **bulk binds** (por ejemplo, ``BULK COLLECT INTO``) pueden utilizarse para reducir el número de **context switches** al recorrer datos en bucles.

      Un error común es usar ``SELECT ... INTO ... FROM dual`` en una asignación **PL/SQL** para obtener un valor que podría obtenerse directamente en **PL/SQL**. Ese patrón provoca dos **context switches**: de **PL/SQL** a **SQL** y de regreso de **SQL** a **PL/SQL**.

   **instance**
      Una **database instance**, o simplemente **instance**, es la combinación de la :term:`SGA` y los procesos en segundo plano (**background processes**). Una **instance** está asociada exactamente a una base de datos. **Oracle** reserva una región de memoria y arranca los **background processes** cuando se inicia una **instance**.

   **IUD statements**
      Un subconjunto de sentencias **DML** en **SQL**. **IUD** es el acrónimo de ``INSERT``, ``UPDATE`` y ``DELETE``. La sentencia ``MERGE`` es una combinación de estas y por ello también se considera incluida, aunque no aparezca explícitamente en el acrónimo.

      Es importante notar que algunas personas (por ejemplo, **Steven Feuerstein**) no consideran ``SELECT`` como parte del **DML**, probablemente porque la letra **M** se interpreta como “modificación” y un ``SELECT`` no modifica datos. Esto contrasta con la definición generalmente aceptada en la documentación de **Oracle**. No se recomienda este uso alternativo de la terminología, ya que puede generar confusión. Las sentencias ``SELECT`` suelen denominarse simplemente **queries**.

   **latch**
      Un **latch** es un dispositivo de exclusión mutua (**mutex**). Un proceso que necesita acceso a una estructura de datos protegida por un **latch** intenta acceder a ella repetidamente (similar a un **spinlock**) hasta conseguir la información requerida.

      En comparación con los :term:`lock` s, los **latches** son mecanismos de **serialization** ligeros. Los **latches** son comunes en estructuras en memoria, como las estructuras de datos de la :term:`SGA`.

      Un problema común relacionado con la contención de **shared pool latches** es el **hard parsing**. Una forma de reducir la contención en los **latches** del **shared pool** es eliminar literales mediante el uso de **bind variables** siempre que sea posible, o configurar el parámetro ``CURSOR_SHARING`` de forma adecuada (se recomienda preferentemente el uso de **bind variables**).

   **lock**
      Un **lock** es también un dispositivo de exclusión mutua (**mutex**). Un proceso se pone en cola (**enqueue**) hasta que su solicitud puede ser atendida en orden de llegada (**first-come-first-serve**, FCFS). En comparación con los :term:`latch` es, los **locks** son mecanismos de sincronización de mayor peso. Un ejemplo típico son los **row-level locks**.

   **PGA**
      La **Program Global Area (PGA)** es una región de memoria no compartida que contiene datos e información de control para un proceso de servidor. La **PGA** se crea cuando se inicia el proceso de servidor. La **PGA** está compuesta por las siguientes áreas, que pueden o no existir en todos los casos:

      * **SQL work area(s)**:
        * **sort area**
        * **hash area**
        * **bitmap merge area**
      * **session memory**
      * **private SQL area**:
        * **persistent area**
        * **runtime area**

      Una **SQL work area** se usa para operaciones que consumen mucha memoria.

      El **private SQL area** es la combinación de la **persistent area** y la **runtime area**. La **runtime area** contiene información sobre el estado de ejecución de la consulta, mientras que la **persistent area** almacena los valores de las **bind variables**. Un **cursor** es el nombre de un **private SQL area** específico, razón por la cual a veces ambos términos se usan de forma intercambiable.

      En conexiones **shared server**, la **session memory** es compartida en lugar de privada. De forma similar, la **persistent area** se ubica en la :term:`SGA` para conexiones **shared server**.

   **PL/SQL optimizer**
      Desde **Oracle Database 10g**, el compilador **PL/SQL** puede optimizar código **PL/SQL** antes de traducirlo a código del sistema. El parámetro de optimización ``PLSQL_OPTIMIZER_LEVEL`` (valores 0, 1, 2 —predeterminado— o 3) determina el nivel de optimización. Cuanto mayor es el valor, más tiempo lleva compilar los objetos, aunque normalmente la diferencia es mínima y compensa el tiempo adicional por las mejoras de rendimiento.

   **processes**
      Existen dos tipos de **processes** en **Oracle**: **Oracle processes** y **client processes**. Un **client process** ejecuta código de la aplicación o código de **Oracle**. Los **Oracle processes** se dividen en tres tipos: **server processes**, **background processes** y **slave processes**.

      Un **server process** es aquel que se comunica con un **client process** y con la base de datos para atender una solicitud. Entre sus responsabilidades se incluyen:

      * Analizar y ejecutar sentencias **SQL**.
      * Ejecutar código **PL/SQL**.
      * Leer bloques de datos desde los **data files** hacia el **buffer cache**.
      * Devolver resultados.

      Los **server processes** pueden ser dedicados (**dedicated**) o compartidos (**shared**). Cuando una conexión de cliente está asociada a un único **server process**, se habla de una conexión **dedicated server**.

      En conexiones **shared server**, los clientes se conectan a un **dispatcher process** en lugar de hacerlo directamente a un **server process**. El **dispatcher** recibe las solicitudes y las coloca en la **request queue** dentro de la **large pool** (ver :term:`SGA`). Las solicitudes se atienden en orden **FIFO** (first-in-first-out). Después, el **dispatcher** coloca los resultados en la **response queue**.

      Los **background processes** se crean automáticamente cuando se inicia una :term:`instance`. Se encargan, por ejemplo, de tareas de mantenimiento y de recuperación (**redo**). Entre los **background processes** obligatorios se encuentran:

      * **PMON**: **process monitor process**.
      * **LREG**: **listener registration process**.
      * **SMON**: **system monitor process**.
      * **DBW**: **database writer process**.
      * **LGWR**: **log writer process**.
      * **CKPT**: **checkpoint process**.
      * **MMON/MMNL**: **manageability monitor process**.
      * **RECO**: **recoverer process**.

      Los **slave processes** son **background processes** que ejecutan acciones en nombre de otros procesos. Los **parallel execution (PX) server processes** son un ejemplo clásico de **slave processes**.

   **PVM**
      La **PL/SQL virtual machine (PVM)** es un componente de la base de datos que ejecuta el **bytecode** de un programa **PL/SQL**. Dentro de la **VM**, el **bytecode** se traduce a **machine code** que se ejecuta en la base de datos. El **bytecode** intermedio (también conocido como **MCode**) se almacena en el **data dictionary** y se interpreta en tiempo de ejecución.

      La :term:`Native compilation <PVM>` es un mecanismo distinto. Al usar **PL/SQL native compilation**, el código **PL/SQL** se compila a **machine-native code**, evitando la interpretación en tiempo de ejecución. La traducción del código **PL/SQL** a una biblioteca compartida en **C** requiere un compilador **C**; estas bibliotecas compartidas no son portables.

   **SARGable**
      Acrónimo de **Search ARGumentable**. Se refiere a predicados o condiciones de búsqueda que pueden aprovechar un **index** de forma eficiente porque la condición está formulada de manera que el optimizador puede aplicar el **index** directamente sobre los datos.

   **SGA**
      La **System Global Area (SGA)** contiene datos e información de control. Está compuesta por el **shared pool**, el **database buffer cache**, el **redo log buffer**, el **Java pool**, el **streams pool**, el **in-memory column store**, la **fixed SGA** y, de forma opcional, la **large pool**. La **SGA** es compartida por todos los **server processes** y **background processes**.

      La llamada **large pool** es un área opcional dentro de la **SGA** destinada a asignaciones de memoria más grandes de lo que resulta apropiado para el **shared pool**, y se utiliza para evitar la fragmentación de memoria.

   **shared pool**
      El **shared pool** es un área dentro de la :term:`SGA` que incluye el **library cache**, el **data dictionary cache**, el **server result cache** y el **reserved pool**. El **library cache** contiene el **shared SQL area** y, en el caso de una conexión **shared server**, también los **private SQL areas**.

   **SQL compiler**
      El **SQL compiler** está formado por el **parser**, el **optimizer** y el **row source generator**. Su función es “compilar sentencias **SQL** en un **shared cursor**”, donde un **cursor** es simplemente un identificador (**handle**) o nombre de un **private SQL area** dentro de la :term:`PGA`. Un **private SQL area** contiene una sentencia ya analizada (**parsed statement**) y otra información, como los valores de las **bind variables**, el estado de ejecución de la consulta y las áreas de trabajo de ejecución de la consulta (**query execution work areas**).

   **UGA**
      La **User Global Area (UGA)** es la memoria asociada a cada sesión de usuario. Los datos a nivel de paquete se almacenan en la **UGA**, por lo que su tamaño crece linealmente con cada nueva sesión.

      Cuando el estado de un paquete es **serially reusable** (``PRAGMA SERIALLY_REUSABLE``), los datos del paquete se almacenan en la :term:`SGA` y persisten durante la vida de la llamada al servidor (**server call**). Los estados de paquetes no reutilizables permanecen durante toda la vida de la sesión.

   **VPD**
      Una **virtual private database (VPD)** permite crear **security policies** que habilitan o deshabilitan el acceso a columnas o filas específicas. Es un sistema de **fine-grained security control** sobre objetos individuales y los datos que contienen, en lugar de operar únicamente al nivel de esquema (**user**).