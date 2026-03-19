# Tarea 1: Implementación de un intérprete de comandos mínimo (minishell)

**Autor:** Sergio Quiroz

---

## Instrucciones de compilación/ejecución

Para compilar el programa, abre una terminal en Linux dentro de la carpeta del proyecto y ejecuta:

    gcc minishell.c -o minishell

Después, para correr el programa:

    ./minishell

---

## Breve explicación del diseño

El programa está desarrollado en lenguaje C y funciona como un shell básico que permite ejecutar comandos del sistema.  
Su estructura principal se basa en un ciclo infinito (`while`) que mantiene activo el intérprete.

El funcionamiento se puede dividir en tres partes principales:

1. Lectura y separación de comandos:
   - Se muestra el prompt "minishell>".
   - Se lee la entrada del usuario usando `fgets`.
   - Se separa el comando y sus argumentos utilizando `strtok`, almacenándolos en un arreglo.

2. Creación y ejecución de procesos:
   - Se utiliza `fork()` para crear un proceso hijo.
   - En el proceso hijo se ejecuta el comando con `execvp()`.
   - El proceso padre espera a que el hijo termine usando `waitpid()`.

3. Manejo de señales:
   - Se maneja la señal `SIGCHLD` para evitar procesos zombie.
   - Se modifica el comportamiento de `SIGINT` (Ctrl+C) para que el shell no se cierre, pero los procesos hijos sí puedan terminar.

---

## Ejemplo de ejecución

    minishell> ls
    minishell.c  minishell
    minishell> ls -l
    total 24
    -rwxrwxr-x 1 serquisa serquisa 16736 Mar 18 19:37 minishell
    -rw-rw-r-- 1 serquisa serquisa  2000 Mar 18 19:37 minishell.c
    minishell> pwd
    /home/serquisa/minishell
    minishell> whoami
    serquisa
    minishell> echo hola mundo
    hola mundo
    minishell> sleep 5
    minishell> exit

---

## Dificultades encontradas y cómo se resolvieron

1. Manejo de Ctrl+C (SIGINT)

   Dificultad: Al presionar Ctrl+C, el programa terminaba completamente.
   Solución: Se configuró el proceso padre para ignorar la señal con `signal(SIGINT, SIG_IGN)` y en el hijo se restauró el comportamiento normal con `signal(SIGINT, SIG_DFL)`.

2. Procesos zombie (SIGCHLD)

   Dificultad: Los procesos hijos terminados quedaban como zombies.
   Solución: Se implementó un manejador para `SIGCHLD` utilizando `waitpid(-1, NULL, WNOHANG)` en un ciclo, lo que permite liberar los procesos sin bloquear la ejecución.

3. Separación de argumentos

   Dificultad: Al inicio los comandos con varios argumentos no funcionaban correctamente.
   Solución: Se utilizó `strtok` para dividir la entrada en tokens separados por espacios.

---

## Conclusión

Se logró implementar un minishell funcional que permite ejecutar comandos del sistema, manejar procesos y señales correctamente, cumpliendo con los requisitos solicitados en la tarea.
