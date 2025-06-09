""" from inputs import *
import conexion
import math


class Vehiculo:
    def __init__(
        self,
        tipo: str,
        modo: str,
        velocidad: float,
        capacidad: float,
        costo_fijo: float,
        costo_km: float,
        costo_kg: float,
    ):
        
        self.tipo = tipo
        self.modo = modo
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg

    def calcular_costo_total(self, distancia, peso):
         cantidad_vehiculos = math.ceil(peso / self.capacidad)
         peso_restante = peso
         costo_total = 0

         for _ in range(cantidad_vehiculos):
             carga = min(peso_restante, self.capacidad)
             costo_vehiculo = (
                 self.costo_fijo +
                 self.costo_km * distancia +
                 self.costo_kg * carga
             )
             costo_total += costo_vehiculo
             peso_restante -= carga

         return costo_total

    def calcular_tiempo(self, distancia, velocidad_limite=None):
        
        #Tiempo en horas que tarda en recorrer un tramo.
        #Si hay velocidad límite, la respeta.
        
        velocidad_final = (
            min(self.velocidad, velocidad_limite)
            if velocidad_limite
            else self.velocidad
        )
        return (distancia / velocidad_final) * 60

    def __repr__(self):
        return f"{self.tipo} ({self.modo})"

    # GETTERS
    def get_tipo(self):
        return self.tipo

    def get_modo(self):
        return self.modo

    def get_velocidad(self):
        return self.velocidad

    def get_capacidad(self):
        return self.capacidad

    def get_costo_fijo(self):
        return self.costo_fijo

    def get_costo_km(self):
        return self.costo_km

    def get_costo_kg(self):
        return self.costo_kg

    # SETTERS de aquellas variables que pueden ser modificadas
    def set_costo_fijo(self, costo_fijo):
        self.costo_fijo = costo_fijo

    def set_costo_km(self, costo_km):
        self.costo_km = costo_km

    def set_costo_kg(self, costo_kg):
        self.costo_kg = costo_kg

    def set_calado_necesario(self, calado_necesario):
        self.calado_necesario = calado_necesario

    # RESTRICCIONES
    def puede_recorrer(self, tramo, peso):
        if tramo.get_tipo().lower() != self.modo:
            return False
        if tramo.get_peso_max() is not None and peso > tramo.get_peso_max():
            return False
        if tramo.get_vel_max() is not None and self.velocidad > tramo.get_vel_max():
            return False
        return True

class Vehiculos:
    def __init__(self):
        self.vehiculos = dict()  # Asumimos que tipo vehiculo es unico

    def addVehiculo(self):
        print("\n===== AGREGAR VEHICULO =====")
        tipo = input("Tipo vehiculo: ")  # Cualquier tipo de vehiculo
        modo = inputModo()
        #velocidad = inputNumPositivo("Velocidad: ")  # Validar velocidad numero positivo
        #capacidad = inputNumPositivo("Capacidad: ")  # Validar capacidad numero positivo
        #costo_fijo = inputNumPositivo("Costo fijo: ")  # Validar costo fijo numero positivo
        #costo_km = inputNumPositivo("Costo por km: ")  # Validar costo km numero positivo
        #costo_kg = inputNumPositivo("Costo por kg: ")  # Validar costo kg numero positivo

        self.vehiculos[tipo] = Vehiculo(
            tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
        )

    def removeVehiculo(self):
        tipo = input("Tipo vehiculo a remover: ")
        if tipo in self.vehiculos:
            self.vehiculos.pop(tipo)
        else:
            print("El tipo de vehiculo a eliminar no existe.")

    def getListVehiculos(self):
        return list(self.vehiculos)

    def getInfoVehiculos(self):
        return self.vehiculos

    def printVehiculos(self):
        print("\nVehiculo | Modo | Velocidad | Capacidad | Costo Fijo | Costo km | Costo kg")
        for tipo, vehiculo in self.vehiculos.items():
            print(
                f"{tipo} | {vehiculo.modo} | {vehiculo.velocidad} | {vehiculo.capacidad} | {vehiculo.costo_fijo} | {vehiculo.costo_km} | {vehiculo.costo_kg}"
            )


class Automotor(Vehiculo):
    def __init__(self):
        super().__init__(
            tipo="Camión",
            modo="automotor",
            velocidad=80,
            capacidad=30000,
            costo_fijo=30,
            costo_km=5,
            costo_kg=0,
        )

    def calcular_costo_total(self, distancia, peso):
        cantidad_vehiculos = math.ceil(peso / self.capacidad)
        peso_restante = peso
        costo_total = 0

        for _ in range(cantidad_vehiculos):
            carga = min(peso_restante, self.capacidad)
            costo_kg = 1 if carga < 15000 else 2
            costo_vehiculo = (
                self.costo_fijo +
                self.costo_km * distancia +
                costo_kg * carga
            )
            costo_total += costo_vehiculo
            peso_restante -= carga

        return costo_total

class Tren(Vehiculo):
    def __init__(self):
        super().__init__(
            tipo="Tren de Carga",
            modo="ferroviario",
            velocidad=100,
            capacidad=150000,
            costo_fijo=100,
            costo_km=0,
            costo_kg=3,
        )

    def calcular_costo_total(self, distancia, peso):
        cantidad_vehiculos = math.ceil(peso / self.capacidad)
        peso_restante = peso
        costo_total = 0

        for _ in range(cantidad_vehiculos):
            carga = min(peso_restante, self.capacidad)
            costo_km = 20 if distancia < 200 else 15
            costo_vehiculo = (
                self.costo_fijo +
                costo_km * distancia +
                self.costo_kg * carga
            )
            costo_total += costo_vehiculo
            peso_restante -= carga

        return costo_total

class Aereo(Vehiculo):
    def __init__(self, conexion: conexion):
        velocidad = 400 if conexion.get_mal_clima() else 600
        super().__init__(
            tipo="Avión",
            modo="aereo",
            velocidad=velocidad,
            capacidad=5000,
            costo_fijo=750,
            costo_km=40,
            costo_kg=10,
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
            costo_kg=2,
        )
        self.tipo_agua = tipo_agua
        self.calado_necesario = calado_necesario """