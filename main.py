import gestion

print("=========================================")
print("    GESTION BIBLIOTECARIA - GRUPO 5      ")
print("=========================================")

#usuario = input("Ingrese su usuario: ")
#contraseña = input("Ingrese su contraseña: ") #Todavía no los valido porque no podemos usar archivos xd
#print(f"\n Bienvenido, {usuario}!\n")

#inicio matrices

#esta matriz después la voy a cambiar, esto es para demostración en la primera entrega
matriz_libros = [
    [1, "Cien años de soledad", "Gabriel Garcia Marquez", "N"],
    [2, "1984", "George Orwell", "S"],
    [3, "El Aleph", "Jorge Luis Borges", "N"]
]
matriz_prestamos = [
    [1, 2, "Juan Perez"] # Prestamo 1 = libro 2 (1984), cuando veamos archivos esto va a ser mejor
]

id_libro_auto = 4
id_prestamo_auto = 2  #estos son contadores para los IDs, los cambio despues, la idea es hacerlo automaticamente pero esto es para la entrega

logueado = False
rol_usuario = "" # -> Esto es para simular una validación de usuario, la idea es después cuando veamos JSON tener un documento que haga de "Base de datos"

while not logueado:
    print("\n--- Iniciar sesion---")
    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    
    #aca hardcodee unos datos para la demo
    if usuario == "empleado" and contraseña == "admin":
        rol_usuario = "empleado"
        logueado = True
    elif usuario == "cliente" and contraseña == "1234":
        rol_usuario = "cliente"
        logueado = True
    else:
        print("ERROR: Usuario o contraseña incorrectos. ")
        
print(f"\nBienvenido, {usuario}!\n")

seguir = True

while seguir:
    if rol_usuario == "empleado":
        print("Seleccione una opción:")
        print("1. Añadir libro")
        print("2. Eliminar libro")
        print("3. Crear prestamo")
        print("4. Eliminar prestamo")
        print("5. Salir")


        opcion = input("Ingrese el numero de la opción deseada: ")
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
                print("Opción invalida")
                
    elif rol_usuario == "cliente":
        
        print("Seleccione una opción:")
        print("1. Solicitar prestamo")
        print("2. Devolver prestamo")
        print("3. Salir")
        
        opcion = input("Ingrese el numero de la opción deseada: ")
        match opcion:
            case "1":
                id_prestamo_auto = gestion.crear_prestamo(matriz_libros, matriz_prestamos, id_prestamo_auto)
            case "2":
                gestion.eliminar_prestamo(matriz_libros, matriz_prestamos)
            case "3":
                print("Saliendo del programa.")
                seguir = False
            case _:
                print("Opción invalida.")