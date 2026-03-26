# Santa Claus
# Gonzalez Falcon Luis & Lopez Morales Fernando

import threading
import time
import random

NUM_ELFOS = 6
NUM_RENOS = 9


# tenemos que crear n elfos y 9 renos
#cada elfo tiene un hilo y cada reno tiene un hilo
#usamos una barrera para los elfos y una barrera para los renos

cuentaBarreraElfos = 0
cuentaBarreraRenoss = 0

def trabajoElfo(num):
    print(f"Soy el elfo {num} y estoy trabajando...")



#creando hilos ELFOS
for i in range(NUM_ELFOS):
    threading.Thread(target= trabajoElfo, args=[i]).start()
    time.sleep(1)

#creando 
