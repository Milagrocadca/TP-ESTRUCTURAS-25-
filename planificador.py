from collections import deque
import math
from itinerario import Itinerario
from conexion import Conexion
from nodos import Nodo

class Planificador:
    '''Busca todas las rutas posibles entre el origen y destino de la solicitud, usando los vehículos disponibles y el criterio de optimización'''
    def __init__(self, nodos, vehiculos):
        self.nodos = nodos
        self.vehiculos = vehiculos
        
    def planificar(self, solicitud, kpi="costo"):
        self.rutas_validas = []

        origen = solicitud.get_origen()
        destino = solicitud.get_destino()
        peso = solicitud.get_peso()

        visitados = set()
        ruta = []

        self._dfs(
            actual=origen,
            destino=destino,
            peso=peso,
            kpi=kpi,
            visitados=visitados,
            acumulado=0,
            ruta=ruta,
            tipo_conexion_actual=None
        )
        
        if not self.rutas_validas:
            return None

        #ITINERARIO CHEQUEAR
        mejor = min(self.rutas_validas, key=lambda x: x[0])
        tramos_completos = mejor[1]
        kpi_total = mejor[0]
        max_cant_vehiculos = mejor[2]
        

        # separar vehículo único y tramos sin vehículo
        primer_tramo = tramos_completos[0]
        vehiculo_usado = primer_tramo[2]
        tramos = [(inicio, fin, conexion) for (inicio, fin, _, conexion,_) in tramos_completos]

        return Itinerario(
            solicitud=solicitud,
            vehiculo=vehiculo_usado,
            tramos=tramos,
            kpi_total=kpi_total,
            kpi_tipo=kpi,
            max_cant_vehiculos=max_cant_vehiculos
            )


    def _dfs(self, actual, destino, peso, kpi, visitados, acumulado, ruta, tipo_conexion_actual):
        '''Busca todas las rutas posibles desde el nodo actual hasta el destino, evitando ciclos y considerando restricciones de vehículos y conexiones'''
        if actual == destino:
            max_cant = max((tramo[4] for tramo in ruta), default=0)
            self.rutas_validas.append((acumulado, list(ruta), max_cant))
            return

        visitados.add(actual)
        nodo_actual = self.nodos[actual]

        for conexion in nodo_actual.conexiones:
            siguiente = conexion.get_destino()
            tipo_conexion = conexion.get_tipo()

            es_tipo_valido = tipo_conexion_actual is None or tipo_conexion == tipo_conexion_actual #revisa que sea el primero o siga el camino por el mismo tipo de vehiculo 
            no_visitado = siguiente not in visitados

            if es_tipo_valido and no_visitado:
                for vehiculo in self.vehiculos:
                    evaluacion = self.evaluar_ruta(vehiculo, conexion, peso, kpi)

                    if evaluacion is not None:
                        valor, cant = evaluacion
                        
                        ruta.append((actual, siguiente, vehiculo, conexion,cant))
                        nuevo_tipo = tipo_conexion if tipo_conexion_actual is None else tipo_conexion_actual

                        self._dfs(
                        actual=siguiente,
                        destino=destino,
                        peso=peso,
                        kpi=kpi,
                        visitados=visitados,
                        acumulado=acumulado + valor,
                        ruta=ruta,
                        tipo_conexion_actual=nuevo_tipo
                    )


                        ruta.pop()

        visitados.remove(actual)

    
        
        #tiene todas los  y vehciulos
        # me fijo si existe ls conexion unica y sino intermediario
        #llamar las def que creemos en nodo

    def evaluar_ruta(self, vehiculo, conexion, peso, kpi):
        '''Calcula el costo o tiempo de recorrer una conexión con un vehículo, para una carga dada.'''
        if not vehiculo.puede_recorrer(conexion, peso):
            return None

        cant = math.ceil(peso / vehiculo.get_capacidad())

        if kpi == "costo":
            valor= vehiculo.calcular_costo_total(conexion.get_distancia(), peso) * cant
        elif kpi == "tiempo":
            valor = vehiculo.calcular_tiempo(conexion.get_distancia(), conexion.get_vel_max())
        else:
            return None

        return valor, cant