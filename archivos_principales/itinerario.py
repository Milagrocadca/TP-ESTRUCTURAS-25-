
from collections import deque


class Itinerario:
    def __init__(
        self, solicitud, vehiculo, tramos, costo_total, tiempo_total, kpi_tipo, max_cant_vehiculos
    ):
        self.solicitud = solicitud
        self.vehiculo = vehiculo
        self.tramos = tramos  # lista de (origen, destino, conexion)
        self.costo_total = costo_total
        self.tiempo_total = tiempo_total
        self.kpi_tipo = kpi_tipo
        self.max_cant_vehiculos = max_cant_vehiculos
        self.max_cant_vehiculos = max_cant_vehiculos

    def __str__(self):
        salida = f"Itinerario para solicitud {self.solicitud.get_id()} ({self.solicitud.get_origen()} → {self.solicitud.get_destino()})\n"
        salida += f"Vehículo: {self.vehiculo.get_tipo()}\n"
        salida += f"Costo total: {self.costo_total:.2f} pesos\n"
        salida += f"Tiempo total: {self.tiempo_total:.2f} minutos\n"
        salida += f"Cantidad máxima de vehículos necesarios en un tramo: {self.max_cant_vehiculos}\n"
        salida += "Tramos:\n"
        for origen, destino, conexion in self.tramos:
            salida += f"  {origen} → {destino} | {conexion.get_tipo()} | {conexion.get_distancia()} km\n"
        return salida

    # GETTER
    def get_solicitud(self):
        return self.solicitud

    def get_vehiculo(self):
        return self.vehiculo

    def get_tramos(self):
        return self.tramos

    def get_kpi_tipo(self):
        return self.kpi_tipo

    def get_max_cant_vehiculos(self):
        return self.max_cant_vehiculos
