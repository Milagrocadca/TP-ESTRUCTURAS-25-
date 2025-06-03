import csv
import numpy as np
from nodos import Nodo
from conexion import Conexion, ConexionFluvial, ConexionMaritima

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
                print(f"Fila inválida (faltan columnas) en nodos: {row} → {e}")
            except Exception as e:
                print(f"Error al procesar nodo: {row} → {e}")
            except FileNotFoundError:
                print(f"Archivo no encontrado: {path_nodos}")
            except Exception as e:
                print(f"Error general al cargar nodos: {e}")
        return nodos



def cargar_conexiones(path_conexiones, nodos):
    try:
        with open(path_conexiones, newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                try:
                    origen = row["origen"]
                    destino = row["destino"]
                    tipo = row["tipo"]
                    distancia = float(np.nan_to_num(row["distancia_km"]))
                    restriccion = row.get("restriccion", "")
                    valor = row.get("valor_restriccion", "")

                    modo = tipo.lower()
                    vel_max = peso_max = None
                    conexion = None  # Inicializamos

                    if restriccion == "velocidad_max":
                        vel_max = float(valor)
                        conexion = Conexion(tipo, distancia, destino, modo, vel_max, peso_max)
                    elif restriccion == "peso_max":
                        peso_max = float(valor)
                        conexion = Conexion(tipo, distancia, destino, modo, vel_max, peso_max)
                    elif restriccion == "prob_mal_tiempo":
                        vel_max = 400 if float(valor) > 0 else 600
                        conexion = Conexion(tipo, distancia, destino, modo, vel_max, peso_max)
                    elif restriccion == "tipo":
                        if valor == "fluvial":
                            conexion = ConexionFluvial(tipo, distancia, destino)
                            modo = "maritimo"
                        elif valor == "maritimo":
                            conexion = ConexionMaritima(tipo, distancia, destino)
                            modo = "maritimo"
                        else:
                            print(f"Restricción tipo desconocida en fila: {row}")
                    else:
                        # Sin restricciones conocidas
                        conexion = Conexion(tipo, distancia, destino, modo, vel_max, peso_max)

                    # Si se creó una conexión válida, la agregamos
                    if conexion:
                        nodos[origen].agregar_conexion(conexion)
                        nodos[origen]._modos.add(modo)
                        nodos[destino]._modos.add(modo)
                    else:
                        print(f"No se pudo crear conexión para fila: {row}")

                except KeyError as e:
                    print(f"Fila inválida (faltan columnas) en conexiones: {row} → {e}")
                except ValueError as e:
                    print(f"Error de conversión de datos en fila de conexiones: {row} → {e}")
                except Exception as e:
                    print(f"Error general al procesar conexión: {row} → {e}")
    except FileNotFoundError:
        print(f"Archivo no encontrado: {path_conexiones}")
    except Exception as e:
        print(f"Error general al cargar conexiones: {e}")
    return nodos