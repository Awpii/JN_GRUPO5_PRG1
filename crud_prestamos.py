import json
import os
from colorama import Fore, Style, init
import crud_libros as CRUD_LIBROS

init(autoreset=True)

# --- FUNCIONES AUXILIARES DE FECHAS ---
def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

def dias_del_mes(mes, año):
    if mes in [1, 3, 5, 7, 8, 10, 12]: return 31
    elif mes in [4, 6, 9, 11]: return 30
    elif mes == 2: return 29 if es_bisiesto(año) else 28
    return 0

def fecha_a_dias(fecha):
    dia, mes, año = fecha[0], fecha[1], fecha[2]
    dias = 0
    for a in range(1, año):
        dias += 366 if es_bisiesto(a) else 365
    for m in range(1, mes):
        dias += dias_del_mes(m, año)
    dias += dia
    return dias

def calcular_penalizacion(fecha_esperada, fecha_real):
    dias_esperados = fecha_a_dias(fecha_esperada)
    dias_reales = fecha_a_dias(fecha_real)
    dias_retraso = dias_reales - dias_esperados
    if dias_retraso > 0:
        return dias_retraso * 1000  # $1000 por dia de atraso
    return 0

def leer_fecha(msj):
    while True:
        try:
            cadena = input(Fore.YELLOW + msj + " (DD/MM/AAAA o 'cancelar'): " + Fore.RESET)
            if cadena.lower() == 'cancelar':
                return None
            partes = cadena.split("/")
            if len(partes) != 3:
                raise ValueError
            dia, mes, año = int(partes[0]), int(partes[1]), int(partes[2])
            if dia < 1 or dia > 31 or mes < 1 or mes > 12 or año < 1000:
                raise ValueError
            return [dia, mes, año]
        except ValueError:
            print(Fore.RED + "Formato invalido. Use numeros separados por barra (/).")

def obtener_proximo_id(nombre_archivo):
    max_id = 0
    try:
        arch = open(nombre_archivo, "rt")
        for linea in arch:
            obj = json.loads(linea)
            if obj["id_prestamo"] > max_id:
                max_id = obj["id_prestamo"]
    except FileNotFoundError:
        pass
    finally:
        try: arch.close()
        except NameError: pass
    return max_id + 1

# --- FUNCIONES DE PRESTAMOS ---
def imprimir_prestamos(arch_prestamos, arch_libros):
    print(Fore.CYAN + Style.BRIGHT + "\n--- Lista de prestamos existentes ---")
    try:
        arch = open(arch_prestamos, "rt")
        hoy = leer_fecha("Ingrese fecha actual para calcular estado")
        if not hoy:
            print(Fore.YELLOW + "Operacion cancelada.")
            return

        print("")
        for linea in arch:
            p = json.loads(linea)
            titulo_libro = CRUD_LIBROS.obtener_titulo(arch_libros, p["id_libro"])
            penalizacion = calcular_penalizacion(p["fecha_esperada"], hoy)
            
            f_p = f"{p['fecha_prestamo'][0]:02d}/{p['fecha_prestamo'][1]:02d}/{p['fecha_prestamo'][2]}"
            f_e = f"{p['fecha_esperada'][0]:02d}/{p['fecha_esperada'][1]:02d}/{p['fecha_esperada'][2]}"
            
            print(f"ID Prestamo: {p['id_prestamo']} | Solicitante: {p['solicitante']} | Libro: '{titulo_libro}'")
            print(f"   Otorgado: {f_p} | Vencimiento: {f_e}")
            if penalizacion > 0:
                print(Fore.RED + f"   ¡ATRASADO! Penalizacion acumulada: ${penalizacion}")
            else:
                print(Fore.GREEN + "   Estado: Al dia.")
            print("-")
    except FileNotFoundError:
        print(Fore.RED + "No hay prestamos activos.")
    finally:
        try: arch.close()
        except NameError: pass
    print(Fore.CYAN + "----------------------------------\n")

