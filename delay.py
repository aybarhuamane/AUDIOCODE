import threading
def f():
    print("¡Hola, mundo!")
# Ejecutar la función luego de 3 segundos.
t = threading.Timer(3, f)
t.start()
print("Esto se ejecuta antes que la función f().")