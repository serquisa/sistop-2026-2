import sys

def verificar_salida(lectura):
	if lectura == "":
		print("Saliendo de minishell")
		return True

def main():
	while True:
		try: 
			sys.stdout.write("minishel>>")
			sys.stdout.flush()
			
			lectura = sys.stdin.readline()
			
			if verificar_salida:
				break
		except Exception as e:
			print(f"minishell: error inesperado: {e}", file=sys.stderr)
main()
