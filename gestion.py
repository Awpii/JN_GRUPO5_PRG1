def imprimir_libros(libros):
    print("\n--- Lista de libros existentes ---")
    if len(libros) == 0:
        print("No hay libros registrados en el sistema.")
    else:
        for libro in libros:
            #formato: Libro = [id_libro, titulo, autor, prestado S/N]
            print(f"ID: {libro[0]}, Titulo: {libro[1]}, Autor: {libro[2]}, Prestado: {libro[3]}")
    print("----------------------------------\n")
    
def imprimir_prestamos(prestamos):
    print("\n--- Lista de prestamos existentes ---")
    if len(prestamos) == 0:
        print("No hay prestamos existentes")
    else:
        for p in prestamos:
            print(f"ID prestamo: {p[0]}| ID Libro: {p[1]} | Solicitante: {p[2]}")
    print("----------------------------------\n")
    
def add_libro(libros, id_actual):
    print("\n--- Añadir un nuevo libro ---")
    titulo = input("Ingrese el titulo del libro: ")
    autor = input("Ingrese el autor del libro: ")
    prestado = input("¿El libro está prestado? (S/N): ").upper()
    
    #creo lista nueva para matriz de libros
    
    nuevo_libro = [id_actual, titulo, autor, prestado]
    libros.append(nuevo_libro)
    
    print("Libro añadido con exito.")
    return id_actual + 1


def eliminar_libro(libros):
    imprimir_libros(libros)
    if len(libros) > 0:
        entrada_id = input("Ingrese el ID del libro que desea eliminar: ")
        if entrada_id.isdigit(): #no podemos usar excepciones xd
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
    imprimir_libros(libros)
    if len(libros) > 0:
        entrada_id = input("Ingrese el ID del libro a prestar: ")
        if entrada_id.isdigit():
            id_libro = int(entrada_id)
            indice_libro = -1
            for i in range(len(libros)):
                if libros[i][0] == id_libro:
                    indice_libro = i
                    break
            if indice_libro != -1:
                if libros[indice_libro][3] == "SI":
                    print("Operación denegada: El libro ya se encuentra prestado.")
                else:
                    nombre = input("Ingrese el nombre del solicitante: ")
                    nuevo_prestamo = [id_prestamo_actual, id_libro, nombre]
                    prestamos.append(nuevo_prestamo)
                    libros[indice_libro][3] = "SI"
                    print("Prestamo generado con exito.")
                    return id_prestamo_actual + 1
            else:
                print("No se encontró un libro con el ID dado.")
        else:
            print("Error: debe ingresar un número valido.")
    return id_prestamo_actual

def eliminar_prestamo(libros, prestamos):
    imprimir_prestamos(prestamos)
    if len(prestamos) > 0:
        entrada_id = input("Ingrese el ID del préstamo a cerrar: ")
        if entrada_id.isdigit():
            id_prestamo = int(entrada_id)
            indice_prestamo = -1
            
            for i in range(len(prestamos)):
                if prestamos[i][0] == id_prestamo:
                    indice_prestamo = i
                    break
            
            if indice_prestamo != -1:
                id_libro = prestamos[indice_prestamo][1]
                prestamos.pop(indice_prestamo)
                for j in range(len(libros)):
                    if libros[j][0] == id_libro:
                        libros[j][3] = "NO"
                        break
                print("Préstamo cerrado con éxito.")
            else:
                print("No se encontró un préstamo con el ID dado.")
        else:
            print("Error: debe ingresar un número valido.")
