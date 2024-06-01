#funcion para leer un archivo de texto linea por linea y que separe las oraciones por espacios 

def lector_texto(archivo):
    with open(archivo, 'r') as file:
        data = file.readlines()
        for line in data:
            line = line.split()
