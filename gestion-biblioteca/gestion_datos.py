import json

#Paths de los archivos
RUTA_LIBROS = 'data/books.json'
RUTA_USUARIOS = 'data/users.json'
RUTA_PRESTAMOS = 'data/loans.txt'

def cargar_json(ruta): #Carga datos desde JSON
    try:
        with open(ruta, 'r', encoding = 'utf-8') as archivo: #Lee el JSON en python
            return json.load(archivo)
    except FileNotFoundError: #Devuelve una matriz si no hay archivo
        return []
    except json.JSONDecodeError: #Por si el JSON está roto o vacío
        return []

def guardar_json(ruta, datos): #Guarda lista de diccionarios en JSON
    try:
        with open(ruta, 'w', encoding = 'utf-8') as archivo: #Escribe el dump a archivo json con indent=2 para para que se lea mejor y ensure_ascii = False para que no moleste por las tildes
            json.dump(datos, archivo, indent = 2, ensure_ascii = False)
            return True
    except IOError:
        return False

def cargar_libros():
    return cargar_json(RUTA_LIBROS)

def guardar_libros(libros):
    return guardar_json(RUTA_LIBROS, libros)

def cargar_usuarios():
    return cargar_json(RUTA_USUARIOS)

def guardar_usuarios(usuarios):
    return guardar_json(RUTA_USUARIOS, usuarios)

def cargar_prestamos(): #Lee el archivo de prestamos (loans.txt) y lo convierte en matriz de diccionarios
    matriz_prestamos = []
    try:
        with open(RUTA_PRESTAMOS, 'r', encoding = 'utf-8') as archivo: #Lee el archivo txt y lo carga como lista
            lineas = archivo.readlines()
            claves = ("ID_Prestamo", "ID_Usuario", "ID_Libros", "Fecha_Prestamo", "Fecha_Devolucion_Prevista", "Fecha_Devolucion_Real", "Estado_Prestamo") #Diccionario para mappear los IDs de los prestamos
            matriz_prestamos = list(map(lambda linea: dict(zip(claves, linea.strip().split('|'))),lineas)) #Convierte lineas a diccionario con zip y map
    except FileNotFoundError:
        pass #Si no existe el archivo se devuelve una lista vacía
    return matriz_prestamos


def guardar_prestamos(matriz_prestamos):
    #Convierte la matriz de diccionarios al .txt
    lineas_a_escribir = []
    for prestamo_dict in matriz_prestamos: #Itera cada diccionario y lo convierte en string
        valores = list(map(str, prestamo_dict.values())) #Con values saco los items del diccionario en orden y con map lo paso a string
        linea = "|".join(valores) #Con el join lo pongo todo separado por pipes
        lineas_a_escribir.append(linea + "\n")
    try:
        with open(RUTA_PRESTAMOS, 'w', encoding = 'utf-8') as archivo: #Se guarda todo en el archivo
            archivo.writelines(lineas_a_escribir)
    except IOError as e:
        raise Exception(f"No se pudo guardar el archivo de prestamos: {e}") #Por si hay errores en el guardado, i.e. si el archivo ya está abierto