from collections import deque
import math
from itinerario import Itinerario
from conexion import Conexion
from nodos import Nodo
from vehiculos import Vehiculo
from vehiculos import Vehiculos
from vehiculos import Automotor
from vehiculos import Aereo


# class Planificador:
#     """Busca todas las rutas posibles entre el origen y destino de la solicitud, usando los vehículos disponibles y el criterio de optimización"""

#     def __init__(self, nodos, vehiculos):
#         self.nodos = nodos
#         self.vehiculos = vehiculos
#         self.itinerarios_validos = []

#     def planificar(self, solicitud, kpi="costo"):
#         """
#     Calcula el costo total por kg para el caso de automotor (camión),
#     considerando que cada camión puede tener diferente carga y costo por kg.
#     """
#         origen = solicitud.get_origen()
#         destino = solicitud.get_destino()
#         peso = solicitud.get_peso()
#         visitados = set()
#         ruta = []
#         rutas_validas = self._dfs(
#             actual=origen,
#             destino=destino,
#             peso=peso,
#             kpi=kpi,
#             visitados=visitados,
#             acumulado_costo=0,
#             acumulado_tiempo=0,
#             ruta=ruta,
#             rutas_validas=[],
#             tipo_conexion_actual=None,
#         )
#         if not rutas_validas:
#             return None

#         for ruta in rutas_validas:
#             costo_total = ruta[0]
#             tiempo_total = ruta[1]
#             tramos_completos = ruta[2]
#             max_cant_vehiculos = ruta[3]
#             primer_tramo = tramos_completos[0]
#             vehiculo_usado = primer_tramo[2]
#             tramos = [
#                 (inicio, fin, conexion)
#                 for (inicio, fin, _, conexion, _) in tramos_completos
#             ]
#             self.itinerarios_validos.append(
#                 Itinerario(
#                     solicitud=solicitud,
#                     vehiculo=vehiculo_usado,
#                     tramos=tramos,
#                     costo_total=costo_total,
#                     tiempo_total=tiempo_total,
#                     kpi_tipo=kpi,
#                     max_cant_vehiculos=max_cant_vehiculos,
#                 )
#             )

#         indice_kpi = 0 if kpi == "costo" else 1
#         mejor = min(rutas_validas, key=lambda r: r[indice_kpi])

#         costo_total = mejor[0]
#         tiempo_total = mejor[1]
#         tramos_completos = mejor[2]
#         max_cant_vehiculos = mejor[3]

#         # Separar vehículo único y tramos sin vehículo
#         primer_tramo = tramos_completos[0]
#         vehiculo_usado = primer_tramo[2]
#         tramos = [
#             (inicio, fin, conexion)
#             for (inicio, fin, _, conexion, _) in tramos_completos
#         ]
#         peso = solicitud.get_peso()

#         # Lógica especial para Automotor
#         if vehiculo_usado.get_tipo() == "Camión":
#             costo_kg_total = self.calcular_costo_kg_automotor(vehiculo_usado, peso)
#         else:
#             costo_kg_total = vehiculo_usado.get_costo_kg() * peso

#         costo_total += costo_kg_total

#         return Itinerario(
#             solicitud=solicitud,
#             vehiculo=vehiculo_usado,
#             tramos=tramos,
#             # pi_total=kpi_total,
#             costo_total=costo_total,
#             tiempo_total=tiempo_total,
#             kpi_tipo=kpi,
#             max_cant_vehiculos=max_cant_vehiculos,
#         )
#     def calcular_costo_kg_automotor(self, vehiculo, peso_total):

#         """
#         Realiza una búsqueda en profundidad (DFS) para encontrar todas las rutas posibles
#         desde el nodo actual hasta el destino, evitando ciclos y considerando restricciones
#         de vehículos y conexiones.
#         """
#         capacidad = vehiculo.get_capacidad()
#         pesos = []
#         while peso_total > 0:
#             carga = min(capacidad, peso_total)
#             pesos.append(carga)
#             peso_total -= carga
#         costo = 0
#         for carga in pesos:
#             costo_kg = 1 if carga < 15000 else 2
#             costo += costo_kg * carga
#         return costo
#     def _dfs(
#         self,
#         actual,
#         destino,
#         peso,
#         kpi,
#         visitados,
#         acumulado_costo,
#         acumulado_tiempo,
#         ruta,
#         rutas_validas,
#         tipo_conexion_actual,
#     ):
#         """Busca todas las rutas posibles desde el nodo actual hasta el destino, evitando ciclos y considerando restricciones de vehículos y conexiones"""
#         if actual == destino:
#             max_cant_vehiculos = max((tramo[4] for tramo in ruta), default=0)
#             rutas_validas.append(
#                 (acumulado_costo, acumulado_tiempo, list(ruta), max_cant_vehiculos)
#             )
#             return rutas_validas

