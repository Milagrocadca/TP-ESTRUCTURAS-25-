from collections import deque
import math

class Planificador:
    def init(self, nodos, vehiculos):
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

        # mejor = min(self.rutas_validas, key=lambda x: x[0])
        # return {
        #     "kpi_total": mejor[0],
        #     "itinerario": mejor[1],
        #     "kpi": kpi
        # }
        
        if not self.rutas_validas:
            return None

        #ITINERARIO CHEQUEAR
        mejor = min(self.rutas_validas, key=lambda x: x[0])
        tramos_completos = mejor[1]
        kpi_total = mejor[0]

        # separar vehículo único y tramos sin vehículo
        primer_tramo = tramos_completos[0]
        vehiculo_usado = primer_tramo[2]
        tramos = [(origen, destino, conexion) for (origen, destino, _, conexion) in tramos_completos]

        return Itinerario(
            solicitud=solicitud,
            vehiculo=vehiculo_usado,
            tramos=tramos,
            kpi_total=kpi_total,
            kpi_tipo=kpi)


    def _dfs(self, actual, origen, destino, peso, kpi, visitados, acumulado, ruta, tipo_conexion_actual, max_cant_vehiculos):

        if actual == destino:
            self.rutas_validas.append((acumulado, list(ruta)))
            return

        visitados.add(actual)
        nodo = self.nodos[actual]

        for conexion in nodo.get_conexiones():
            siguiente = conexion.get_destino()
            tipo_conexion = conexion.get_tipo()

            es_tipo_valido = tipo_conexion_actual is None or tipo_conexion == tipo_conexion_actual
            no_visitado = siguiente not in visitados

            if es_tipo_valido and no_visitado:
                for vehiculo in self.vehiculos:
                    evaluacion = self.evaluar_ruta(vehiculo, conexion, peso, kpi)

                    if evaluacion is not None:
                        valor, cant = evaluacion
                        
                        ruta.append((actual, siguiente, vehiculo, conexion))
                        nuevo_tipo = tipo_conexion if tipo_conexion_actual is None else tipo_conexion_actual

                        self._dfs(
                        actual=origen,
                        destino=destino,
                        peso=peso,
                        kpi=kpi,
                        visitados=visitados,
                        acumulado=0,
                        ruta=ruta,
                        tipo_conexion_actual=None,
                        max_cant_vehiculos=0
                    )


                        ruta.pop()

        visitados.remove(actual)

    
        
        #tiene todas los  y vehciulos
        # me fijo si existe ls conexion unica y sino intermediario
        #llamar las def que creemos en nodo

    def evaluar_ruta(self, vehiculo, conexion, peso, kpi):
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


""" # A PARTIR DE ACA
from math import ceil

def evaluar_ruta(ruta, vehiculo, peso, nodos):
    tiempo_total = 0
    costo_total = 0

    for tramo in ruta:
        # Validar que ambos nodos del tramo soportan el modo de transporte
        if not (nodos[tramo.origen].tiene_modo(vehiculo.modo) and
                nodos[tramo.destino].tiene_modo(vehiculo.modo)):
            return None

        # Validar que el vehículo puede usar ese tramo
        if not vehiculo.puede_recorrer(tramo, peso):
            return None

        # Determinar la velocidad efectiva
        velocidad = tramo.vel_max if tramo.vel_max else vehiculo.velocidad

        # Calcular cantidad de vehículos necesarios
        cantidad = ceil(peso / vehiculo.capacidad)

        # Calcular tiempo y costo del tramo
        tiempo_tramo = tramo.distancia / velocidad
        costo_tramo = vehiculo.calcular_costo_total(tramo.distancia, peso)

        tiempo_total += tiempo_tramo
        costo_total += costo_tramo * cantidad

    return {
        "ruta": ruta.copy(),  # importante hacer copia si vas a usarla más de una vez
        "vehiculo": vehiculo,
        "modo": vehiculo.modo,
        "tiempo_total": round(tiempo_total, 2),
        "costo_total": round(costo_total, 2)
    }
from math import ceil

class Planificador:
    def __init__(self):
        self.nodos = {}  # nombre -> Nodo
        self.vehiculos = [Automotor(), Tren(), Aereo(), Maritimo("fluvial"), Maritimo("maritimo")]

    def buscar_rutas(self, solicitud):
        origen = solicitud.get_origen()
        destino = solicitud.get_destino()
        peso = solicitud.get_peso()
        rutas_viables = []

        # Paso 1: Encontrar rutas posibles (sin ciclos)
        rutas_crudas = []
        self._dfs(origen, destino, [], set(), rutas_crudas)

        # Paso 2: Evaluar rutas con cada tipo de vehículo
        for ruta in rutas_crudas:
            for vehiculo in self.vehiculos:
                resultado = evaluar_ruta(ruta, vehiculo, peso, self.nodos)
                if resultado:
                    rutas_viables.append(resultado)

        return rutas_viables

    def _dfs(self, actual, destino, camino_actual, visitados, resultados):
        if actual in visitados:
            return
        visitados.add(actual)

        if actual == destino:
            resultados.append(camino_actual.copy())
        else:
            nodo = self.nodos[actual]
            for conexion in nodo.conexiones:
                if conexion.destino not in visitados:
                    camino_actual.append(conexion)
                    self._dfs(conexion.destino, destino, camino_actual, visitados.copy(), resultados)
                    camino_actual.pop()
 """
