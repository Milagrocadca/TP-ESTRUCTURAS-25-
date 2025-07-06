from conexion import Conexion

class Nodo:
    """
    Representa una ciudad o punto en el grafo, con sus modos de transporte habilitados y conexiones salientes
    """
    
    def __init__(self, nombre, modos):
        #nombre= Nombre de la ciudad
        #modos= modos de transporte habilitados (list o set) 
        self.nombre = nombre
        self.modos = set(modos)
        self.conexiones = [] 

    
    def agregar_conexion(self, conexion):
        if not isinstance(conexion, Conexion):
            raise TypeError("El objeto agregado debe ser una instancia de Conexion")
        self.conexiones.append(conexion)
    
    
    def tiene_modo(self, modo):
        """
    Verifica si el nodo tiene habilitado el modo de transporte especificado.
    Retorna True si el modo está habilitado, False en caso contrario.
    """
        return modo in self.modos

    def __repr__(self):
         return f"Nodo({self.nombre}, modos={self.modos})"
