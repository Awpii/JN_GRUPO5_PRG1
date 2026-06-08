import json
import os

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
    print("\n--- Lista de libros existentes ---")
    try:
        arch = open(arch_libros, "rt")
        for linea in arch:
            lib = json.loads(linea)
            print(f"ID: {lib['id']} | Titulo: '{lib['titulo']}' | Autor: {lib['autor']} | Ed: {lib['edicion']} | Año: {lib['anio']} | Edt: {lib['editorial']} | Disp: {lib['cant_disp']}/{lib['cant_total']}")
    except FileNotFoundError:
        print("No hay libros registrados.")
    finally:
        try: arch.close()
        except NameError: pass
    print("----------------------------------\n")

def buscar_libro(arch_libros):
    print("\n--- Buscar Libro ---")
    print("1. Titulo | 2. Autor | 3. Editorial | 4. Año de publicacion")
    opc = input("Seleccione criterio: ")
    termino = input("Ingrese el termino de busqueda: ").lower()
    encontrados = False
    
    print("\nResultados:")
    try:
        arch = open(arch_libros, "rt")
        for linea in arch:
            lib = json.loads(linea)
            coincidencia = False
            if opc == "1" and termino in lib["titulo"].lower(): coincidencia = True
            elif opc == "2" and termino in lib["autor"].lower(): coincidencia = True
            elif opc == "3" and termino in lib["editorial"].lower(): coincidencia = True
            elif opc == "4" and termino == str(lib["anio"]): coincidencia = True
                
            if coincidencia:
                print(f"ID: {lib['id']} | Titulo: '{lib['titulo']}' | Autor: {lib['autor']} | Año: {lib['anio']} | Disp: {lib['cant_disp']}/{lib['cant_total']}")
                encontrados = True
    except FileNotFoundError:
        pass
    finally:
        try: arch.close()
        except NameError: pass
            
    if not encontrados:
        print("No se encontraron coincidencias.")

def add_libro(arch_libros, id_actual):
    print("\n--- Añadir un nuevo libro ---")
    try:
        nuevo_libro = {
            "id": id_actual,
            "titulo": input("Titulo: "),
            "autor": input("Autor: "),
            "edicion": input("Edicion: "),
            "anio": int(input("Año de publicacion: ")),
            "editorial": input("Editorial: "),
            "cant_total": int(input("Cantidad de ejemplares: "))
        }
        nuevo_libro["cant_disp"] = nuevo_libro["cant_total"]
        
        arch = open(arch_libros, "at")
        arch.write(json.dumps(nuevo_libro) + "\n")
        print("Libro añadido con exito.")
        return id_actual + 1
    except ValueError:
        print("Error: El año y la cantidad deben ser numeros enteros.")
        return id_actual
    except OSError as error:
        print("Error al guardar:", error)
        return id_actual
    finally:
        try: arch.close()
        except NameError: pass

def modificar_libro(arch_libros):
    imprimir_libros(arch_libros)
    try:
        id_mod = int(input("Ingrese el ID del libro a modificar: "))
        ent = open(arch_libros, "rt")
        sal = open("temp_libros.json", "wt")
        modificado = False
        
        for linea in ent:
            lib = json.loads(linea)
            if lib["id"] == id_mod:
                print("1. Titulo | 2. Autor | 3. Edicion | 4. Año | 5. Editorial | 6. Cant. Total")
                opc = input("Que campo desea modificar? ")
                match opc:
                    case "1": lib["titulo"] = input("Nuevo Titulo: ")
                    case "2": lib["autor"] = input("Nuevo Autor: ")
                    case "3": lib["edicion"] = input("Nueva Edicion: ")
                    case "4": lib["anio"] = int(input("Nuevo Año: "))
                    case "5": lib["editorial"] = input("Nueva Editorial: ")
                    case "6": 
                        nueva_cant = int(input("Nueva Cantidad Total: "))
                        dif = nueva_cant - lib["cant_total"]
                        lib["cant_total"] = nueva_cant
                        lib["cant_disp"] += dif
                    case _: print("Opcion invalida.")
                modificado = True
            sal.write(json.dumps(lib) + "\n")
            
    except (FileNotFoundError, ValueError, OSError):
        print("Error en la operacion.")
    finally:
        try: ent.close()
        except NameError: pass
        try: sal.close()
        except NameError: pass
        
    if modificado:
        os.remove(arch_libros)
        os.rename("temp_libros.json", arch_libros)
        print("Libro modificado.")
    else:
        try: os.remove("temp_libros.json")
        except: pass
        print("ID no encontrado.")

def eliminar_libro(arch_libros):
    imprimir_libros(arch_libros)
    try:
        id_eliminar = int(input("Ingrese el ID del libro que desea eliminar: "))
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
        print("Error en la operacion.")
    finally:
        try: ent.close()
        except NameError: pass
        try: sal.close()
        except NameError: pass
        
    if eliminado:
        os.remove(arch_libros)
        os.rename("temp_libros.json", arch_libros)
        print("Libro eliminado con exito.")
    else:
        try: os.remove("temp_libros.json")
        except: pass
        print("No se encontro un libro con el ID dado.")

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
    try:
        ent = open(arch_libros, "rt")
        sal = open("temp_libros.json", "wt")
        for linea in ent:
            lib = json.loads(linea)
            if lib["id"] == id_libro:
                lib["cant_disp"] += variacion
            sal.write(json.dumps(lib) + "\n")
    except (FileNotFoundError, OSError):
        pass
    finally:
        try: ent.close()
        except NameError: pass
        try: sal.close()
        except NameError: pass
        
    try:
        os.remove(arch_libros)
        os.rename("temp_libros.json", arch_libros)
    except OSError:
        pass