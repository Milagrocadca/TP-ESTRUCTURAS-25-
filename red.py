import csv
import numpy as np
from nodos import Nodo
from conexion import Conexion, ConexionFluvial, ConexionMaritima

def cargar_nodos(path_nodos):
    nodos = {}
    with open(path_nodos, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:
            nombre = row['nombre']
            nodo = Nodo(nombre, modos=[])
            nodos[nombre] = nodo
    return nodos

def cargar_conexiones(path_conexiones, nodos):
    with open(path_conexiones, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:
            origen = row["origen"]
            destino = row["destino"]
            tipo = row["tipo"]
            distancia = float(np.nan_to_num(row["distancia_km"]))
            restriccion = row.get("restriccion", "")
            valor = row.get("valor_restriccion", "")

            modo = tipo.lower()
            vel_max = peso_max = None

            if restriccion == "velocidad_max":
                vel_max = float(valor)
            elif restriccion == "peso_max":
                peso_max = float(valor)
            elif restriccion == "prob_mal_tiempo":
                vel_max = 400 if float(valor) > 0 else 600
            elif restriccion == "tipo":
                if valor == "fluvial":
                    conexion = ConexionFluvial(tipo, distancia, destino)
                elif valor == "maritimo":
                    conexion = ConexionMaritima(tipo, distancia, destino)
                else:
                    continue
                nodos[origen].agregar_conexion(conexion)
                nodos[origen]._modos.add("maritimo")
                nodos[destino]._modos.add("maritimo")
                continue

            conexion = Conexion(tipo, distancia, destino, modo, vel_max, peso_max)
            nodos[origen].agregar_conexion(conexion)
            nodos[origen]._modos.add(modo)
            nodos[destino]._modos.add(modo)
    return nodos