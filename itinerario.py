from validaciones import *

from collections import deque

class Itinerario:
    def __init__(self, solicitud, tramos, vehiculo, tiempo_total, costo_total):
        """
        Representa la solución óptima para una solicitud de transporte.

        :param solicitud: Objeto Solicitud
        :param tramos: Lista de objetos Conexion
        :param vehiculo: Objeto Vehiculo usado
        :param tiempo_total: Tiempo total del itinerario
        :param costo_total: Costo total del itinerario
        """
        self.solicitud = solicitud
        self.tramos = tramos
        self.vehiculo = vehiculo
        self.tiempo_total = tiempo_total
        self.costo_total = costo_total

    def imprimir(self):
        print(f"\n Solicitud ID: {self.solicitud.id_carga}")
        print(f"Vehículo utilizado: {self.vehiculo}")
        print(f"Tramos del itinerario:")
        for tramo in self.tramos:
            print(f"   {tramo.origen} , {tramo.destino} | Modo: {tramo.modo} | Distancia: {tramo.distancia} km")
        print(f"\n Tiempo total: {self.tiempo_total} horas")
        print(f"Costo total: ${self.costo_total}")

    def as_dict(self):
        """ Útil para exportar a CSV """
        return {
            "id_solicitud": self.solicitud.id_carga,
            "origen": self.solicitud.origen,
            "destino": self.solicitud.destino,
            "vehiculo": self.vehiculo.tipo,
            "modo": self.vehiculo.modo,
            "tiempo_total": self.tiempo_total,
            "costo_total": self.costo_total
        }