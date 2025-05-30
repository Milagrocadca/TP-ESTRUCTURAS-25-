from validaciones import *

class Vehiculo:
    def __init__(self, idVehiculo, tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg):
        """
        :param tipo: Nombre del vehículo (str, ej: 'Camión', 'Tren')
        :param modo: Modo de transporte ('automotor', 'ferroviario', etc.)
        :param velocidad: Velocidad nominal (km/h)
        :param capacidad: Capacidad de carga (kg)
        :param costo_fijo: Costo fijo por tramo ($)
        :param costo_km: Costo por km recorrido ($)
        :param costo_kg: Costo por kg transportado ($)
        """
        if not Vehiculo.validarModo(modo):
            raise ValueError ("El modo del vehiculo ingresado no se encentra dentro de las opciones disponibles")

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
         
        self.idVehiculo= idVehiculo
        
        self.tipo = tipo        
        self.modo = modo
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.costo_fijo = costo_fijo
        self.costo_km = costo_km
        self.costo_kg = costo_kg

    @staticmethod 
    def validarModo(modo):
        lista_modos=('automotor','ferroviario','aereo','maritimo')
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


    #RESTRICCIONES
    def puede_recorrer(self, tramo, peso):
        """
        Verifica si el vehículo puede recorrer el tramo dado el peso:
        - El modo debe coincidir
        - El peso no debe superar el máximo permitido del tramo
        - El calado del vehículo debe ser compatible (si aplica)
        """
        if tramo.modo != self.modo:
            return False

        if tramo.peso_max is not None and peso > tramo.peso_max:
            return False

        if tramo.vel_max is not None and self.velocidad > tramo.vel_max:
            return False

        if tramo.modo == "maritimo" and tramo.calado_max is not None:
            if hasattr(self, "calado_necesario") and self.calado_necesario is not None:
                if self.calado_necesario > tramo.calado_max:
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

class Ferroviario(Vehiculo):
    def __init__(self):
        super().__init__(
            tipo="Tren",
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