def crear_prestamo(arch_libros, arch_prestamos, id_prestamo_actual):
    CRUD_LIBROS.imprimir_libros(arch_libros)
    entrada = input(Fore.YELLOW + "Ingrese el ID del libro a prestar (o 'cancelar'): " + Fore.RESET)
    if entrada.lower() == 'cancelar':
        print(Fore.YELLOW + "Operacion cancelada.")
        return id_prestamo_actual

    try:
        id_libro = int(entrada)
        
        titulo = CRUD_LIBROS.obtener_titulo(arch_libros, id_libro)
        if titulo == "Desconocido":
            print(Fore.RED + "No se encontro un libro con el ID provisto.")
            return id_prestamo_actual
            
        if not CRUD_LIBROS.verificar_disponibilidad(arch_libros, id_libro):
            print(Fore.RED + "Operacion denegada: no hay ejemplares disponibles.")
            return id_prestamo_actual
            
        nombre = input(Fore.YELLOW + "Nombre del solicitante (o 'cancelar'): " + Fore.RESET)
        if nombre.lower() == 'cancelar':
            print(Fore.YELLOW + "Operacion cancelada.")
            return id_prestamo_actual

        f_prestamo = leer_fecha("Fecha de prestamo")
        if not f_prestamo:
            print(Fore.YELLOW + "Operacion cancelada.")
            return id_prestamo_actual

        f_esperada = leer_fecha("Fecha esperada de devolucion")
        if not f_esperada:
            print(Fore.YELLOW + "Operacion cancelada.")
            return id_prestamo_actual
        
        nuevo_prestamo = {
            "id_prestamo": id_prestamo_actual,
            "id_libro": id_libro,
            "solicitante": nombre,
            "fecha_prestamo": f_prestamo,
            "fecha_esperada": f_esperada
        }
        
        try:
            arch_p = open(arch_prestamos, "at")
            arch_p.write(json.dumps(nuevo_prestamo) + "\n")
        except OSError:
            print(Fore.RED + "Error al guardar el prestamo.")
            return id_prestamo_actual
        finally:
            try: arch_p.close()
            except NameError: pass
            
        CRUD_LIBROS.modificar_stock(arch_libros, id_libro, -1)
        
        print(Fore.GREEN + "Prestamo registrado exitosamente.")
        return id_prestamo_actual + 1
        
    except ValueError:
        print(Fore.RED + "Error: debe ingresar un numero valido.")
    return id_prestamo_actual

def eliminar_prestamo(arch_libros, arch_prestamos):
    print(Fore.CYAN + Style.BRIGHT + "\n--- Devolucion de prestamo ---")
    entrada = input(Fore.YELLOW + "Ingrese el ID del prestamo a cerrar (o 'cancelar'): " + Fore.RESET)
    if entrada.lower() == 'cancelar':
        print(Fore.YELLOW + "Operacion cancelada.")
        return

    try:
        id_prestamo = int(entrada)
        ent_p = open(arch_prestamos, "rt")
        sal_p = open("temp_prestamos.json", "wt")
        encontrado = False
        abortar = False
        id_libro_devuelto = -1
        
        for linea in ent_p:
            p = json.loads(linea)
            if p["id_prestamo"] == id_prestamo:
                f_real = leer_fecha("Ingrese la fecha real de devolucion")
                if not f_real:
                    abortar = True
                    break # Rompemos el ciclo para no seguir procesando
                
                encontrado = True
                id_libro_devuelto = p["id_libro"]
                penalizacion = calcular_penalizacion(p["fecha_esperada"], f_real)
                
                if penalizacion > 0:
                    print(Fore.RED + f"\n¡ATENCION! El usuario se ha retrasado.")
                    print(Fore.RED + f"Debe abonar una penalizacion de: ${penalizacion}")
                else:
                    print(Fore.GREEN + "\nDevolucion a tiempo. Sin penalizacion.")
            else:
                sal_p.write(linea)
    except (FileNotFoundError, ValueError, OSError):
        print(Fore.RED + "Error en la operacion o ingreso invalido.")
        abortar = True
    finally:
        try: ent_p.close()
        except NameError: pass
        try: sal_p.close()
        except NameError: pass

    if abortar:
        try: os.remove("temp_prestamos.json")
        except: pass
        print(Fore.YELLOW + "Operacion cancelada.")
        return

    if encontrado:
        os.remove(arch_prestamos)
        os.rename("temp_prestamos.json", arch_prestamos)
        
        CRUD_LIBROS.modificar_stock(arch_libros, id_libro_devuelto, 1)
        print(Fore.GREEN + "Prestamo cerrado y libro retornado al stock exitosamente.")
    else:
        try: os.remove("temp_prestamos.json")
        except: pass
        print(Fore.RED + "No se encontro un prestamo con el ID indicado.")