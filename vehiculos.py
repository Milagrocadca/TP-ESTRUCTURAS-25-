from inputs import *
import conexion


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
        """
        Costo de usar este vehículo en un tramo, sin multiplicar por cantidad de vehículos.
        """
        return self.costo_fijo + self.costo_km * distancia + self.costo_kg * peso

    def calcular_tiempo(self, distancia, velocidad_limite=None):
        """
        Tiempo en horas que tarda en recorrer un tramo.
        Si hay velocidad límite, la respeta.
        """
        v = (
            min(self.velocidad, velocidad_limite)
            if velocidad_limite
            else self.velocidad
        )
        return distancia / v

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
        print("\t\n===== AGREGAR VEHICULO =====")
        tipo = input("\t >Tipo vehiculo: ")  # Cualquier tipo de vehiculo
        modo = inputModo()
        velocidad = inputNumPositivo(
            "\t >Velocidad: "
        )  # Validar velocidad numero positivo
        capacidad = inputNumPositivo(
            "\t >Capacidad: "
        )  # Validar capacidad numero positivo
        costo_fijo = inputNumPositivo(
            "\t >Costo fijo: "
        )  # Validar costo fijo numero positivo
        costo_km = inputNumPositivo(
            "\t >Costo por km: "
        )  # Validar costo km numero positivo
        costo_kg = inputNumPositivo(
            "\t >Costo por kg: "
        )  # Validar costo kg numero positivo

        self.vehiculos[tipo] = Vehiculo(
            tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
        )

    def removeVehiculo(self):
        tipo = input("\t >Tipo vehiculo a remover: ")
        if tipo in self.vehiculos:
            self.vehiculos.pop(tipo)
        else:
            print("El tipo de vehiculo a eliminar no existe.")

    def getListVehiculos(self):
        return list(self.vehiculos)

    def getInfoVehiculos(self):
        return self.vehiculos

    def printVehiculos(self):
        print(
            f"\n{'Vehiculo':<15}|{'Modo':<15}|{'Velocidad':<15}|{'Capacidad':<15}|{'Costo Fijo':<15}|{'Costo km':<15}|{'Costo kg':<15}"
        )
        vehiculos: Vehiculos = self.vehiculos
        for tipo in vehiculos.keys():
            vehiculo: Vehiculo = vehiculos[tipo]
            modo = vehiculo.modo
            velocidad = vehiculo.velocidad
            capacidad = vehiculo.capacidad
            costo_fijo = vehiculo.costo_fijo
            costo_km = vehiculo.costo_km
            costo_kg = vehiculo.costo_kg
            print(
                f"{tipo:<15}|{modo:<15}|{velocidad:<15}|{capacidad:<15}|{costo_fijo:<15}|{costo_km:<15}|{costo_kg:<15}"
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
            costo_kg=3,
        )

    def calcular_costo_total(self, distancia, peso):
        costo_km = 20 if distancia < 200 else 15
        return self.costo_fijo + costo_km * distancia + self.costo_kg * peso


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
        self.calado_necesario = calado_necesario
