from validaciones import *


def inputNumPositivo(titulo):
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
    modo = input("Modo transporte: ")  # Validar modo de transporte
    while not validarModo(modo):
        modo = input("Modo transporte: ")  # Validar modo de transporte

    return modo

