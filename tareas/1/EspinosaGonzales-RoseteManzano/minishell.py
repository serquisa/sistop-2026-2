
#!/usr/bin/env python3

import os
import shlex
import signal
import sys

background_pids = set()


def sigchld_handler(signum, frame):
    try:
        while True:
            pid, status = os.waitpid(-1, os.WNOHANG)

            if pid == 0:
                break

            if pid in background_pids:
                background_pids.remove(pid)

                if os.WIFEXITED(status):
                    code = os.WEXITSTATUS(status)
                    print(f"\nProceso {pid} terminó (código {code})")

                elif os.WIFSIGNALED(status):
                    sig = os.WTERMSIG(status)
                    print(f"\nProceso {pid} terminó por señal {sig}")

    except ChildProcessError:
        pass


def ignore_sigint(signum, frame):
    print()


def parse_command(line):

    try:
        args = shlex.split(line)
    except ValueError:
        print("Error al leer el comando")
        return None, False

    if not args:
        return None, False

    background = False

    if args[-1] == "&":
        background = True
        args = args[:-1]

    return args, background


def run_command(args, background):

    try:
        pid = os.fork()

    except OSError as e:
        print("No se pudo crear el proceso:", e)
        return

    if pid == 0:

        signal.signal(signal.SIGINT, signal.SIG_DFL)

        try:
            os.execvp(args[0], args)

        except FileNotFoundError:
            os.write(2, f"Comando no encontrado: {args[0]}\n".encode())

        except Exception as e:
            os.write(2, f"Error al ejecutar: {e}\n".encode())

        os._exit(1)

    else:

        if background:
            background_pids.add(pid)
            print(f"Proceso en segundo plano: {pid}")

        else:
            while True:
                try:
                    os.waitpid(pid, 0)
                    break
                except InterruptedError:
                    continue


def main():

    signal.signal(signal.SIGCHLD, sigchld_handler)
    signal.signal(signal.SIGINT, ignore_sigint)

    while True:

        try:
            line = input("minishell> ")

        except EOFError:
            print()
            break

        except KeyboardInterrupt:
            print()
            continue

        line = line.strip()

        if not line:
            continue

        if line == "exit":
            break

        args, background = parse_command(line)

        if args is None:
            continue

        run_command(args, background)


if __name__ == "__main__":

    if os.name == "nt":
        print("Este programa está pensado para Unix/Linux (usa fork).")
        sys.exit(1)

    main()
