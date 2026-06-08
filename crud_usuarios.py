import json

def iniciar_sesion(arch_usuarios, usuario, contrasenia):
    """
    chequea credenciales leyendo el json de usuarios, devuelve el rol o un error
    """
    try:
        arch = open(arch_usuarios, "rt")
        for linea in arch:
            user_data = json.loads(linea)
            if user_data["usuario"] == usuario:
                if user_data["clave"] == contrasenia:
                    return user_data["rol"]
                else:
                    return "CLAVE_INCORRECTA"
        return "USUARIO_INEXISTENTE"
    except FileNotFoundError:
        return "ARCHIVO_NO_ENCONTRADO"
    finally:
        try: 
            arch.close()
        except NameError: 
            pass