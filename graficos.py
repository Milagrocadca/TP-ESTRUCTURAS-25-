from conexion import Conexion
from itinerario import Itinerario
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def graficar_distancia_vs_tiempo(itinerario, solicitud_id=None):
    """
    Grafica la distancia acumulada recorrida en función del tiempo acumulado.
    Cada punto representa el avance tras cada tramo del itinerario.
    """
    plt.figure()

    valor_por_defecto = 100000  # Valor por defecto para velocidad_max elegimos un numero imposible de llegar en caso de que no haya limite)
    tramos = itinerario.get_tramos()
    vehiculo = itinerario.get_vehiculo()

    print(tramos)

    distancias = [0]
    tiempos = [0]
    distancia_acumulada = 0
    tiempo_acumulado = 0

    for origen, destino, conexion in tramos:
        distancia = conexion.get_distancia()
        vel_max = float(conexion.restricciones.get("velocidad_max", valor_por_defecto))
        tiempo = vehiculo.calcular_tiempo(distancia, vel_max)
        distancia_acumulada += distancia
        tiempo_acumulado += tiempo
        distancias.append(distancia_acumulada)
        tiempos.append(tiempo_acumulado)
        print(
            f"Tiempo: {tiempo_acumulado:.2f} min, Distancia: {distancia_acumulada:.2f} km"
        )

    print(tiempos)
    print(distancias)

    plt.plot(tiempos, distancias, marker="o")
    plt.xlabel("Tiempo acumulado (minutos)")
    plt.ylabel("Distancia acumulada (km)")
    titulo = "Distancia acumulada vs Tiempo"
    if solicitud_id:
        titulo += f" (Solicitud {solicitud_id})"
    plt.title(titulo)
    plt.grid(True)


def graficar_costo_vs_distancia(itinerario, solicitud_id=None):
    """
    Grafica el costo total acumulado por cada modo de transporte.
    Agrupa todos los itinerarios válidos por modo y suma sus costos.
    """
    plt.figure()

    tramos = itinerario.get_tramos()
    vehiculo = itinerario.get_vehiculo()

    distancias = [0]
    costos = [0]
    distancia_acumulada = 0
    costo_acumulado = 0

    for origen, destino, conexion in tramos:
        distancia = conexion.get_distancia()
        peso = (
            itinerario.get_solicitud().get_peso()
            if hasattr(itinerario, "get_solicitud")
            else 0
        )
        costo = vehiculo.calcular_costo_total(distancia, peso)
        # Si el resultado es una tupla, tomá solo el primer valor
        if isinstance(costo, tuple):
            costo = costo[0]
        distancia_acumulada += distancia
        costo_acumulado += costo
        distancias.append(distancia_acumulada)
        costos.append(costo_acumulado)
        print(
            f"Distancia: {distancia_acumulada:.2f} km, Costo acumulado: {costo_acumulado:.2f}"
        )

    print(distancias)
    print(costos)

    plt.plot(distancias, costos, marker="o", color="red")
    plt.xlabel("Distancia acumulada (km)")
    plt.ylabel("Costo acumulado")
    titulo = "Costo acumulado vs Distancia"
    if solicitud_id:
        titulo += f" (Solicitud {solicitud_id})"
    plt.title(titulo)
    plt.grid(True)



def graficar_comparacion_itinerarios(itinerario_costo, itinerario_tiempo, solicitud_id=None):
    """
    Grafica un gráfico de barras agrupadas comparando costo total, tiempo total y cantidad de tramos
    entre dos itinerarios: el optimizado por costo y el optimizado por tiempo.
    """
    plt.figure() 

    etiquetas = ["Costo total", "Tiempo total (min)"]
    valores_costo = [
        itinerario_costo.costo_total / 1000,
        itinerario_costo.tiempo_total,
    ]

    valores_tiempo = [
        itinerario_tiempo.costo_total / 1000,
        itinerario_tiempo.tiempo_total,
    ]

    n = len(etiquetas)
    x = np.arange(n)
    ancho = 0.35

    print(valores_costo)
    print(valores_tiempo)

    plt.figure(figsize=(8, 6))
    plt.bar(
        x - ancho / 2, valores_costo, ancho, label="Optimizado por Costo en miles de $"
    )
    plt.bar(x + ancho / 2, valores_tiempo, ancho, label="Optimizado por Tiempo")

    plt.xlabel("Categorías")
    plt.ylabel("Valor")
    titulo = "Comparación de Itinerarios: Costo vs Tiempo"
    if solicitud_id:
        titulo += f" (Solicitud {solicitud_id})"
    plt.title(titulo)
    plt.xticks(x, etiquetas)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.7)


def graficar_mapa_utilizacion(itinerarios, titulo="Mapa de utilización de la red"):
    """
    Dibuja un grafico de la red mostrando la utilización de cada conexión.
    - Los nodos son las ciudades.
    - Las aristas se dibujan más gruesas según cuántas veces se usaron en los itinerarios.
    """
    G = nx.DiGraph()
    edge_usage = {}

    # Contar cuántas veces se usa cada conexión
    for itinerario in itinerarios:
        for origen, destino, conexion in itinerario.get_tramos():
            key = (origen, destino)
            edge_usage[key] = edge_usage.get(key, 0) + 1
            G.add_node(origen)
            G.add_node(destino)
            G.add_edge(origen, destino)

    # Preparar pesos para las aristas
    all_weights = [edge_usage[edge] for edge in G.edges()]
    max_weight = max(all_weights) if all_weights else 1

    # Dibujar el grafo
    pos = nx.spring_layout(G, seed=42)  
    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Dibujar aristas con grosor proporcional al uso
    for edge in G.edges():
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[edge],
            width=1 + 4 * edge_usage[edge] / max_weight,
            alpha=0.7,
            edge_color="red"
        )

    plt.title(titulo)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
