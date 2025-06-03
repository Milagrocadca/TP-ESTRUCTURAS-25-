import csv
import numpy as np
from nodos import Nodo
from conexion import Conexion, ConexionFluvial, ConexionMaritima

#crear clase red que en el init de red tenga cargar nodo y cargar conexiones. tener los nodos y hacer un self.nodos 
#cargar conexiones nos devuelve conexion
class Red:
    def __init__(self):
        self.nodos=Red.cargar_nodos()
        self.conexiones=Red.cargar_conexiones()


    @staticmethod
    def cargar_nodos(path_nodos):
        nodos = {}
        with open(path_nodos, newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                try:
                    nombre = row['nombre']
                    nodo = Nodo(nombre, modos=[])
                    nodos[nombre] = nodo
                except KeyError as e:
                    print(f"Fila inválida (faltan columnas) en nodos: {row}  {e}")
                except Exception as e:
                    print(f"Error al procesar nodo: {row}  {e}")
                except FileNotFoundError:
                    print(f"Archivo no encontrado: {path_nodos}")
                except Exception as e:
                    print(f"Error general al cargar nodos: {e}")
            return nodos



    @staticmethod
    def cargar_conexion(row):
        try:
            origen = row["origen"]
            destino = row["destino"]
            tipo = row["tipo"]
            distancia = float(row["distancia_km"]) if row["distancia_km"] else 0
            restriccion = row.get("restriccion", "").strip()
            valor = row.get("valor_restriccion", "").strip()

            modo = tipo.lower()
            vel_max = peso_max = prob_mal_tiempo = None
            conexion = None

            if restriccion == "velocidad_max":
                vel_max = float(valor)
            elif restriccion == "peso_max":
                peso_max = float(valor)
            if restriccion == "prob_mal_tiempo":
                 prob_mal_tiempo = float(valor)
            elif restriccion == "tipo":
                if valor == "fluvial":
                    conexion = ConexionFluvial(tipo, distancia, destino)
                    modo = "maritimo"
                elif valor == "maritimo":
                    conexion = ConexionMaritima(tipo, distancia, destino)
                    modo = "maritimo"

            if conexion is None:
                conexion = Conexion(origen, destino, tipo, distancia, restriccion, valor)

            return origen, destino, modo, conexion

        except Exception as e:
            print(f"Error al cargar conexión: {row}  {e}")
            return None

    @staticmethod
    def cargar_conexiones(path_conexiones, nodos):
        try:
            with open(path_conexiones, newline='', encoding='utf-8') as archivo:
                reader = csv.DictReader(archivo)
                for row in reader:
                    resultado = Red.cargar_conexion(row)
                    if resultado:
                        origen, destino, modo, conexion = resultado
                        nodos[origen].agregar_conexion(conexion)
                        nodos[origen]._modos.add(modo)
                        nodos[destino]._modos.add(modo)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {path_conexiones}")
        except Exception as e:
            print(f"Error general al cargar conexiones: {e}")
        return nodos
