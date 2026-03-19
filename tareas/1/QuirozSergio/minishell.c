#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <signal.h>

#define MAX_ARGS 20

// Esta función sirve para evitar procesos zombie
void sigchld_handler(int sig) {
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

// Aquí se separa el comando en partes
void parse_input(char *input, char **args) {
    int i = 0;
    char *token = strtok(input, " \t");

    while (token != NULL && i < MAX_ARGS - 1) {
        args[i++] = token;
        token = strtok(NULL, " \t");
    }
    args[i] = NULL;
}

int main() {
    char input[256];
    char *args[MAX_ARGS];

    // Ignorar Ctrl + C en el shell
    signal(SIGINT, SIG_IGN);
    // Manejar cuando terminan procesos hijos
    signal(SIGCHLD, sigchld_handler);

    while (1) {
        printf("minishell> ");
        fflush(stdout);

        // Limpiar el buffer antes de leer
        memset(input, 0, sizeof(input));

        // Leer lo que escribe el usuario
        if (fgets(input, sizeof(input), stdin) == NULL) {
            printf("\n");
            break;
        }

        // Quitar el salto de línea
        input[strcspn(input, "\n")] = 0;

        // Si no se escribió nada, continuar
        if (strlen(input) == 0)
            continue;

        // Si se escribe exit, termina el programa
        if (strcmp(input, "exit") == 0)
            break;

        parse_input(input, args);

        // Crear proceso hijo
        pid_t pid = fork();

        if (pid == 0) {
            // En el hijo, Ctrl+C sí funciona normal
            signal(SIGINT, SIG_DFL);
            // Ejecutar el comando
            execvp(args[0], args);
            // Si falla el exec
            perror("Error");
            exit(1);
        }
        else if (pid > 0) {
            // El padre espera a que termine el hijo
            int status;
            waitpid(pid, &status, 0);
        }
        else {
            // Error al crear proceso
            perror("Error en fork");
        }
    }

    return 0;
}
