import gestion

print("=========================================")
print("    BIBLIOTEKEITOR 3000      ")
print("=========================================")

usuario = input("Ingrese su usuario: ")
contraseña = input("Ingrese su contraseña: ") #Todavía no los valido porque no podemos usar archivos xd
print(f"\n Bienvenido, {usuario}!\n")

#inicio matrices

matriz_libros = []
matriz_prestamos = []

id_libro_auto = 1
id_prestamo_auto = 1 #estos son contadores para los IDs, los cambio despues

seguir = True

while seguir:
    print("Seleccione una opción:")
    print("1. Añadir libro")
    print("2. Eliminar libro")
    print("3. Crear prestamo")
    print("4. Eliminar prestamo")
    print("5. Salir")


    opcion = input("Ingrese el número de la opción deseada: ")
    match opcion:
        case "1":
            id_libro_auto = gestion.add_libro(matriz_libros, id_libro_auto)
        case "2":
            gestion.eliminar_libro(matriz_libros)
        case "3":
            id_prestamo_auto = gestion.crear_prestamo(matriz_libros, matriz_prestamos, id_prestamo_auto)
        case "4":
            gestion.eliminar_prestamo(matriz_libros, matriz_prestamos)
        case "5":
            print("Saliendo del programa.")
            seguir = False
        case _:
            print("Opción no válida. Por favor, ingrese un número del 1 al 5.")
