import gestion_datos
import utils as utilidades

def registrar_prestamo():
    print("\n--- Registrar nuevo préstamo ---")
    id_usuario = input("Ingrese el ID del usuario (ej. U001): ").strip().upper()
    
    if utilidades.validar_id(id_usuario, 'usuario'):
        ids_libro_str = input("Ingrese los IDs de los libros a prestar (separados por comas, ej. L001,L002): ").strip().upper()
        ids_libros_list = ids_libro_str.replace(' ', '').split(',')
        
        libros = gestion_datos.cargar_libros()
        usuarios = gestion_datos.cargar_usuarios()
        
        if any(u['ID_Usuario'] == id_usuario for u in usuarios):
            libros_a_prestar = []
            error_encontrado = False
            
            for id_l in ids_libros_list:
                if not error_encontrado:
                    libro_encontrado = next(filter(lambda l: l['ID_Libro'] == id_l, libros), None) #Busca el libro por ID, None si no lo encuentra
                    if libro_encontrado is None:
                        utilidades.imprimir_error(f"El libro con ID {id_l} no existe.")
                        error_encontrado = True
                    elif libro_encontrado['Estado'] != 'Disponible':
                        utilidades.imprimir_error(f"El libro con ID {id_l} no está disponible para préstamo.")
                        error_encontrado = True
                    else:
                        libros_a_prestar.append(libro_encontrado)
            
            if not error_encontrado:
                #Crear prestamo
                prestamos = gestion_datos.cargar_prestamos()
                nuevo_id_prestamo = utilidades.generar_nuevo_id(prestamos, 'P')
                nuevo_prestamo = {
                    "ID_Prestamo": nuevo_id_prestamo,
                    "ID_Usuario": id_usuario,
                    "ID_Libros": ",".join(ids_libros_list),
                    "Fecha_Prestamo": utilidades.obtener_fecha_actual_str(),
                    "Fecha_Devolucion_Prevista": utilidades.calcular_fecha_devolucion_str(),
                    "Fecha_Devolucion_Real": "null", "Estado_Prestamo": "Activo"
                }
                prestamos.append(nuevo_prestamo)
                for libro_obj in libros_a_prestar:
                    libro_obj['Estado'] = 'Prestado'
                
                try: #separé los errores para que sea mas facil saber que se rompe
                    if not gestion_datos.guardar_prestamos(prestamos):
                        raise Exception("Error al guardar el nuevo préstamo.")
                    
                    if not gestion_datos.guardar_libros(libros):
                        raise Exception("Error al actualizar el estado de los libros.")

                    utilidades.imprimir_exito(f"Prestamo {nuevo_id_prestamo} registrado con éxito.")

                except Exception as e: 
                    utilidades.imprimir_error(f"No se pudo completar el registro del préstamo: {e}")
                    utilidades.imprimir_advertencia("Los datos pueden haberse cargado mal, revisa los archivos.")
            
def modificar_prestamo():
    #Modifica prestamos para registrar devoluciones
    print("\n--- Modificar prestamo ---")
    id_prestamo = input("Ingrees el ID del prestamo a modificar (ej. P001): ").strip().upper()
    if utilidades.validar_id(id_prestamo, 'prestamo'):
        prestamos = gestion_datos.cargar_prestamos()
        libros = gestion_datos.cargar_libros()
        
        prestamo_a_cambiar = buscaprestamos_recursivo(prestamos, id_prestamo)
        
        if prestamo_a_cambiar:
            if prestamo_a_cambiar['Estado_Prestamo'] != 'Devuelto':
                #Actualizar prestamo, liros
                prestamo_a_cambiar['Estado_Prestamo'] = 'Devuelto'
                prestamo_a_cambiar['Fecha_Devolucion_Real'] = utilidades.obtener_fecha_actual_str()
                ids_libros_devueltos = prestamo_a_cambiar['ID_Libros'].split(',')
                for id_l in ids_libros_devueltos:
                    libro_obj = next(filter(lambda l: l['ID_Libro'] == id_l, libros), None)
                    if libro_obj:
                        libro_obj['Estado'] = 'Disponible'
                try:
                    if not gestion_datos.guardar_prestamos(prestamos):
                        raise Exception("Error al actualizar el archivo de préstamos.")
                    
                    if not gestion_datos.guardar_libros(libros):
                        raise Exception("Error al actualizar el estado de los libros devueltos.")

                    utilidades.imprimir_exito(f"Devolución para el prestamo {id_prestamo} registrada con éxito.")
                except Exception as e: #lo mismo que arriba, para separar los errores
                    utilidades.imprimir_error(f"No se pudo registrar la devolución: {e}")
                    utilidades.imprimir_advertencia("Revisa los archivos para confirmar que no se haya roto nada.")
            else:
                utilidades.imprimir_advertencia("Este préstamo ya ha sido devuelto.")
        else:
            utilidades.imprimir_error(f"No se encontró un préstamo con el ID {id_prestamo}.")
    else:
        utilidades.imprimir_error(f"El ID de prestamo {id_prestamo} es inválido.")
        
def buscaprestamos_recursivo(lista_prestamos, id_buscar):
    if not lista_prestamos: #lista vacia, gil, para que buscas?
        return None
    
    prestamo_buscado = lista_prestamos[0]
    if prestamo_buscado['ID_Prestamo'] == id_buscar: #si se encuentra en el primer elemento
        return prestamo_buscado
    else: #mala suerte y a seguir buscando
        return buscaprestamos_recursivo(lista_prestamos[1:], id_buscar)
    
def ver_prestamos(solo_activos = False):
    #Mostrar prestamos en su totalidad, ordenados por estado.
    titulo = "Prestamos Activos" if solo_activos else "Historial de Prestamos"
    print(f"\n--- {titulo} ---")
    prestamos = gestion_datos.cargar_prestamos()
    
    lista_a_procesar = prestamos
    if solo_activos:
        lista_a_procesar = list(filter(lambda p: p['Estado_Prestamo'] == 'Activo', prestamos))

    if not lista_a_procesar:
        utilidades.imprimir_advertencia("No hay préstamos para mostrar.")
    else:
        lista_a_mostrar = sorted(lista_a_procesar, key=lambda p: p['Estado_Prestamo']) #Prestamos activos se muestran antes que los demás cuando se ven todos los prestamos.
        print(f"{'ID Préstamo':<12} | {'ID Usuario':<12} | {'IDs Libros':<20} | {'Estado':<10} | {'F. Préstamo':<15} | {'F. Prevista':<15}")
        print("-" * 95)
        for p in lista_a_mostrar:
            print(f"{p.get('ID_Prestamo', ''):<12} | {p.get('ID_Usuario', ''):<12} | {p.get('ID_Libros', ''):<20} | {p.get('Estado_Prestamo', ''):<10} | {p.get('Fecha_Prestamo', ''):<15} | {p.get('Fecha_Devolucion_Prevista', ''):<15}")
            
def ver_prestamos_activos():
    ver_prestamos(solo_activos = True) #Para mostrar los prestamos activos solamente

def ver_historial_prestamos():
    ver_prestamos(solo_activos = False) #Para mostrar TODOS los prestamos en el historial