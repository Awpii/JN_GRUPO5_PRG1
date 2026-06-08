import json
import os
import crud_libros as CRUD_LIBROS

def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

def dias_del_mes(mes, anio):
    if mes in [1, 3, 5, 7, 8, 10, 12]: return 31
    elif mes in [4, 6, 9, 11]: return 30
    elif mes == 2: return 29 if es_bisiesto(anio) else 28
    return 0

def fecha_a_dias(fecha):
    dia, mes, anio = fecha[0], fecha[1], fecha[2]
    dias = 0
    for a in range(1, anio):
        dias += 366 if es_bisiesto(a) else 365
    for m in range(1, mes):
        dias += dias_del_mes(m, anio)
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
            cadena = input(msj + " (DD/MM/AAAA): ")
            partes = cadena.split("/")
            if len(partes) != 3:
                raise ValueError
            dia, mes, anio = int(partes[0]), int(partes[1]), int(partes[2])
            if dia < 1 or dia > 31 or mes < 1 or mes > 12 or anio < 1000:
                raise ValueError
            return [dia, mes, anio]
        except ValueError:
            print("Formato invalido. Use numeros separados por barra (/).")

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
    print("\n--- Lista de prestamos existentes ---")
    try:
        arch = open(arch_prestamos, "rt")
        hoy = leer_fecha("Ingrese fecha actual para calcular estado")
        
        for linea in arch:
            p = json.loads(linea)
            titulo_libro = CRUD_LIBROS.obtener_titulo(arch_libros, p["id_libro"])
            penalizacion = calcular_penalizacion(p["fecha_esperada"], hoy)
            
            f_p = f"{p['fecha_prestamo'][0]:02d}/{p['fecha_prestamo'][1]:02d}/{p['fecha_prestamo'][2]}"
            f_e = f"{p['fecha_esperada'][0]:02d}/{p['fecha_esperada'][1]:02d}/{p['fecha_esperada'][2]}"
            
            print(f"ID Prestamo: {p['id_prestamo']} | Solicitante: {p['solicitante']} | Libro: '{titulo_libro}'")
            print(f"   Otorgado: {f_p} | Vencimiento: {f_e}")
            if penalizacion > 0:
                print(f"   ¡ATRASADO! Penalizacion acumulada: ${penalizacion}")
            else:
                print("   Estado: Al dia.")
            print("-")
    except FileNotFoundError:
        print("No hay prestamos activos.")
    finally:
        try: arch.close()
        except NameError: pass
    print("----------------------------------\n")

def crear_prestamo(arch_libros, arch_prestamos, id_prestamo_actual):
    CRUD_LIBROS.imprimir_libros(arch_libros)
    try:
        id_libro = int(input("Ingrese el ID del libro a prestar: "))
        
        # Validamos usando funciones del modulo CRUD_LIBROS
        titulo = CRUD_LIBROS.obtener_titulo(arch_libros, id_libro)
        if titulo == "Desconocido":
            print("No se encontro un libro con el ID provisto.")
            return id_prestamo_actual
            
        if not CRUD_LIBROS.verificar_disponibilidad(arch_libros, id_libro):
            print("Operacion denegada: no hay ejemplares disponibles.")
            return id_prestamo_actual
            
        nombre = input("Nombre del solicitante: ")
        f_prestamo = leer_fecha("Fecha de prestamo")
        f_esperada = leer_fecha("Fecha esperada de devolucion")
        
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
            print("Error al guardar el prestamo.")
            return id_prestamo_actual
        finally:
            try: arch_p.close()
            except NameError: pass
            
        # Restamos 1 al stock disponible
        CRUD_LIBROS.modificar_stock(arch_libros, id_libro, -1)
        
        print("Prestamo registrado exitosamente.")
        return id_prestamo_actual + 1
        
    except ValueError:
        print("Error: debe ingresar un numero valido.")
    return id_prestamo_actual

def eliminar_prestamo(arch_libros, arch_prestamos):
    print("\n--- Devolucion de prestamo ---")
    try:
        id_prestamo = int(input("Ingrese el ID del prestamo a cerrar: "))
        ent_p = open(arch_prestamos, "rt")
        sal_p = open("temp_prestamos.json", "wt")
        encontrado = False
        id_libro_devuelto = -1
        
        for linea in ent_p:
            p = json.loads(linea)
            if p["id_prestamo"] == id_prestamo:
                encontrado = True
                id_libro_devuelto = p["id_libro"]
                f_real = leer_fecha("Ingrese la fecha real de devolucion")
                penalizacion = calcular_penalizacion(p["fecha_esperada"], f_real)
                
                if penalizacion > 0:
                    print(f"\n¡ATENCION! El usuario se ha retrasado.")
                    print(f"Debe abonar una penalizacion de: ${penalizacion}")
                else:
                    print("\nDevolucion a tiempo. Sin penalizacion.")
            else:
                sal_p.write(linea)
    except (FileNotFoundError, ValueError, OSError):
        print("Error en la operacion.")
        return
    finally:
        try: ent_p.close()
        except NameError: pass
        try: sal_p.close()
        except NameError: pass

    if encontrado:
        os.remove(arch_prestamos)
        os.rename("temp_prestamos.json", arch_prestamos)
        
        # Sumamos 1 al stock disponible
        CRUD_LIBROS.modificar_stock(arch_libros, id_libro_devuelto, 1)
        print("Prestamo cerrado y libro retornado al stock exitosamente.")
    else:
        try: os.remove("temp_prestamos.json")
        except: pass
        print("No se encontro un prestamo con el ID indicado.")