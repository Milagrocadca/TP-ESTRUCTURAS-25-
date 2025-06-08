from validaciones import *


def inputNumPositivo(titulo):
    flag = True
    while flag:
        try:
            val = float(input(titulo))
            if validarPositivo(val):
                flag = False
            else:
                print(
                    "\t El valor ingresado debe ser un numero positivo. Intente nuevamente"
                )
        except ValueError:
            print(
                "\t Error! El valor ingresado debe ser un numero positivo. Intente nuevamente"
            )
    return val


def inputModo():
    modo = input("\t >Modo transporte: ")  # Validar modo de transporte
    while not validarModo(modo):
        modo = input("\t >Modo transporte: ")  # Validar modo de transporte

    return modo

