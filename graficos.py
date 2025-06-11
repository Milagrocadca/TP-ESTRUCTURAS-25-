from vehiculo import *
from conexion import *
from itinerario import *
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np


def graficar_distancia_vs_tiempo(itinerario):
    # Obtener los tramos del itinerario
    tramos = itinerario.get_tramos()
    vehiculo = itinerario.get_vehiculo()

    print(tramos)

    distancias = [0]
    tiempos = [0]
    distancia_acumulada = 0
    tiempo_acumulado = 0

    for origen, destino, conexion in tramos:
        distancia = conexion.get_distancia()
        tiempo = vehiculo.calcular_tiempo(distancia, conexion.get_vel_max())
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
    plt.title("Distancia acumulada vs Tiempo")
    plt.grid(True)
    plt.show()


def graficar_costo_vs_distancia(itinerario):
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
    plt.title("Costo acumulado vs Distancia")
    plt.grid(True)
    plt.show()


def graficar_costo_total_vs_modo(itinerarios_validos):
    """
    Agrupa por modo y suma el costo total de todos los itinerarios de ese modo.
    """
    modo_costos = defaultdict(float)
    for itinerario in itinerarios_validos:
        vehiculo = itinerario.get_vehiculo()
        modo = (
            vehiculo.get_modo()
            if hasattr(vehiculo, "get_modo")
            else vehiculo.get_tipo()
        )
        modo_costos[modo] += itinerario.costo_total

    modos = list(modo_costos.keys())
    costos = list(modo_costos.values())

    plt.figure(figsize=(8, 5))
    plt.bar(modos, costos, color="skyblue")
    plt.xlabel("Modo de transporte")
    plt.ylabel("Costo total")
    plt.title("Costo total vs. Modo de transporte")
    plt.grid(axis="y")
    plt.show()


def graficar_tiempo_total_vs_modo(itinerarios_validos):
    from collections import defaultdict

    modo_tiempos = defaultdict(float)
    for itinerario in itinerarios_validos:
        vehiculo = itinerario.get_vehiculo()
        modo = (
            vehiculo.get_modo()
            if hasattr(vehiculo, "get_modo")
            else vehiculo.get_tipo()
        )
        modo_tiempos[modo] += itinerario.tiempo_total

    modos = list(modo_tiempos.keys())
    tiempos = list(modo_tiempos.values())

    plt.figure(figsize=(8, 5))
    plt.bar(modos, tiempos, color="orange")
    plt.xlabel("Modo de transporte")
    plt.ylabel("Tiempo total (minutos)")
    plt.title("Tiempo total vs. Modo de transporte")
    plt.grid(axis="y")
    plt.show()


def graficar_comparacion_itinerarios(itinerario_costo, itinerario_tiempo):
    """
    Grafica un gráfico de barras agrupadas comparando costo total, tiempo total y cantidad de tramos
    entre dos itinerarios: el optimizado por costo y el optimizado por tiempo.
    """
    etiquetas = ["Costo total", "Tiempo total (min)", "Cantidad de tramos"]
    valores_costo = [
        itinerario_costo.costo_total / 1000,
        itinerario_costo.tiempo_total,
        len(itinerario_costo.get_tramos()),
    ]
    valores_tiempo = [
        itinerario_tiempo.costo_total / 1000,
        itinerario_tiempo.tiempo_total,
        len(itinerario_tiempo.get_tramos()),
    ]

    n = len(etiquetas)
    x = np.arange(n)
    ancho = 0.35

    print(valores_costo)
    print(valores_tiempo)

    # Crear el gráfico
    plt.figure(figsize=(8, 6))
    plt.bar(
        x - ancho / 2, valores_costo, ancho, label="Optimizado por Costo en miles de $"
    )
    plt.bar(x + ancho / 2, valores_tiempo, ancho, label="Optimizado por Tiempo")

    # Etiquetas y leyenda
    plt.xlabel("Categorías")
    plt.ylabel("Valor")
    plt.title("Comparación de Itinerarios: Costo vs Tiempo")
    plt.xticks(x, etiquetas)
    plt.legend()
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()