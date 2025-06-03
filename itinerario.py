from validaciones import *

from collections import deque

class Itinerario:
    def init(self, solicitud, vehiculo, tramos, kpi_total, kpi_tipo):
        self.solicitud = solicitud
        self.vehiculo = vehiculo
        self.tramos = tramos # lista de (origen, destino, conexion)
        self.kpi_total = kpi_total
        self.kpi_tipo = kpi_tipo

    def __str__(self):
        salida = f"Itinerario para solicitud {self.solicitud.get_id()} ({self.solicitud.get_origen()} → {self.solicitud.get_destino()})\n"
        salida += f"Vehículo: {self.vehiculo.get_tipo()}\n"
        salida += f"KPI ({self.kpi_tipo}) total: {self.kpi_total:.2f}\n"
        salida += "Tramos:\n"
        for origen, destino, conexion in self.tramos:
            salida += f"  {origen} → {destino} | {conexion.get_tipo()} | {conexion.get_distancia()} km\n"
        return salida

    #GETTER
    def get_solicitud(self):
        return self.solicitud

    def get_vehiculo(self):
        return self.vehiculo

    def get_tramos(self):
        return self.tramos

    def get_kpi_total(self):
        return self.kpi_total

    def get_kpi_tipo(self):
        return self.kpi_tipo