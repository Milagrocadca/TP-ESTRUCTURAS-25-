from vehiculo import *
from conexion import *
from itinerario import *
#GRAFICO DE LINEA
import matplotlib.pyplot as plt
def graficar_distancia_vs_tiempo(itinerario):
    # Obtener los tramos del itinerario
    tramos = itinerario.get_tramos()
    vehiculo = itinerario.get_vehiculo()

    distancias = []
    tiempos = []
    distancia_acumulada = 0
    tiempo_acumulado = 0

    for origen, destino, conexion in tramos:
        distancia = conexion.get_distancia()
        tiempo = vehiculo.calcular_tiempo(distancia, conexion.get_vel_max())
        distancia_acumulada += distancia
        tiempo_acumulado += tiempo
        distancias.append(distancia_acumulada)
        tiempos.append(tiempo_acumulado)
        print(f"Tiempo: {tiempo_acumulado:.2f} min, Distancia: {distancia_acumulada:.2f} km")

    plt.plot(tiempos, distancias, marker='o')
    plt.xlabel('Tiempo acumulado (minutos)')
    plt.ylabel('Distancia acumulada (km)')
    plt.title('Distancia acumulada vs Tiempo')
    plt.grid(True)
    plt.show()

def graficar_costo_vs_distancia(itinerario):
    tramos = itinerario.get_tramos()
    vehiculo = itinerario.get_vehiculo()

    distancias = []
    costos = []
    distancia_acumulada = 0
    costo_acumulado = 0

    for origen, destino, conexion in tramos:
        distancia = conexion.get_distancia()
        peso = itinerario.get_solicitud().get_peso() if hasattr(itinerario, "get_solicitud") else 0
        costo = vehiculo.calcular_costo_total(distancia, peso)
        distancia_acumulada += distancia
        costo_acumulado += costo
        distancias.append(distancia_acumulada)
        costos.append(costo_acumulado)
        print(f"Distancia: {distancia_acumulada:.2f} km, Costo acumulado: {costo_acumulado:.2f}")

    plt.plot(distancias, costos, marker='o', color='red')
    plt.xlabel('Distancia acumulada (km)')
    plt.ylabel('Costo acumulado')
    plt.title('Costo acumulado vs Distancia')
    plt.grid(True)
    plt.show()