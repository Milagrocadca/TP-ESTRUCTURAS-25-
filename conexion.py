from random import random
class Conexion:
    '''Representa una conexión entre dos nodos (ciudades) mediante un tipo de transporte.
    Guarda información sobre el origen, destino, tipo de transporte, distancia y posibles restricciones 
    '''

    def __init__(self, origen, destino, tipo, distancia_km, restriccion=None, valor_restriccion=None):
        self.restricciones = {}  

        if not Conexion.validarTipo(tipo):
            raise ValueError("El tipo del tramo solo puede ser Ferroviaria, Automotor, Fluvial, Aerea")
        if tipo.lower() == "ferroviaria":
            tipo = "ferroviario"
        elif tipo.lower() == "aerea":
            tipo = "aereo"
        self.origen = origen
        self.destino = destino
        self.tipo = tipo  # Ej: "Ferroviaria", "Automotor", "Fluvial", "Aerea"
        
        try:
            self.distancia = float(distancia_km)
        except (ValueError, TypeError):
            raise ValueError(f"Distancia inválida: {distancia_km}")

        if restriccion:
            self.restricciones[restriccion] = valor_restriccion

    @staticmethod   
    def validarTipo(modo):
        """
        Verifica si el tipo de transporte ingresado es válido.
        Acepta: 'automotor', 'ferroviaria', 'aerea', 'maritimo', 'fluvial'.
        Retorna True si es válido, False en caso contrario.
        """
        return modo.lower() in ("automotor", "ferroviaria", "aerea", "maritimo", "fluvial")

    #GETTER    
    def get_tipo(self):
        return self.tipo
    def get_destino(self):
        return self.destino
    def get_distancia(self):
        return self.distancia

    def get_mal_clima(self):
        if self.tipo == "aereo" and "prob_mal_tiempo" in self.restricciones:
            try:
                return random() < float(self.restricciones["prob_mal_tiempo"])
            except (ValueError, TypeError):
                return False
        return False
    
    def __eq__(self, other):
        if not isinstance(other, Conexion):
            return False
        return self.origen == other.origen and self.destino == other.destino and self.tipo == other.tipo

    def __str__(self):
        return (f"Conexion({self.origen} → {self.destino}, tipo={self.tipo}, distancia={self.distancia}km, "
                f"restricciones={self.restricciones}")