# El elevador
# Gonzalez Falcon Luis Adrian & Lopez Morales Fernando Samuel

import threading
import time
import random
# Elevador es un hilo
# Usuario otro hilo
# 5 pisos

# mulitplex para limitar la cantidad de presonas dentro del elevador
# cola para poder emparejar al elevador y al usuario

candado = threading.Lock()
capacidadElevador = threading.Semaphore(5)
dentro = []

def entrarElevador(num):
   capacidadElevador.acquire()



for i in range(10):
    t = threading.Thread(target=entrarElevador, args=[i]).start();  
