import csv
import numpy as np
from nodos import Nodo
from conexion import Conexion

class Red:
    """
    Inicializa la red de nodos y conexiones a partir de archivos CSV.
    Carga los nodos y luego las conexiones entre ellos.
    """
    def __init__(self):
        self.path_nodos = 'nodos.csv'
        self.path_conexiones =('conexiones.csv')
        self.red = (
            self.cargar_nodos()
        )  # red = {'nodo1':{}, 'nodo2':{}, ..., 'nodon':{}}
        self.cargar_conexiones()


    def cargar_nodos(self):
        """
        Lee el archivo de nodos y crea un diccionario de objetos Nodo para cada ciudad/punto.
        Devuelve un diccionario con los nombres de los nodos como claves.
        """
        nodos = {}
        with open(self.path_nodos, newline="", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                try:
                    nombre = row["nombre"]
                    nodo = Nodo(nombre, modos=[])
                    nodos[nombre] = nodo
                except KeyError as e:
                    print(f"Fila inválida (faltan columnas) en nodos: {row}  {e}")
                except Exception as e:
                    print(f"Error al procesar nodo: {row}  {e}")
                except FileNotFoundError:
                    print(f"Archivo no encontrado: {self.path_nodos}")
                except Exception as e:
                    print(f"Error general al cargar nodos: {e}")
            return nodos

    @staticmethod
    def cargar_conexion(row):
        """
    Crea dos objetos Conexion (ida y vuelta) a partir de una fila del archivo CSV de conexiones.
    Devuelve los nodos de origen y destino, el modo, y ambas conexiones.
    """
        try:
            origen = row["origen"]
            destino = row["destino"]
            tipo = row["tipo"]
            modo = tipo.lower()
            distancia = float(row["distancia_km"]) if row["distancia_km"] else 0
            restriccion = row.get("restriccion", "").strip()
            valor = row.get("valor_restriccion", "").strip()
            conexion = None

            conexion_origen = Conexion(
                origen, destino, tipo, distancia, restriccion, valor
            )
            conexion_destino = Conexion(
                destino, origen, tipo, distancia, restriccion, valor
            )

            return origen, destino, modo, conexion_origen, conexion_destino

        except Exception as e:
            print(f"Error al cargar conexión: {row}  {e}")
            return None

    def cargar_conexiones(self):
        """
        Lee el archivo de conexiones y agrega cada conexión a los nodos correspondientes en la red.
        También actualiza los modos de transporte habilitados para cada nodo.
        """
        try:
            with open(self.path_conexiones, newline="", encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                for row in reader:
                    resultado = Red.cargar_conexion(row)
                    if resultado:
                        (
                            nodo_origen,
                            nodo_destino,
                            modo,
                            conexion_origen,
                            conexion_destino,
                        ) = resultado
                        self.red[nodo_origen].agregar_conexion(conexion_origen)
                        self.red[nodo_origen].modos.add(modo)

                        self.red[nodo_destino].agregar_conexion(conexion_destino)
                        self.red[nodo_destino].modos.add(modo)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {self.path_conexiones}")
        except Exception as e:
            print(f"Error general al cargar conexiones: {e}")

    def get_red(self):
        """
    Devuelve el diccionario completo de la red de nodos con sus conexiones.
    """
        return self.red
