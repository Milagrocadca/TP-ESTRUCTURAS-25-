import math
import random
from itinerario import Itinerario
from vehiculos import Automotor
from vehiculos import Aereo


class Planificador:
    def __init__(self, nodos, vehiculos):
        self.nodos = nodos
        self.vehiculos = vehiculos
        self.itinerarios_validos = []

    def planificar(self, solicitud, kpi="costo"):
        self.itinerarios_validos = []
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

        return self.seleccionar_mejor_itinerario(solicitud, kpi)

    def seleccionar_mejor_itinerario(self, solicitud, kpi):
        if not self.itinerarios_validos:
            return None

        if kpi == "costo":
            mejor = min(self.itinerarios_validos, key=lambda elem: elem.costo_total)
        elif kpi == "tiempo":
            mejor = min(self.itinerarios_validos, key=lambda elem: elem.tiempo_total)
        elif kpi == "aleatorio":
            candidatos = [elem for elem in self.itinerarios_validos if len(elem.tramos) <= 3]
            if not candidatos:
                return None
            mejor = random.choice(candidatos)
        else:
            return None

        vehiculo_usado = mejor.vehiculo
        peso = solicitud.get_peso()
        costo_total = mejor.costo_total

        if vehiculo_usado.get_tipo() == "Camión":
            costo_kg_total = Automotor.calcular_costo_kg_automotor(vehiculo_usado, peso)
        else:
            costo_kg_total = vehiculo_usado.get_costo_kg() * peso

        costo_total += costo_kg_total

        return Itinerario(
            solicitud=mejor.solicitud,
            vehiculo=mejor.vehiculo,
            tramos=mejor.tramos,
            costo_total=costo_total,
            tiempo_total=mejor.tiempo_total,
            kpi_tipo=mejor.kpi_tipo,
            max_cant_vehiculos=mejor.max_cant_vehiculos,
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
