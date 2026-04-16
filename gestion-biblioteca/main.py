import colorama
import crud_books
import crud_users
import crud_loans
import stats as estadisticas

def mostrar_menu():     #Mostrar el menu principal, colorama para que quede flama. Tupla de strings y joins para el print, queda joya
    print("\n" * 50)
    menu_items = (
        f"{colorama.Fore.GREEN}====================================================",
        "           Sistema de gestion de bibliotecas 3000X           ",
        "====================================================",
        f"{colorama.Fore.GREEN}--- Gestión de usuarios ---",
        f"{colorama.Fore.WHITE}1 - Registrar usuario",
        f"{colorama.Fore.WHITE}2 - Eliminar usuario",
        f"{colorama.Fore.WHITE}3 - Ver todos los usuarios",
        f"{colorama.Fore.GREEN}--- Gestión de libros ---",
        f"{colorama.Fore.WHITE}4 - Registrar libro",
        f"{colorama.Fore.WHITE}5 - Eliminar libro",
        f"{colorama.Fore.WHITE}6 - Ver todos los libros",
        f"{colorama.Fore.GREEN}--- Gestión de prestamos ---",
        f"{colorama.Fore.WHITE}7 - Registrar prestamo",
        f"{colorama.Fore.WHITE}8 - Registrar devolucion (modificar prestamo)",
        f"{colorama.Fore.WHITE}9 - Ver prestamos activos",
        f"{colorama.Fore.WHITE}10 - Ver historial de prestamos",
        f"{colorama.Fore.GREEN}--- Estadisticas ---",
        f"{colorama.Fore.WHITE}11 - Ver Estadisticas",
        f"{colorama.Fore.YELLOW}--- Salida ---",
        f"{colorama.Fore.LIGHTBLUE_EX}12 - Salir",
        f"{colorama.Fore.GREEN}===================================================="
    )
    print("\n".join(menu_items))

def ejecutar_programa(): #Ejecuta el loop del menu para mostrar las opciones durante la navegacion
    colorama.init(autoreset = True)
    opciones = {     #Diccionario para mappear funciones a opciones del menu y lambbdas para funciones con argumentos especificos, me dio fiaca usar IF/ELSE
        "1": crud_users.registrar_usuario,
        "2": crud_users.eliminar_usuario,
        "3": crud_users.ver_usuarios,
        "4": crud_books.registrar_libro,
        "5": crud_books.eliminar_libro,
        "6": crud_books.ver_libros,
        "7": crud_loans.registrar_prestamo,
        "8": crud_loans.modificar_prestamo,
        "9": lambda: crud_loans.ver_prestamos(solo_activos = True),
        "10": lambda: crud_loans.ver_prestamos(solo_activos = False),
        "11": estadisticas.mostrar_estadisticas,
    }

    terminar = False #Para controlar la salida del loop
    while not terminar:
        mostrar_menu()
        opcion = input("Elija una opcion: ").strip()

        if opcion == "12":
            terminar = True
        else:
            funcion_a_ejecutar = opciones.get(opcion) #.get para buscar opciones, None si no existe la opcion
            if funcion_a_ejecutar:
                try:
                    funcion_a_ejecutar()
                except (ValueError, KeyError) as data_err: #agarro los errores especificos
                    print(f"{colorama.Fore.RED}Error de datos: {data_err}")
                    print(f"{colorama.Fore.YELLOW}Por favor, revise la integridad de los archivos .json y .txt.")
                except Exception as e: #esto es por si se me pasó algo por alto
                    print(f"{colorama.Fore.RED}Hubo un error inesperado durante la operación: {e}")
            else:
                print(f"{colorama.Fore.RED}Opción invalida, proba de nuevo")
            input(f"\n{colorama.Fore.WHITE}--- Continuar --- (Enter)")
    print(f"\n{colorama.Fore.MAGENTA}Chau loco")

if __name__ == "__main__":
    ejecutar_programa()