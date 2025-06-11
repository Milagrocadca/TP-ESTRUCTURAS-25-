from red import Red
from vehiculos import *
from solicitud import Solicitud
from conexion import Conexion
from graficos import *
from planificador import Planificador

def main():
    red_nodos = Red()
    tipos_vehiculos = Vehiculos()
    print(red_nodos.get_red())

    flag = True
    while flag:
        print("\n===== MENÚ PLANIFICADOR =====")
        print("1. Agregar vehiculo")
        print("2. Remover vehiculo")
        print("3. Ver lista vehiculos")
        print("4. Agregar solicitud")
        print("5. Mostrar graficos de los itinerarios creados")
        print("6. Salir")
        

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
            tipos_vehiculos.addVehiculo()

        if opcion == "2":
            # tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
            print(tipos_vehiculos.removeVehiculo())

        if opcion == "3":
            # tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
            tipos_vehiculos.printVehiculos()


        if opcion=="4":
            archivo='solicitudes.csv'
            planificador = Planificador(
                red_nodos.get_red(), tipos_vehiculos.getInfoVehiculos()
            )
            solicitudes = Solicitud.cargar_solicitudes(archivo)
            for solicitud in solicitudes:
                itinerario_costo = planificador.planificar(solicitud, kpi="costo")
                itinerario_tiempo = planificador.planificar(solicitud, kpi="tiempo")

                if not itinerario_costo and not itinerario_tiempo:
                    print(f"No se encontró itinerario para la solicitud {solicitud.get_id()}")
                    continue

                if (
                    itinerario_costo
                    and itinerario_tiempo
                    and itinerario_costo.get_tramos() == itinerario_tiempo.get_tramos()
                ):
                    print(f"\n Ruta única óptima para solicitud {solicitud.get_id()} (minimiza tiempo y costo):\n")
                    print(itinerario_costo)
                else:
                    if itinerario_costo:
                        print(f"\n Ruta más barata para solicitud {solicitud.get_id()}:\n")
                        print(itinerario_costo)
                    if itinerario_tiempo:
                        print(f"\n Ruta más rápida para solicitud {solicitud.get_id()}:\n")
                        print(itinerario_tiempo)

        """if opcion == "4":
            archivo = 'solicitudes.csv'  # input("Ingrese el archivo: ")
            solicitudes = Solicitud.cargar_solicitudes(archivo)
            from planificador import (
                Planificador,
            )  # Importa aquí para evitar ciclos si es necesario

            planificador = Planificador(
                red_nodos.get_red(), tipos_vehiculos.getInfoVehiculos()
            )
            for solicitud in solicitudes:
                itinerario = planificador.planificar(solicitud)
                if itinerario:
                    print(itinerario)
                else:
                    print(
                        f"No se encontró itinerario para la solicitud {solicitud.get_id()}"
                    )"""

            
        if opcion == "5":
            print("Buscando los graficos...")
            
            if itinerario_costo and itinerario_tiempo:
                if itinerario_costo==itinerario_tiempo:
                    print("Mostrando los graficos de...")
                    print("---Itinerario de costo y tiempo a la vez---")
                    graficar_distancia_vs_tiempo(itinerario_costo)
                    graficar_costo_vs_distancia(itinerario_costo)
                else:
                    print("Mostrando la comparacion de graficos de itinerario costo y tiempo...")
                    graficar_comparacion_itinerarios(itinerario_costo, itinerario_tiempo)
                    
                    print("Mostrando los graficos de...")
                    print("---Itinerario de costo---")
                    graficar_distancia_vs_tiempo(itinerario_costo)
                    graficar_costo_vs_distancia(itinerario_costo)
                    
                    print("Mostrando los graficos de...")
                    print("\n---Itinerario de tiempo---")
                    graficar_distancia_vs_tiempo(itinerario_tiempo)
                    graficar_costo_vs_distancia(itinerario_tiempo)


            elif itinerario_costo:
                print("Mostrando los graficos de...")
                print("---Itinerario de costo---")
                graficar_distancia_vs_tiempo(itinerario_costo)
                graficar_costo_vs_distancia(itinerario_costo)

            elif itinerario_tiempo:
                print("Mostrando los graficos de...")
                print("\n---Itinerario de tiempo---")
                graficar_distancia_vs_tiempo(itinerario_tiempo)
                graficar_costo_vs_distancia(itinerario_tiempo)

            archivo='solicitudes.csv'
            planificador = Planificador(
                red_nodos.get_red(), tipos_vehiculos.getInfoVehiculos()
            )
            solicitudes = Solicitud.cargar_solicitudes(archivo)
            itinerarios_validos = []
            for solicitud in solicitudes:
                itinerario = planificador.planificar(solicitud, kpi="costo")
                if itinerario:
                    itinerarios_validos.append(itinerario)
            if itinerarios_validos:
                print("Mostrando graficos de itinerarios validos...")
                graficar_costo_total_vs_modo(itinerarios_validos)
                graficar_tiempo_total_vs_modo(itinerarios_validos)
            else:
                print("No hay itinerarios válidos para graficar.")

        if opcion == "6":
            flag = False


if __name__ == "__main__":
    main()
