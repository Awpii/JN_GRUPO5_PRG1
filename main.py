import crud_usuarios as CRUD_USUARIOS
import crud_libros as CRUD_LIBROS
import crud_prestamos as CRUD_PRESTAMOS

print("=========================================")
print("    GESTION BIBLIOTECARIA - GRUPO 5      ")
print("=========================================")

ARCH_USUARIOS = "usuarios.json"
ARCH_LIBROS = "libros.json"
ARCH_PRESTAMOS = "prestamos.json"

logueado = False
rol_usuario = ""

while not logueado:
    print("\n--- Iniciar sesion---")
    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    
    resultado = CRUD_USUARIOS.iniciar_sesion(ARCH_USUARIOS, usuario, contraseña)
    
    if resultado == "ARCHIVO_NO_ENCONTRADO":
        print("ERROR CRITICO: El archivo 'usuarios.json' no existe.")
        print("Por favor, cree el archivo para poder ingresar.")
        exit()
    elif resultado == "USUARIO_INEXISTENTE":
        print("ERROR: Usuario inexistente.")
    elif resultado == "CLAVE_INCORRECTA":
        print("ERROR: Contraseña incorrecta.")
    else:
        rol_usuario = resultado
        logueado = True
        
print(f"\nBienvenido, {usuario}!\n")

# Calculamos los IDs leyendo los archivos linea por linea
id_libro_auto = CRUD_LIBROS.obtener_proximo_id(ARCH_LIBROS)
id_prestamo_auto = CRUD_PRESTAMOS.obtener_proximo_id(ARCH_PRESTAMOS)

seguir = True
while seguir:
    if rol_usuario == "empleado":
        print("\n=== MENU EMPLEADO ===")
        print("1. Añadir libro")
        print("2. Modificar libro")
        print("3. Eliminar libro")
        print("4. Buscar libro")
        print("5. Ver lista completa de libros")
        print("6. Crear prestamo")
        print("7. Cerrar prestamo (Devolucion / Multas)")
        print("8. Consultar prestamos vigentes")
        print("9. Salir")

        opcion = input("Ingrese opcion: ")
        match opcion:
            case "1": id_libro_auto = CRUD_LIBROS.add_libro(ARCH_LIBROS, id_libro_auto)
            case "2": CRUD_LIBROS.modificar_libro(ARCH_LIBROS)
            case "3": CRUD_LIBROS.eliminar_libro(ARCH_LIBROS)
            case "4": CRUD_LIBROS.buscar_libro(ARCH_LIBROS)
            case "5": CRUD_LIBROS.imprimir_libros(ARCH_LIBROS)
            case "6": id_prestamo_auto = CRUD_PRESTAMOS.crear_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS, id_prestamo_auto)
            case "7": CRUD_PRESTAMOS.eliminar_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS)
            case "8": CRUD_PRESTAMOS.imprimir_prestamos(ARCH_PRESTAMOS, ARCH_LIBROS)
            case "9":
                print("Saliendo del programa.")
                seguir = False
            case _: print("Opcion invalida.")
                
    elif rol_usuario == "cliente":
        print("\n=== MENU CLIENTE ===")
        print("1. Solicitar prestamo")
        print("2. Devolver prestamo")
        print("3. Buscar libros disponibles")
        print("4. Ver lista completa de libros")
        print("5. Salir")
        
        opcion = input("Ingrese opcion: ")
        match opcion:
            case "1": id_prestamo_auto = CRUD_PRESTAMOS.crear_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS, id_prestamo_auto)
            case "2": CRUD_PRESTAMOS.eliminar_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS)
            case "3": CRUD_LIBROS.buscar_libro(ARCH_LIBROS)
            case "4": CRUD_LIBROS.imprimir_libros(ARCH_LIBROS)
            case "5":
                print("Saliendo del programa.")
                seguir = False
            case _: print("Opción invalida.")