import json
import os
from colorama import Fore, Style, init

init(autoreset=True)

def obtener_proximo_id(nombre_archivo):
    max_id = 0
    try:
        arch = open(nombre_archivo, "rt")
        for linea in arch:
            obj = json.loads(linea)
            if obj["id"] > max_id:
                max_id = obj["id"]
    except FileNotFoundError:
        pass
    finally:
        try: arch.close()
        except NameError: pass
    return max_id + 1

def imprimir_libros(arch_libros):
    print(Fore.CYAN + Style.BRIGHT + "\n--- Lista de libros existentes ---")
    try:
        arch = open(arch_libros, "rt")
        for linea in arch:
            lib = json.loads(linea)
            print(f"ID: {lib['id']} | Titulo: '{lib['titulo']}' | Autor: {lib['autor']} | Ed: {lib['edicion']} | Año: {lib['año']} | Edt: {lib['editorial']} | Disp: {lib['cant_disp']}/{lib['cant_total']}")
    except FileNotFoundError:
        print(Fore.RED + "No hay libros registrados")
    finally:
        try: arch.close()
        except NameError: pass
    print(Fore.CYAN + "----------------------------------\n")

def mostrar_autores(arch_libros):
    print(Fore.CYAN + Style.BRIGHT + "\n--- Autores Registrados (Sin duplicados) ---")
    autores = set() 
    try:
        arch = open(arch_libros, "rt")
        for linea in arch:
            lib = json.loads(linea)
            autores.add(lib["autor"]) 
    except FileNotFoundError:
        print(Fore.RED + "No hay libros registrados")
    finally:
        try: arch.close()
        except NameError: pass
        
    if len(autores) > 0:
        lista_formateada = [f"▪ {autor}" for autor in autores]
        for a in lista_formateada:
            print(Fore.GREEN + a)
    print(Fore.CYAN + "----------------------------------\n")

def buscar_libro(arch_libros):
    print(Fore.CYAN + Style.BRIGHT + "\n--- Buscar Libro ---")
    print("1. Titulo | 2. Autor | 3. Editorial | 4. Año de publicacion | 5. Cancelar")
    opc = input(Fore.YELLOW + "Seleccione criterio: " + Fore.RESET)
    
    if opc == "5" or opc.lower() == "cancelar":
        print(Fore.YELLOW + "Operacion cancelada")
        return

    termino = input(Fore.YELLOW + "Ingrese el termino de busqueda (o 'cancelar'): " + Fore.RESET).lower()
    if termino == "cancelar":
        print(Fore.YELLOW + "Operacion cancelaada")
        return

    encontrados = False
    print(Fore.GREEN + "\nResultados:")
    try:
        arch = open(arch_libros, "rt")
        for linea in arch:
            lib = json.loads(linea)
            coincidencia = False
            if opc == "1" and termino in lib["titulo"].lower(): coincidencia = True
            elif opc == "2" and termino in lib["autor"].lower(): coincidencia = True
            elif opc == "3" and termino in lib["editorial"].lower(): coincidencia = True
            elif opc == "4" and termino == str(lib["año"]): coincidencia = True
                
            if coincidencia:
                print(f"ID: {lib['id']} | Titulo: '{lib['titulo']}' | Autor: {lib['autor']} | Año: {lib['año']} | Disp: {lib['cant_disp']}/{lib['cant_total']}")
                encontrados = True
    except FileNotFoundError:
        pass
    finally:
        try: arch.close()
        except NameError: pass
            
    if not encontrados:
        print(Fore.RED + "No se encontraron matches")

def add_libro(arch_libros, id_actual):
    print(Fore.CYAN + Style.BRIGHT + "\n--- Añadir un nuevo libro ---")
    titulo = input(Fore.YELLOW + "Titulo (o 'cancelar'): " + Fore.RESET)
    if titulo.lower() == "cancelar": return id_actual
    
    autor = input(Fore.YELLOW + "Autor (o 'cancelar'): " + Fore.RESET)
    if autor.lower() == "cancelar": return id_actual
    
    edicion = input(Fore.YELLOW + "Edicion (o 'cancelar'): " + Fore.RESET)
    if edicion.lower() == "cancelar": return id_actual
    
    try:
        entrada_año = input(Fore.YELLOW + "Año de publicacion (o 'cancelar'): " + Fore.RESET)
        if entrada_año.lower() == "cancelar": return id_actual
        año = int(entrada_año)
        
        entrada_cant = input(Fore.YELLOW + "Cantidad de ejemplares (o 'cancelar'): " + Fore.RESET)
        if entrada_cant.lower() == "cancelar": return id_actual
        cantidad = int(entrada_cant)
    except ValueError:
        print(Fore.RED + "Error: El año y la cantidad deben ser numeros enteros.")
        return id_actual
        
    editorial = input(Fore.YELLOW + "Editorial (o 'cancelar'): " + Fore.RESET)
    if editorial.lower() == "cancelar": return id_actual
    
    try:
        nuevo_libro = {
            "id": id_actual, "titulo": titulo, "autor": autor, "edicion": edicion,
            "año": año, "editorial": editorial, "cant_total": cantidad, "cant_disp": cantidad
        }
        arch = open(arch_libros, "at")
        arch.write(json.dumps(nuevo_libro) + "\n")
        print(Fore.GREEN + "Libro agregado añadido con exito")
        return id_actual + 1
    except OSError as error:
        print(Fore.RED + f"error al guardar: {error}")
        return id_actual
    finally:
        try: arch.close()
        except NameError: pass

