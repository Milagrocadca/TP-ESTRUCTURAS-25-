# validaciones generales que se pueden aplicar en varias clases
def validarPositivo(num):
    """
Verifica si un número es positivo (mayor o igual a cero).
Retorna True si es positivo, False en caso contrario.
"""
    return num >= 0

def validarModo(modo):
    """
Verifica si el modo de transporte ingresado es válido.
Acepta: 'automotor', 'ferroviario', 'aereo', 'maritimo', 'fluvial'.
Retorna True si es válido, False en caso contrario.
"""
    return modo.lower() in ("automotor", "ferroviario", "aereo", "maritimo", "fluvial")

def validarTipo(modo):
    """
Verifica si el tipo de transporte ingresado es válido.
Acepta: 'automotor', 'ferroviaria', 'aerea', 'maritimo', 'fluvial'.
Retorna True si es válido, False en caso contrario.
"""
    return modo.lower() in ("automotor", "ferroviaria", "aerea", "maritimo", "fluvial")






