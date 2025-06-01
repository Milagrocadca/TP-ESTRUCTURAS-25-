from validaciones import *

class Vehiculo:
    def __init__(self, tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg):
        if not Vehiculo.validarModo(modo):
            raise ValueError("El modo del vehiculo ingresado no se encentra dentro de las opciones disponibles")
        elif not validarPositivo(velocidad):
            raise ValueError("El valor de la velocidad debe ser un numero positivo") 
        elif not validarPositivo(capacidad):
            raise ValueError("El valor de la capacidad debe ser un numero positivo") 
        elif not validarPositivo(costo_fijo):
            raise ValueError("El valor del costo fijo debe ser un numero positivo") 
        elif not validarPositivo(costo_kg):
            raise ValueError("El valor del costo por kg debe ser un numero positivo") 
        elif not validarPositivo(costo_km):
            raise ValueError("El valor del costo por km debe ser un numero positivo") 

        self.tipo = tipo        
        self.modo = modo
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg

    @staticmethod 
    def validarModo(modo):
        lista_modos = ('automotor', 'ferroviario', 'aereo', 'maritimo')
        return modo in lista_modos

    def calcular_costo_total(self, distancia, peso):
        """
        Costo de usar este vehículo en un tramo, sin multiplicar por cantidad de vehículos.
        """
        return self.costo_fijo + self.costo_km * distancia + self.costo_kg * peso

    def calcular_tiempo(self, distancia, velocidad_limite=None):
        """
        Tiempo en horas que tarda en recorrer un tramo.
        Si hay velocidad límite, la respeta.
        """
        v = min(self.velocidad, velocidad_limite) if velocidad_limite else self.velocidad
        return distancia / v

    def __repr__(self):
        return f"{self.tipo} ({self.modo})"

    # GETTERS
    def get_tipo(self): return self.tipo
    def get_modo(self): return self.modo
    def get_velocidad(self): return self.velocidad
    def get_capacidad(self): return self.capacidad
    def get_costo_fijo(self): return self.costo_fijo
    def get_costo_km(self): return self.costo_km
    def get_costo_kg(self): return self.costo_kg

    # SETTERS
    def set_tipo(self, tipo): self.tipo = tipo
    def set_modo(self, modo): self.modo = modo
    def set_velocidad(self, velocidad): self.velocidad = velocidad
    def set_capacidad(self, capacidad): self.capacidad = capacidad
    def set_costo_fijo(self, costo_fijo): self.costo_fijo = costo_fijo
    def set_costo_km(self, costo_km): self.costo_km = costo_km
    def set_costo_kg(self, costo_kg): self.costo_kg = costo_kg
    def set_calado_necesario(self, calado_necesario): 
        self.calado_necesario = calado_necesario

    # RESTRICCIONES
    def puede_recorrer(self, tramo, peso):
        if tramo.get_modo() != self.modo:
            return False
        if tramo.get_peso_max() is not None and peso > tramo.get_peso_max():
            return False
        if tramo.get_vel_max() is not None and self.velocidad > tramo.get_vel_max():
            return False
        return True

class Automotor(Vehiculo):
    def __init__(self):
        super().__init__(
            tipo="Camión",
            modo="automotor",
            velocidad=80,
            capacidad=30000,
            costo_fijo=30,
            costo_km=5,
            costo_kg=0  
        )

    def calcular_costo_total(self, distancia, peso):
        costo_kg = 1 if peso < 15000 else 2
        return self.costo_fijo + self.costo_km * distancia + costo_kg * peso

class Tren(Vehiculo):
    def __init__(self):
        super().__init__(
            tipo="Tren de Carga",
            modo="ferroviario",
            velocidad=100,
            capacidad=150000,
            costo_fijo=100,
            costo_km=0, 
            costo_kg=3
        )

    def calcular_costo_total(self, distancia, peso):
        costo_km = 20 if distancia < 200 else 15
        return self.costo_fijo + costo_km * distancia + self.costo_kg * peso

class Aereo(Vehiculo):
    def __init__(self, mal_tiempo=False):
        velocidad = 400 if mal_tiempo else 600
        super().__init__(
            tipo="Avión",
            modo="aereo",
            velocidad=velocidad,
            capacidad=5000,
            costo_fijo=750,
            costo_km=40,
            costo_kg=10
        )

class Maritimo(Vehiculo):
    def __init__(self, tipo_agua, calado_necesario=None):
        costo_fijo = 500 if tipo_agua == "fluvial" else 1500
        super().__init__(
            tipo=f"Barco ({tipo_agua})",
            modo="maritimo",
            velocidad=40,
            capacidad=100000,
            costo_fijo=costo_fijo,
            costo_km=15,
            costo_kg=2
        )
        self.tipo_agua = tipo_agua
        self.calado_necesario = calado_necesario
