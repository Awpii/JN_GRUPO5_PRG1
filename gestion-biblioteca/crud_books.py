import gestion_datos
import utils as utilidades

def registrar_libro():
    #Pedir datos y crear libro nuevo en books.json
    print("\n--- Registrar nuevo libro ---")
    titulo = input("Título: ").strip().title()
    autor = input("Autor: ").strip().title()
    
    if titulo and autor:
        libros = gestion_datos.cargar_libros()
        nuevo_id = utilidades.generar_nuevo_id(libros, 'L')
        nuevo_libro = {
            "ID_Libro": nuevo_id, "Titulo": titulo, "Autor": autor,
            "Estado": "Disponible", "Fecha_Ingreso": utilidades.obtener_fecha_actual_str()
        }
        libros.append(nuevo_libro)
        if not gestion_datos.guardar_libros(libros):
            utilidades.imprimir_error("No se pudo guardar el nuevo libro en el archivo de datos.")
        else:
            utilidades.imprimir_exito(f"Libro '{titulo}' registrado con ID: {nuevo_id}")
    else:
        utilidades.imprimir_error("Título y Autor son campos obligatorios.") #Lo mismo que en usuario, error si no agrega todos los campos
        
def eliminar_libro():
    #Eliminar libro por ID, siempre que NO ESTÉ PRESTADO
    print("\n--- Eliminar libro ---")
    id_libro = input("Ingrese el ID del libro a eliminar (ej. L001): ").strip().upper()
    
    if utilidades.validar_id(id_libro, 'libro'):
        prestamos = gestion_datos.cargar_prestamos()
        prestamo_activo_encontrado = any(
            p['Estado_Prestamo'] == 'Activo' and id_libro in p['ID_Libros'] for p in prestamos
        )
        if not prestamo_activo_encontrado:
            libros = gestion_datos.cargar_libros()
            longitud_inicial = len(libros)
            libros_actualizados = list(filter(lambda l: l['ID_Libro'] != id_libro, libros)) #Filtra por el libro designado por ID para la eliminación
            if len(libros_actualizados) < longitud_inicial:
                if gestion_datos.guardar_libros(libros_actualizados):
                    utilidades.imprimir_exito(f"Libro con ID {id_libro} eliminado correctamente.")
            else:
                utilidades.imprimir_error(f"No se encontró un libro con el ID {id_libro}.")
        else:
            utilidades.imprimir_error(f"No se puede eliminar el libro {id_libro}. El libro se encuentra prestado.")
    else:
        utilidades.imprimir_error("Formato de ID inválido.")

def libros_recursividad(lista_de_libros):
    
    if not lista_de_libros:
        return
    else:
        libro_actual = lista_de_libros[0] 
        print(f"{libro_actual.get('ID_Libro', ''):<10} | {libro_actual.get('Titulo', ''):<40} | {libro_actual.get('Autor', ''):<25} | {libro_actual.get('Estado', ''):<12}") #se saca el primer libro de la lista
        
        libros_recursividad(lista_de_libros[1:]) #reinvoco la funcion de nuevo con el slice

def ver_libros():
    #Mostrar los libros por titulo.
    print("\n--- Inventario de Libros ---")
    libros = gestion_datos.cargar_libros()
    
    if not libros:
        utilidades.imprimir_advertencia("No hay libros en el inventario.")
    else:
        libros_ordenados = sorted(libros, key = lambda libro: libro['ID_Libro']) #Ordena los libros por ID.
        print(f"{'ID_Libro':<10} | {'Titulo':<40} | {'Autor':<25} | {'Estado':<12}")
        print("-" * 80)
        libros_recursividad(libros_ordenados)