#         visitados.add(actual)
#         nodo_actual = self.nodos[actual]
#         for conexion in nodo_actual.conexiones:
#             siguiente = conexion.get_destino()
#             tipo_conexion_siguiente = conexion.get_tipo()
#             es_tipo_valido = (
#                 tipo_conexion_actual is None
#                 or tipo_conexion_siguiente == tipo_conexion_actual
#             )  # revisa que sea el primero o siga el camino por el mismo tipo de vehiculo
#             no_visitado = siguiente not in visitados
#             if es_tipo_valido and no_visitado:
#                 #la variable vehiculos es la lista de vehiculo. Pero no menciona si es automotor, aereo, maritimo, etc.
#                 for vehiculo in self.vehiculos.values():
#                     evaluacion = self.evaluar_ruta(vehiculo, conexion, peso, kpi)
#                     if evaluacion is not None:
#                         costo, tiempo, cant_vehiculos = evaluacion

#                         ruta.append(
#                             (actual, siguiente, vehiculo, conexion, cant_vehiculos)
#                         )
#                         nuevo_tipo = (
#                             tipo_conexion_siguiente
#                             if tipo_conexion_actual is None
#                             else tipo_conexion_actual
#                         )
#                         rutas_validas = self._dfs(
#                             actual=siguiente,
#                             destino=destino,
#                             peso=peso,
#                             kpi=kpi,
#                             visitados=visitados,
#                             acumulado_costo=acumulado_costo + costo,
#                             acumulado_tiempo=acumulado_tiempo + tiempo,
#                             ruta=ruta,
#                             rutas_validas=rutas_validas,
#                             tipo_conexion_actual=nuevo_tipo,
#                         )
#                         ruta.pop()
#         visitados.remove(actual)
#         return rutas_validas


#     def get_itinerarios_validos(self):
#         """
#     Devuelve la lista de itinerarios válidos encontrados en la última planificación.
#     """
#         return self.itinerarios_validos

#     def evaluar_ruta(self, vehiculo, conexion, peso, kpi):
#         """
#             Evalúa si un vehículo puede recorrer una conexión con el peso dado.
#             Si es posible, calcula y retorna:
#             - el costo del tramo (sin costo por kg para camión),
#             - el tiempo necesario para recorrer el tramo (considerando clima si es aéreo),
#             - y la cantidad de vehículos necesarios para ese tramo.
#             Si el vehículo no puede recorrer la conexión, retorna None.
#             """
#         if not vehiculo.puede_recorrer(conexion):
#             return None

#         # Para Automotor, obtener ambos valores; para otros, solo el costo
#         if vehiculo.get_tipo() == "Camión":
#             costo, _ = vehiculo.calcular_costo_total(conexion.get_distancia(), peso)
#         else:
#             costo = vehiculo.calcular_costo_total(conexion.get_distancia(), peso)

#         cant_vehiculos = math.ceil(peso / vehiculo.get_capacidad())
#         if isinstance(vehiculo, Aereo):
#             tiempo = vehiculo.calcular_tiempo(conexion.get_distancia(), conexion)
#         else:
#             vel_max_str = conexion.restricciones.get('velocidad_max')
#             if vel_max_str is not None and vel_max_str != '':
#                 vel_max = float(vel_max_str)
#             else:
#                 vel_max = None  # No hay restricción, se usará la velocidad del vehículo
#             tiempo = vehiculo.calcular_tiempo(conexion.get_distancia(), vel_max)
  

#         return costo, tiempo, cant_vehiculos

