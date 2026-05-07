def imprimir_libros(libros):
    """
    Muestra en consola la lista de libros ordenados alfabéticamente por título.
    Si la lista está vacía, informa al usuario.
    
    Parámetros:
    - libros (list): Matriz donde cada elemento es una lista [id, titulo, autor, prestado].
    """
    print("\n--- Lista de libros existentes ---")
    if len(libros) == 0:
        print("No hay libros registrados en el sistema.")
    else:
        # Ordena por título (índice 1) usando una función lambda
        libros_ordenar = sorted(libros, key=lambda x: x[1])
        for libro in libros_ordenar:
            print(f"ID: {libro[0]}, Titulo: {libro[1]}, Autor: {libro[2]}, Prestado: {libro[3]}")
    print("----------------------------------\n")

    
def imprimir_prestamos(prestamos):
    """
    Muestra en consola la lista de préstamos actuales ordenados por el nombre del solicitante.
    
    Parámetros:
    - prestamos (list): Matriz donde cada elemento es [id_prestamo, id_libro, solicitante].
    """
    print("\n--- Lista de prestamos existentes ---")
    if len(prestamos) == 0:
        print("No hay prestamos existentes")
    else:
        # Ordena por nombre del solicitante (índice 2)
        prestamos_ordenar = sorted(prestamos, key=lambda x: x[2])
        for p in prestamos_ordenar:
            print(f"ID prestamo: {p[0]}| ID Libro: {p[1]} | Solicitante: {p[2]}")
    print("----------------------------------\n")

    
def add_libro(libros, id_actual):
    """
    Solicita datos al usuario para crear un nuevo libro y lo agrega a la matriz.
    
    Parámetros:
    - libros (list): Matriz de libros actual.
    - id_actual (int): El ID autoincremental que le corresponde al nuevo libro.
    
    Retorna:
    - int: El próximo ID disponible (id_actual + 1).
    """
    print("\n--- Añadir un nuevo libro ---")
    titulo = input("Ingrese el titulo del libro: ")
    autor = input("Ingrese el autor del libro: ")
    prestado = input("¿El libro está prestado? (S/N): ").upper()
    
    nuevo_libro = [id_actual, titulo, autor, prestado]
    libros.append(nuevo_libro)
    
    print("Libro añadido con exito.")
    return id_actual + 1


def eliminar_libro(libros):
    """
    Busca un libro por ID y lo elimina de la matriz si existe.
    
    Parámetros:
    - libros (list): Matriz de libros actual.
    """
    imprimir_libros(libros)
    if len(libros) > 0:
        entrada_id = input("Ingrese el ID del libro que desea eliminar: ")
        if entrada_id.isdigit():
            id_eliminar = int(entrada_id)
            encontrado = False
            i = 0
            while i < len(libros) and not encontrado:
                if libros[i][0] == id_eliminar:
                    libros.pop(i)
                    encontrado = True
                    print("Libro eliminado con exito.")
                else:
                    i += 1
            if not encontrado:
                print("No se encontró un libro con el ID dado.")
        else:
            print("Error: Ingrese un numero valido.")

        
def crear_prestamo(libros, prestamos, id_prestamo_actual):
    """
    Registra un préstamo. Verifica que el libro exista y no esté prestado actualmente.
    Cambia el estado del libro a 'S' (Si) en la matriz de libros.
    
    Parámetros:
    - libros (list): Matriz de libros.
    - prestamos (list): Matriz de préstamos.
    - id_prestamo_actual (int): ID autoincremental para el préstamo.
    
    Retorna:
    - int: El próximo ID de préstamo disponible.
    """
    imprimir_libros(libros)
    if len(libros) > 0:
        entrada_id = input("Ingrese el ID del libro a prestar: ")
        if entrada_id.isdigit():
            id_libro = int(entrada_id)
            indice_libro = -1
            i = 0
            while i < len(libros) and indice_libro == -1:
                if libros[i][0] == id_libro:
                    indice_libro = i
                i += 1
            
            if indice_libro != -1:
                if libros[indice_libro][3] == "S":
                    print("Operacion denegada: el libro ya esta prestado.")
                else:
                    nombre = input("Ingrese el nombre del solicitante: ")
                    nuevo_prestamo = [id_prestamo_actual, id_libro, nombre]
                    prestamos.append(nuevo_prestamo)
                    libros[indice_libro][3] = "S"
                    print("Prestamo creado exitosamente.")
                    return id_prestamo_actual + 1
            else:
                print("No se encontró un libro con el ID provisto.")
        else:
            print("Error: debe ingresar un numero valido.")
    return id_prestamo_actual


def eliminar_prestamo(libros, prestamos):
    """
    Cierra un préstamo activo. Elimina el registro de la matriz de préstamos y 
    vuelve a poner el libro como disponible ('N') en la matriz de libros.
    
    Parámetros:
    - libros (list): Matriz de libros.
    - prestamos (list): Matriz de préstamos.
    """
    imprimir_prestamos(prestamos)
    if len(prestamos) > 0:
        entrada_id = input("Ingrese el ID del préstamo a cerrar: ")
        if entrada_id.isdigit():
            id_prestamo = int(entrada_id)
            indice_prestamo = -1
            i = 0
            while i < len(prestamos) and indice_prestamo == -1:
                if prestamos[i][0] == id_prestamo:
                    indice_prestamo = i
                i += 1
            
            if indice_prestamo != -1:
                id_libro = prestamos[indice_prestamo][1]
                prestamos.pop(indice_prestamo)
                
                # Buscar el libro para marcarlo como disponible de nuevo
                encontrado = False
                j = 0
                while j < len(libros) and not encontrado:
                    if libros[j][0] == id_libro:
                        libros[j][3] = "N"
                        encontrado = True
                    j += 1
                print("Prestamo eliminado exitosamente. El libro vuelve a estar disponible.")
            else:
                print("No se encontro un prestamo con el ID indicado.")
        else:
            print("Error: debe ingresar un numero valido.")
            
