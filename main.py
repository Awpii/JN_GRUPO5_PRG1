import crud_usuarios
import crud_libros
import crud_prestamos
import os
from colorama import Fore, Style, init

init(autoreset=True)

print(Fore.CYAN + Style.BRIGHT + "=========================================")
print(Fore.CYAN + Style.BRIGHT + "    GESTION BIBLIOTECARIA - GRUPO 5      ")
print(Fore.CYAN + Style.BRIGHT + "=========================================")

ARCH_USUARIOS = "C:\\VSCode\\School_Projects\\JN_GRUPO5_PRG1\\data\\usuarios.json"
ARCH_LIBROS = "C:\\VSCode\\School_Projects\\JN_GRUPO5_PRG1\\data\\libros.json"
ARCH_PRESTAMOS = "C:\\VSCode\\School_Projects\\JN_GRUPO5_PRG1\\data\\prestamos.json"

logueado = False
rol_usuario = ""

while not logueado:
    print(Fore.CYAN + "\n--- Iniciar sesion ---")
    usuario = input(Fore.YELLOW + "Ingrese su usuario (o 'cancelar' para salir): " + Fore.RESET)
    
    if usuario.lower() == 'cancelar':
        print(Fore.YELLOW + "Saliendo del sistema..")
        exit()
        
    contraseña = input(Fore.YELLOW + "Ingrese su contraseña: " + Fore.RESET)
    
    resultado = crud_usuarios.iniciar_sesion(ARCH_USUARIOS, usuario, contraseña)
    
    if resultado == "ARCHIVO_NO_ENCONTRADO":
        print(Fore.RED + Style.BRIGHT + "\nERROR CRITICO: El archivo 'usuarios.json' no existe")
        print(Fore.RED + "El programa esta buscando la base de datos en:")
        print(Fore.RED + f"-> {ARCH_USUARIOS}")
        print(Fore.RED + "Por favor mueva los archivos JSON a esa carpeta")
        exit()
    elif resultado == "USUARIO_INEXISTENTE":
        print(Fore.RED + "ERROR: Usuario inexistente")
    elif resultado == "CLAVE_INCORRECTA":
        print(Fore.RED + "ERROR - Contraseña incorrecta")
    else:
        rol_usuario = resultado
        logueado = True
        
print(Fore.GREEN + Style.BRIGHT + f"\nBienvenido {usuario}!\n")

id_libro_auto = crud_libros.obtener_proximo_id(ARCH_LIBROS)
id_prestamo_auto = crud_prestamos.obtener_proximo_id(ARCH_PRESTAMOS)

seguir = True
while seguir:
    if rol_usuario == "empleado":
        print(Fore.CYAN + Style.BRIGHT + "\n=== MENU EMPLEADO ===")
        print("1. Agregar libro")
        print("2. Modificar libro")
        print("3. Eliminar libro")
        print("4. Buscar libro")
        print("5. Ver inventario de libros")
        print("6. Ver autores registrados") #usa set y comprension de listas
        print("7. Crear prestamo")
        print("8. Cerrar prestamo")
        print("9. Consultar prestamos")
        print("10. Salir")

        opcion = input(Fore.YELLOW + "ingrese opcion: " + Fore.RESET)
        match opcion:
            case "1": id_libro_auto = crud_libros.add_libro(ARCH_LIBROS, id_libro_auto)
            case "2": crud_libros.modificar_libro(ARCH_LIBROS)
            case "3": crud_libros.eliminar_libro(ARCH_LIBROS)
            case "4": crud_libros.buscar_libro(ARCH_LIBROS)
            case "5": crud_libros.imprimir_libros(ARCH_LIBROS)
            case "6": crud_libros.mostrar_autores(ARCH_LIBROS)
            case "7": id_prestamo_auto = crud_prestamos.crear_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS, id_prestamo_auto)
            case "8": crud_prestamos.eliminar_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS)
            case "9": crud_prestamos.imprimir_prestamos(ARCH_PRESTAMOS, ARCH_LIBROS)
            case "10":
                print(Fore.YELLOW + "Saliendo")
                seguir = False
            case _: print(Fore.RED + "Opcion invalida")
                
    elif rol_usuario == "cliente":
        print(Fore.CYAN + Style.BRIGHT + "\n=== MENU CLIENTE ===")
        print("1. Solicitar prestamo")
        print("2. Devolver prestamo")
        print("3. Buscar libros")
        print("4. Ver lista completa de libros")
        print("5. Salir")
        
        opcion = input(Fore.YELLOW + "Ingrese opcion: " + Fore.RESET)
        match opcion:
            case "1": id_prestamo_auto = crud_prestamos.crear_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS, id_prestamo_auto)
            case "2": crud_prestamos.eliminar_prestamo(ARCH_LIBROS, ARCH_PRESTAMOS)
            case "3": crud_libros.buscar_libro(ARCH_LIBROS)
            case "4": crud_libros.imprimir_libros(ARCH_LIBROS)
            case "5":
                print(Fore.YELLOW + "Saliendo")
                seguir = False
            case _: print(Fore.RED + "Opción invalida")