class Planificador:
    def __init__(self, nodos, vehiculos):
        self.nodos = nodos
        self.vehiculos = vehiculos
        self.itinerarios_validos = []

    def planificar(self, solicitud, kpi="costo"):
        origen = solicitud.get_origen()
        destino = solicitud.get_destino()
        peso = solicitud.get_peso()
        visitados = set()
        ruta = []

        rutas_validas = self._dfs(
            actual=origen,
            destino=destino,
            peso=peso,
            kpi=kpi,
            visitados=visitados,
            acumulado_costo=0,
            acumulado_tiempo=0,
            ruta=ruta,
            rutas_validas=[],
            tipo_conexion_actual=None,
        )

        if not rutas_validas:
            return None

        for ruta_dict in rutas_validas:
            costo_total = ruta_dict["costo_total"]
            tiempo_total = ruta_dict["tiempo_total"]
            tramos_completos = ruta_dict["tramos_completos"]
            max_cant_vehiculos = ruta_dict["max_cant_vehiculos"]

            vehiculo_usado = tramos_completos[0]["vehiculo"]
            tramos = [
                (t["origen"], t["destino"], t["conexion"])
                for t in tramos_completos
            ]

            self.itinerarios_validos.append(
                Itinerario(
                    solicitud=solicitud,
                    vehiculo=vehiculo_usado,
                    tramos=tramos,
                    costo_total=costo_total,
                    tiempo_total=tiempo_total,
                    kpi_tipo=kpi,
                    max_cant_vehiculos=max_cant_vehiculos,
                )
            )

        mejor = min(rutas_validas, key=lambda r: r["costo_total"] if kpi == "costo" else r["tiempo_total"])
        costo_total = mejor["costo_total"]
        tiempo_total = mejor["tiempo_total"]
        tramos_completos = mejor["tramos_completos"]
        max_cant_vehiculos = mejor["max_cant_vehiculos"]

        vehiculo_usado = tramos_completos[0]["vehiculo"]
        tramos = [
            (t["origen"], t["destino"], t["conexion"])
            for t in tramos_completos
        ]

        if vehiculo_usado.get_tipo() == "Camión":
            costo_kg_total = self.calcular_costo_kg_automotor(vehiculo_usado, peso)
        else:
            costo_kg_total = vehiculo_usado.get_costo_kg() * peso

        costo_total += costo_kg_total

        return Itinerario(
            solicitud=solicitud,
            vehiculo=vehiculo_usado,
            tramos=tramos,
            costo_total=costo_total,
            tiempo_total=tiempo_total,
            kpi_tipo=kpi,
            max_cant_vehiculos=max_cant_vehiculos,
        )

    def calcular_costo_kg_automotor(self, vehiculo, peso_total):
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

    def _dfs(
        self,
        actual,
        destino,
        peso,
        kpi,
        visitados,
        acumulado_costo,
        acumulado_tiempo,
        ruta,
        rutas_validas,
        tipo_conexion_actual,
    ):
        if actual == destino:
            rutas_validas.append({
                "costo_total": acumulado_costo,
                "tiempo_total": acumulado_tiempo,
                "tramos_completos": list(ruta),
                "max_cant_vehiculos": max((tramo["cant_vehiculos"] for tramo in ruta), default=0),
            })
            return rutas_validas

        visitados.add(actual)
        nodo_actual = self.nodos[actual]
        for conexion in nodo_actual.conexiones:
            siguiente = conexion.get_destino()
            tipo_conexion_siguiente = conexion.get_tipo()
            es_tipo_valido = (
                tipo_conexion_actual is None
                or tipo_conexion_siguiente == tipo_conexion_actual
            )
            no_visitado = siguiente not in visitados
            if es_tipo_valido and no_visitado:
                for vehiculo in self.vehiculos.values():
                    evaluacion = self.evaluar_ruta(vehiculo, conexion, peso, kpi)
                    if evaluacion is not None:
                        costo, tiempo, cant_vehiculos = evaluacion

                        tramo = {
                            "origen": actual,
                            "destino": siguiente,
                            "vehiculo": vehiculo,
                            "conexion": conexion,
                            "cant_vehiculos": cant_vehiculos
                        }
                        ruta.append(tramo)

                        nuevo_tipo = (
                            tipo_conexion_siguiente
                            if tipo_conexion_actual is None
                            else tipo_conexion_actual
                        )

                        rutas_validas = self._dfs(
                            actual=siguiente,
                            destino=destino,
                            peso=peso,
                            kpi=kpi,
                            visitados=visitados,
                            acumulado_costo=acumulado_costo + costo,
                            acumulado_tiempo=acumulado_tiempo + tiempo,
                            ruta=ruta,
                            rutas_validas=rutas_validas,
                            tipo_conexion_actual=nuevo_tipo,
                        )
                        ruta.pop()
        visitados.remove(actual)
        return rutas_validas

    def get_itinerarios_validos(self):
        return self.itinerarios_validos

    def evaluar_ruta(self, vehiculo, conexion, peso, kpi):
        if not vehiculo.puede_recorrer(conexion):
            return None

        if vehiculo.get_tipo() == "Camión":
            costo, _ = vehiculo.calcular_costo_total(conexion.get_distancia(), peso)
        else:
            costo = vehiculo.calcular_costo_total(conexion.get_distancia(), peso)

        cant_vehiculos = math.ceil(peso / vehiculo.get_capacidad())

        if isinstance(vehiculo, Aereo):
            tiempo = vehiculo.calcular_tiempo(conexion.get_distancia(), conexion)
        else:
            vel_max_str = conexion.restricciones.get('velocidad_max')
            if vel_max_str is not None and vel_max_str != '':
                vel_max = float(vel_max_str)
            else:
                vel_max = None  # O la velocidad por defecto del vehículo
            tiempo = vehiculo.calcular_tiempo(conexion.get_distancia(), vel_max)

        return costo, tiempo, cant_vehiculos
