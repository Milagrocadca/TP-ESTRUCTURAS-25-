from collections import deque
import math
from itinerario import Itinerario
from conexion import Conexion
from nodos import Nodo
from vehiculos import *
class Planificador:
    """Busca todas las rutas posibles entre el origen y destino de la solicitud, usando los vehículos disponibles y el criterio de optimización"""

    def __init__(self, nodos, vehiculos):
        self.nodos = nodos
        self.vehiculos = vehiculos

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

        """
        mejor = None
        for ruta in rutas_validas:
            valor = ruta[0]
            if mejor == None:
                mejor = ruta
            elif valor < mejor[0]:
                mejor = ruta

        tramos_completos = mejor[1]
        kpi_total = mejor[0]
        max_cant_vehiculos = mejor[2]
        """
        if not rutas_validas:
            return None

        indice_kpi = 0 if kpi == "costo" else 1
        mejor = min(rutas_validas, key=lambda r: r[indice_kpi])
        print(rutas_validas)

        costo_total = mejor[0]
        tiempo_total = mejor[1]
        tramos_completos = mejor[2]
        max_cant_vehiculos = mejor[3]

        # separar vehículo único y tramos sin vehículo
        primer_tramo = tramos_completos[0]
        vehiculo_usado = primer_tramo[2]
        tramos = [
            (inicio, fin, conexion)
            for (inicio, fin, _, conexion, _) in tramos_completos
        ]

        return Itinerario(
            solicitud=solicitud,
            vehiculo=vehiculo_usado,
            tramos=tramos,
            #pi_total=kpi_total,
            costo_total=costo_total,
            tiempo_total=tiempo_total,
            kpi_tipo=kpi,
            max_cant_vehiculos=max_cant_vehiculos,
        )

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
        """Busca todas las rutas posibles desde el nodo actual hasta el destino, evitando ciclos y considerando restricciones de vehículos y conexiones"""
        if actual == destino:
            max_cant_vehiculos = max((tramo[4] for tramo in ruta), default=0)
            rutas_validas.append((acumulado_costo, acumulado_tiempo, list(ruta), max_cant_vehiculos))
            return rutas_validas

        visitados.add(actual)
        nodo_actual = self.nodos[actual]
        for conexion in nodo_actual.conexiones:
            siguiente = conexion.get_destino()
            tipo_conexion_siguiente = conexion.get_tipo()
            es_tipo_valido = (
                tipo_conexion_actual is None
                or tipo_conexion_siguiente == tipo_conexion_actual
            )  # revisa que sea el primero o siga el camino por el mismo tipo de vehiculo
            no_visitado = siguiente not in visitados
            if es_tipo_valido and no_visitado:
                # <-- PROBLEMA: la variable vehiculos es la lista de vehiculo. Pero no menciona si es automotor, aereo, maritimo, etc.
                for vehiculo in self.vehiculos.values():
                    evaluacion = self.evaluar_ruta(vehiculo, conexion, peso, kpi)
                    if evaluacion is not None:
                        costo, tiempo, cant_vehiculos = evaluacion

                        ruta.append(
                            (actual, siguiente, vehiculo, conexion, cant_vehiculos)
                        )
                        nuevo_tipo = (
                            tipo_conexion_siguiente
                            if tipo_conexion_actual is None
                            else tipo_conexion_actual
                        )
                        rutas_validas=self._dfs(
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

        # tiene todas los  y vehciulos
        # me fijo si existe ls conexion unica y sino intermediario
        # llamar las def que creemos en nodo

    def evaluar_ruta(self, vehiculo, conexion, peso,kpi):
        if not vehiculo.puede_recorrer(conexion, peso):
            return None

        costo_total, cant_vehiculos = vehiculo.calcular_costo_total(conexion.get_distancia(), peso), math.ceil(peso / vehiculo.get_capacidad())
        tiempo = vehiculo.calcular_tiempo(conexion.get_distancia(), conexion.get_vel_max())

        return costo_total, tiempo, cant_vehiculos


"""
    def evaluar_ruta(self, vehiculo, conexion, peso, kpi):
        #Calcula el costo o tiempo de recorrer una conexión con un vehículo, para una carga dada.
        if not vehiculo.puede_recorrer(conexion, peso):
            return None

        cant_vehiculos = math.ceil(peso / vehiculo.get_capacidad())

        if kpi == "costo":
            valor = vehiculo.calcular_costo_total(
                conexion.get_distancia(), peso
            )
        elif kpi == "tiempo":
            valor = vehiculo.calcular_tiempo(
                conexion.get_distancia(), conexion.get_vel_max()
            )
        else:
            return None

        return valor, cant_vehiculos"""