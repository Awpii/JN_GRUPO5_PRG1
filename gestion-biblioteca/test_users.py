import pytest
USUARIOS_EXISTENTES =[
    {
        "ID_Usuario": "U001",
        "Email": "maria.gonzalez@email.com"
    },
    {
        "ID_Usuario": "U002",
        "Email": "ana.martinez@email.com",
    },
    {
        "ID_Usuario": "U003",
        "Email": "laura.fernandez@email.com"
    },
    {
        "ID_Usuario": "U004",
        "Email": "carlos.rodriguez@email.com"
    },
    {
        "ID_Usuario": "U005",
        "Email": "juan.perez@email.com"
    }
]

def test_email_duplicado():
    """Verifica que el loop encuentre un email ya existente."""
    
    email_a_verificar = "maria.gnzalez@email.com"
    encontrado = False #Flag
    
    for usuario in USUARIOS_EXISTENTES:
        if usuario['Email'] == email_a_verificar:
            encontrado = True
            break # Si lo encuentro, salgo del loop
    
    # Aserción: Esperamos que la bandera sea True
    assert encontrado == True