def modificar_libro(arch_libros):
    imprimir_libros(arch_libros)
    entrada = input(Fore.YELLOW + "Ingrese el ID del libro a modificar (o cancelar): " + Fore.RESET)
    if entrada.lower() == 'cancelar':
        print(Fore.YELLOW + "Operacion cancelada")
        return
        
    try:
        id_mod = int(entrada)
        ent = open(arch_libros, "rt")
        sal = open("temp_libros.json", "wt")
        modificado = False
        abortar = False
        
        for linea in ent:
            lib = json.loads(linea)
            if lib["id"] == id_mod:
                print(Fore.CYAN + "1. Titulo | 2. Autor | 3. Edicion | 4. Año | 5. Editorial | 6. Cant. Total | 7. Cancelar")
                opc = input(Fore.YELLOW + "Que campo desea modificar? " + Fore.RESET)
                
                if opc == "7" or opc.lower() == "cancelar":
                    abortar = True
                    break
                    
                match opc:
                    case "1": lib["titulo"] = input(Fore.YELLOW + "Nuevo Titulo: " + Fore.RESET)
                    case "2": lib["autor"] = input(Fore.YELLOW + "Nuevo Autor: " + Fore.RESET)
                    case "3": lib["edicion"] = input(Fore.YELLOW + "Nueva Edicion: " + Fore.RESET)
                    case "4": lib["año"] = int(input(Fore.YELLOW + "Nuevo Año: " + Fore.RESET))
                    case "5": lib["editorial"] = input(Fore.YELLOW + "Nueva Editorial: " + Fore.RESET)
                    case "6": 
                        nueva_cant = int(input(Fore.YELLOW + "Nueva Cantidad Total: " + Fore.RESET))
                        dif = nueva_cant - lib["cant_total"]
                        lib["cant_total"] = nueva_cant
                        lib["cant_disp"] += dif
                    case _: print(Fore.RED + "opcion invalida")
                modificado = True
            sal.write(json.dumps(lib) + "\n")
            
    except (FileNotFoundError, ValueError, OSError):
        print(Fore.RED + "error en la operacion o ingreso invalido")
        abortar = True
    finally:
        try: ent.close()
        except NameError: pass
        try: sal.close()
        except NameError: pass
        
    if abortar:
        try: os.remove("temp_libros.json")
        except: pass
        print(Fore.YELLOW + "ooperacion cancelada")
        return
        
    if modificado:
        os.remove(arch_libros)
        os.rename("temp_libros.json", arch_libros)
        print(Fore.GREEN + "Libro modificado con exito")
    else:
        try: os.remove("temp_libros.json")
        except: pass
        print(Fore.RED + "ID no encontrado")

def eliminar_libro(arch_libros):
    imprimir_libros(arch_libros)
    entrada = input(Fore.YELLOW + "Iingrese el ID del libro que desea eliminar (o cancelar): " + Fore.RESET)
    if entrada.lower() == 'cancelar':
        print(Fore.YELLOW + "operacion cancelada.")
        return
        
    try:
        id_eliminar = int(entrada)
        ent = open(arch_libros, "rt")
        sal = open("temp_libros.json", "wt")
        eliminado = False
        
        for linea in ent:
            lib = json.loads(linea)
            if lib["id"] == id_eliminar:
                eliminado = True
            else:
                sal.write(linea)
    except (FileNotFoundError, ValueError, OSError):
        print(Fore.RED + "Error en la operacion o ingreso invalido")
        return
    finally:
        try: ent.close()
        except NameError: pass
        try: sal.close()
        except NameError: pass
        
    if eliminado:
        os.remove(arch_libros)
        os.rename("temp_libros.json", arch_libros)
        print(Fore.GREEN + "Libro eliminado con exito")
    else:
        try: os.remove("temp_libros.json")
        except: pass
        print(Fore.RED + "No se encontro un libro con el ID dado")

def obtener_titulo(arch_libros, id_libro):
    titulo = "Desconocido"
    try:
        arch = open(arch_libros, "rt")
        for linea in arch:
            lib = json.loads(linea)
            if lib["id"] == id_libro:
                titulo = lib["titulo"]
                break
    except FileNotFoundError:
        pass
    finally:
        try: arch.close()
        except NameError: pass
    return titulo

def verificar_disponibilidad(arch_libros, id_libro):
    disponible = False
    try:
        arch = open(arch_libros, "rt")
        for linea in arch:
            lib = json.loads(linea)
            if lib["id"] == id_libro and lib["cant_disp"] > 0:
                disponible = True
                break
    except FileNotFoundError:
        pass
    finally:
        try: arch.close()
        except NameError: pass
    return disponible

def modificar_stock(arch_libros, id_libro, variacion):
    """Suma o resta a la cantidad disponible de un libro"""
    hubo_error = False
    try:
        ent = open(arch_libros, "rt")
        sal = open("temp_libros.json", "wt")
        for linea in ent:
            lib = json.loads(linea)
            if lib["id"] == id_libro:
                lib["cant_disp"] += variacion
                try:
                    assert lib["cant_disp"] >= 0, "error critico: Stock negativo detectado"
                except AssertionError as msg:
                    print(Fore.RED + str(msg))
                    lib["cant_disp"] = 0 # fuerzo a 0 para no romper el archivo que usamos de base de datos
            sal.write(json.dumps(lib) + "\n")
    except (FileNotFoundError, OSError):
        hubo_error = True
    finally:
        try: ent.close()
        except NameError: pass
        try: sal.close()
        except NameError: pass
        
    if not hubo_error:
        try:
            os.remove(arch_libros)
            os.rename("temp_libros.json", arch_libros)
        except OSError:
            pass