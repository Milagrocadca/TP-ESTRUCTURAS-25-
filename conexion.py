from random import random
from validaciones import *
class Conexion:
    '''Representa una conexión entre dos nodos (ciudades) mediante un tipo de transporte.
    Guarda información sobre el origen, destino, tipo de transporte, distancia y posibles restricciones 
    '''

    def __init__(self, origen, destino, tipo, distancia_km, restriccion=None, valor_restriccion=None):
        
        #if not validarTipo(tipo):
        #    raise ValueError ("El tipo del tramo solo puede ser Ferroviaria, Automotor, Fluvial, Aerea")
        if tipo.lower()=="ferroviaria":
            tipo="ferroviario"
        elif  tipo.lower()=="aerea":
            tipo="aereo"
        self.origen = origen
        self.destino = destino
        self.tipo = tipo  # Ej: "Ferroviaria", "Automotor", "Fluvial", "Aerea"
        self.distancia = float(distancia_km)
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion

        #RESTRICCIONES
        self.vel_max = float(valor_restriccion) if restriccion == "velocidad_max" else None
        self.peso_max = float(valor_restriccion) if restriccion == "peso_max" else None
        self.tipo_agua = valor_restriccion if restriccion == "tipo" else None
        self.prob_mal_tiempo = float(valor_restriccion) if restriccion == "prob_mal_tiempo" else None
        
        


    #GETTER
    def get_origen(self):
        return self.origen

    def get_destino(self):
        return self.destino

    def get_tipo(self):
        return self.tipo

    def get_distancia(self):
        return self.distancia

    def get_restriccion(self):
        return self.restriccion

    def get_valor_restriccion(self):
        return self.valor_restriccion

    def get_vel_max(self):
        return self.vel_max

    def get_peso_max(self):
        return self.peso_max

    def get_tipo_agua(self):
        return self.tipo_agua

    def get_prob_mal_tiempo(self):
        return self.prob_mal_tiempo

  
    def get_mal_clima(self):
        if self.tipo=="aerea":
            numero = random()
            if numero < self.prob_mal_tiempo:
                return True
            else:
                return False   #retorna False si hay buen clima

    #SIN SETTER ya que estan cargados desde un archivo

    def __eq__(self, other):
        if not isinstance(other, Conexion):
            return False
        return self.origen == other.origen and self.destino == other.destino and self.tipo == other.tipo

    def __str__(self):
        return (f"Conexion({self.origen} → {self.destino}, tipo={self.tipo}, distancia={self.distancia}km, "
                f"restriccion={self.restriccion}, valor={self.valor_restriccion})")