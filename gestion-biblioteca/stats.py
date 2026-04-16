import gestion_datos
import utils as utilidades
from datetime import datetime

def calcular_libro_mas_prestado():
    prestamos = gestion_datos.cargar_prestamos()
    libros = gestion_datos.cargar_libros()
    
    #si hay prestamos que tienen 2 libros se agregan los dos 
    todos_los_libros_prestados = []
    for p in prestamos:
        todos_los_libros_prestados.extend(p['ID_Libros'].split(','))
        
    if not todos_los_libros_prestados:
        return None, 0

    conteo_libros = contador_de_happens(todos_los_libros_prestados, {}) #diccionario vacio como contador
    id_mas_prestado = max(conteo_libros, key = conteo_libros.get) #contar la cantidad de veces que aparece un libro
    conteo_maximo = conteo_libros[id_mas_prestado]
    
    info_libro = next(filter(lambda l: l['ID_Libro'] == id_mas_prestado, libros), None) #filtro los datos del libro
    
    return info_libro, conteo_maximo

def calcular_usuario_mas_activo():
    prestamos = gestion_datos.cargar_prestamos()
    usuarios = gestion_datos.cargar_usuarios()
    
    if not prestamos:
        return None, 0

    ids_usuarios_prestamos = list(map(lambda p: p['ID_Usuario'], prestamos)) #saco ids de usuario
    conteo_usuarios = {}
    for id_usuario in ids_usuarios_prestamos: #contar la cantidad de veces que aparece un user
        conteo_usuarios[id_usuario] = conteo_usuarios.get(id_usuario, 0) + 1
        
    id_mas_activo = max(conteo_usuarios, key = conteo_usuarios.get)
    conteo_maximo = conteo_usuarios[id_mas_activo]
    info_usuario = next(filter(lambda u: u['ID_Usuario'] == id_mas_activo, usuarios), None)
    
    return info_usuario, conteo_maximo

def contador_de_happens(lista_de_ids, happens_actual):
    if not lista_de_ids:
        return happens_actual #no hay ocurrencias de ids
    id_actual = lista_de_ids[0] 
    
    happens_actual[id_actual] = happens_actual.get(id_actual, 0) + 1 #llama a la funcion de conteo con la lista y el diccionario actualizados
    return contador_de_happens(lista_de_ids[1:], happens_actual)


def calcular_promedios_devolucion():
    prestamos = gestion_datos.cargar_prestamos()
    
    prestamos_devueltos = list(filter(lambda p: p['Estado_Prestamo'] == 'Devuelto', prestamos)) #Calcular solo los prestamos con devolucion
    
    if not prestamos_devueltos:
        return 0, 0 #devuelvo 0 de promedio si no hay devoluciones

    tardias = 0
    a_tiempo = 0
    
    for p in prestamos_devueltos:
        try:
            # paso string a datetime para comparar
            fecha_prevista = datetime.strptime(p['Fecha_Devolucion_Prevista'], '%d/%m/%Y')
            fecha_real = datetime.strptime(p['Fecha_Devolucion_Real'], '%d/%m/%Y')
            
            if fecha_real > fecha_prevista:
                tardias = tardias + 1
            else:
                a_tiempo = a_tiempo + 1
        except (ValueError, TypeError):
            # esto ignora prestamos que tengan "Null" en fecha de devolucion o format roto
            print(f"Advertencia: Formato de fecha invalido para {p['ID_Prestamo']}, se ignora el prestamo.")
    
    total_devoluciones = len(prestamos_devueltos)
    promedio_a_tiempo = (a_tiempo / total_devoluciones) * 100
    promedio_tardias = (tardias / total_devoluciones) * 100
    
    return promedio_a_tiempo, promedio_tardias

def mostrar_estadisticas():
    print("\n--- Estadisticas ---")

    libro, conteo_libro = calcular_libro_mas_prestado()
    if libro:
        print(f"El libro mas prestado es: '{libro['Titulo']}' por {libro['Autor']} Prestamos: {conteo_libro}.")
    else:
        utilidades.imprimir_advertencia("No hay datos de prestamos de libros")

    usuario, conteo_usuario = calcular_usuario_mas_activo()
    if usuario:
        print(f"El usuario que mas prestamos obtiene es: {usuario['Nombre']} {usuario['Apellido']} Cantidad: {conteo_usuario}.")
    else:
        utilidades.imprimir_advertencia("No hay datos de prestamos de usuarios.")

    prom_a_tiempo, prom_tardias = calcular_promedios_devolucion()
    if prom_a_tiempo > 0 or prom_tardias > 0:
        print(f"Promedio de devoluciones a tiempo: {prom_a_tiempo:.2f}%")
        print(f"Promedio de devoluciones tardías: {prom_tardias:.2f}%")
    else:
        utilidades.imprimir_advertencia("No hay datos de devoluciones para calcular las estadisticas de prestamos.")