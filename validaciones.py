# validaciones generales que se pueden aplicar en varias clases
def validarPositivo(num):
    return num >= 0


def validarModo(modo):
    return modo.lower() in ("automotor", "ferroviario", "aereo", "maritimo", "fluvial")

def validarTipo(modo):
    return modo.lower() in ("automotor", "ferroviaria", "aerea", "maritimo", "fluvial")

# HAY QUE AGREGAR LA VALIDACION DE METODO SI ES TIMEPO O COSTO\


# update 3/6 no es necesario este archivo

