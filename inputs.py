from validaciones import *


def inputNumPositivo(titulo):
    """
    Solicita al usuario que ingrese un número positivo.
    Muestra el mensaje 'titulo', valida que la entrada sea un número positivo
    y repite la solicitud hasta que el usuario ingrese un valor válido.
    Retorna el número positivo ingresado.
    """
    seguir= True
    while seguir:
        try:
            valor = float(input(titulo))
            if validarPositivo(valor):
                seguir = False
            else:
                print("El valor ingresado debe ser un numero positivo. Intente nuevamente")
        except ValueError:
            print("El valor ingresado debe ser un numero positivo. Intente nuevamente")
    return valor


def inputModo():
    """
    Solicita al usuario que ingrese un modo de transporte válido.
    Repite la solicitud hasta que el usuario ingrese un modo aceptado por validarModo.
    Retorna el modo de transporte válido ingresado.
    """
    modo = input("Modo transporte: ")  # Validar modo de transporte
    while not validarModo(modo):
        modo = input("Modo transporte: ")  # Validar modo de transporte

    return modo

