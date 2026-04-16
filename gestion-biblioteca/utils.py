import re
from datetime import datetime, timedelta
from colorama import Fore, Style

#re.compile pa compilar REGEX de una y no tener que repetir cosas ^: Inicio de string seguido de la letra del ID y \d{3}$: para que solo sean 3 numeros y fin del string
REGEX_ID_LIBRO = re.compile(r'^L\d{3}$')
REGEX_ID_USUARIO = re.compile(r'^U\d{3}$')
REGEX_ID_PRESTAMO = re.compile(r'^P\d{3}$')

def validar_id(id_str, tipo): #Validar el ID, por las dudas, seguro sirva para los casos de prueba
    assert tipo in ('libro', 'usuario', 'prestamo'), "Tipo de ID no válido" #Assert para chequear que sea siempre True
    
    if tipo == 'libro': #.match para que todo cumpla con el REGEX
        return REGEX_ID_LIBRO.match(id_str)
    if tipo == 'usuario':
        return REGEX_ID_USUARIO.match(id_str)
    if tipo == 'prestamo':
        return REGEX_ID_PRESTAMO.match(id_str)

def generar_nuevo_id(lista_de_dicts, prefijo):#Genera IDs incrementales
    if not lista_de_dicts:
        return f"{prefijo}{'1'.zfill(3)}" #rellenar con 0s a la izq hasta que sean 3 digitos (i.e. nada de L02 o L2 -> siempre L002)
    
    clave_id = f'ID_{"Libro" if prefijo == "L" else "Usuario" if prefijo == "U" else "Prestamo"}' #defino la clave de diccionario para libros
    numeros = list(map(lambda item: int(item[clave_id].lstrip(prefijo)), lista_de_dicts)) #lambda para sacar ID sin letra y pasar a INT
    nuevo_numero = max(numeros) + 1 #Numero mas alto + 1
    return f"{prefijo}{str(nuevo_numero).zfill(3)}"

def obtener_fecha_actual_str(): #Funcioncita pa sacar la fecha actual con datetime, el profe dijo que podiamos usar esta lib
    return datetime.now().strftime('%d/%m/%Y')

def calcular_fecha_devolucion_str(dias = 15): #Calcula la fecha de devolucion del libro haciendo una suma, tengo que descubrir como setear la cantidad de dias
    fecha_devolucion = datetime.now() + timedelta(days = dias)
    return fecha_devolucion.strftime('%d/%m/%Y') 

def imprimir_error(mensaje): #Colorama para que los errores sean siempre rojos, mensajes siempre verdes y warnings siempre amarillos
    print(f"{Fore.RED}[ERROR] {mensaje}{Style.RESET_ALL}")

def imprimir_exito(mensaje):
    print(f"{Fore.GREEN}[EXITO] {mensaje}{Style.RESET_ALL}")

def imprimir_advertencia(mensaje):
    print(f"{Fore.YELLOW}[AVISO] {mensaje}{Style.RESET_ALL}")