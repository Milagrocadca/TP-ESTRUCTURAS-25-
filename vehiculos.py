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
        costo_total = 0

        # Sumar costo fijo y por km por cada vehículo
        for _ in range(cantidad_vehiculos):
            costo_total += self.costo_fijo + self.costo_km * distancia

        return costo_total

    def calcular_tiempo(self, distancia, velocidad_limite=None):
        """
        Tiempo en minutos que tarda en recorrer un tramo.
        Si hay velocidad límite, la respeta.
        """
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
    def puede_recorrer(self, tramo):
        """
    Verifica si el vehículo puede recorrer el tramo dado, comparando el modo de transporte
    y otras posibles restricciones.
    """
        if tramo.get_tipo().lower() != self.modo:
            return False
        
        return True

class Vehiculos:
    def __init__(self):
        self.vehiculos = dict()  # tipo de vehiculo es único

    def addVehiculo(self, opcion):
        if opcion == "a":
            self.vehiculos["Camión"] = Automotor()
        elif opcion == "b":
            self.vehiculos["Tren de Carga"] = Tren()
        elif opcion == "c":
            self.vehiculos["Avión"] = Aereo(None)
        elif opcion == "d":
            self.vehiculos["Barco (fluvial)"] = Maritimo("fluvial")
        elif opcion == "e":
            self.vehiculos["Barco (maritimo)"] = Maritimo("maritimo")
        else:
            raise ValueError("Opción no reconocida.")

    def removeVehiculo(self, opcion):
        tipos = {
            "a": "Camión",
            "b": "Tren de Carga",
            "c": "Avión",
            "d": "Barco (fluvial)",
            "e": "Barco (maritimo)"
        }
        tipo = tipos.get(opcion)
        if tipo and tipo in self.vehiculos:
            self.vehiculos.pop(tipo)
            return True
        else:
            return False

    def getListVehiculos(self):
        return list(self.vehiculos.values())

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
        """
    Calcula el costo total de recorrer un tramo de una distancia dada con un peso dado.
    Suma el costo fijo y el costo por km por cada vehículo necesario para transportar la carga.
    (En Automotor, también retorna el costo por kg según la carga.)
    """
        cantidad_vehiculos = math.ceil(peso / self.capacidad)
        costo_total = 0

        # Sumar costo fijo y por km por cada vehículo
        for _ in range(cantidad_vehiculos):
            costo_total += self.costo_fijo + self.costo_km * distancia

        # Costo por kg depende del peso total
        costo_kg = 1 if peso < 15000 else 2

        return costo_total,costo_kg
    def calcular_costo_kg_automotor(vehiculo, peso_total):
        """
    (Solo Automotor) Calcula el costo total por kg para camiones, considerando que cada camión
    puede llevar diferente carga y tener diferente costo por kg según la cantidad transportada.
    """
        capacidad = vehiculo.get_capacidad()
        pesos = []
        while peso_total > 0:
            carga = min(capacidad, peso_total)
            pesos.append(carga)
            peso_total -= carga
        costo = 0
        for carga in pesos:
            costo_kg = 1 if carga < 15000 else 2
            costo += costo_kg * carga
        return costo

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
        costo_total = 0

        costo_km = 20 if distancia < 200 else 15

        for _ in range(cantidad_vehiculos):
            costo_total += self.costo_fijo + costo_km * distancia

        return costo_total


class Aereo(Vehiculo):
    def __init__(self, conexion):
        # La velocidad inicial solo se usa si no se pasa conexión en calcular_tiempo
        velocidad = 400
        if conexion is not None and hasattr(conexion, "get_mal_clima"):
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

    def calcular_tiempo(self, distancia, conexion=None):
        """
        Calcula el tiempo considerando el mal clima si la conexión lo indica.
        """
        if conexion is not None and hasattr(conexion, "get_mal_clima"):
            velocidad = 400 if conexion.get_mal_clima() else 600
        else:
            velocidad = self.velocidad
        return (distancia / velocidad) * 60

class Maritimo(Vehiculo):
    def __init__(self, tipo_agua, calado_necesario=None):
        costo_fijo = 500 if tipo_agua == "fluvial" else 1500
        super().__init__(
            tipo=f"Barco ({tipo_agua})",
            modo="fluvial",  #cambie fluvial por maritimo adaptandolo a csv conexiones
            velocidad=40,
            capacidad=100000,
            costo_fijo=costo_fijo,
            costo_km=15,
            costo_kg=2,
        )
        self.tipo_agua = tipo_agua
        self.calado_necesario = calado_necesario
