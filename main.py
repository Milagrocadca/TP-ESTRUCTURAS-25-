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
    ejecutado = False
    seguir = True
    while seguir:
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
            tipos_vehiculos.removeVehiculo()

        if opcion == "3":
            # tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
            tipos_vehiculos.printVehiculos()
            

        if opcion == "4":
            if not ejecutado:
                ejecutado = True

                solicitudes = []
                while not solicitudes:
                    path = input("Ingrese la ruta del archivo de solicitudes: ")
                    try:
                        solicitudes = Solicitud.cargar_solicitudes(path)
                    except FileNotFoundError as e:
                        print(f"Archivo no encontrado: {e}")
                    except ValueError as e:
                        print(f"Error en los datos del archivo: {e}")
                    # el while sigue automáticamente si 'solicitudes' sigue vacío

                if solicitudes:
                    print(f"Se cargaron {len(solicitudes)} solicitudes correctamente.")
                    # Podés continuar con el resto del código aquí
                
                planificador = Planificador(
                    red_nodos.get_red(), tipos_vehiculos.getInfoVehiculos()
                )

                for solicitud in solicitudes:
                    itinerario_costo = planificador.planificar(solicitud, kpi="costo")
                    itinerario_tiempo = planificador.planificar(solicitud, kpi="tiempo")

                    if not itinerario_costo and not itinerario_tiempo:
                        print(
                            f"No se encontró itinerario para la solicitud {solicitud.get_id()}"
                        )
                    else:
                        if (
                            itinerario_costo
                            and itinerario_tiempo
                            and itinerario_costo.get_tramos() == itinerario_tiempo.get_tramos()
                        ):
                            print(
                                f"\nRuta única óptima para solicitud {solicitud.get_id()} (minimiza tiempo y costo):\n"
                            )
                            print(itinerario_costo)
                        else:
                            if itinerario_costo:
                                print(
                                    f"\nRuta más barata para solicitud {solicitud.get_id()}:\n"
                                )
                                print(itinerario_costo)
                            if itinerario_tiempo:
                                print(
                                    f"\nRuta más rápida para solicitud {solicitud.get_id()}:\n"
                                )
                                print(itinerario_tiempo)
            else:
                print('Ya ha enviado una solicitud. Toque la opcion 6 para salir.')

        if opcion == "5":
            print("\nBuscando los graficos...")
            if ejecutado:
                if itinerario_costo and itinerario_tiempo:
                    if (itinerario_costo.get_tramos() == itinerario_tiempo.get_tramos()
                    ):
                        print("\nMostrando los graficos de...")
                        print("\n===== Itinerario de costo y tiempo a la vez =====")
                        graficar_distancia_vs_tiempo(itinerario_costo)
                        graficar_costo_vs_distancia(itinerario_costo)
                    else:
                        print(
                            "\nMostrando la comparacion de graficos de itinerario costo y tiempo..."
                        )
                        graficar_comparacion_itinerarios(
                            itinerario_costo, itinerario_tiempo
                        )

                        print("\nMostrando los graficos de...")
                        print("\n===== Itinerario de costo =====")
                        graficar_distancia_vs_tiempo(itinerario_costo)
                        graficar_costo_vs_distancia(itinerario_costo)

                        print("\nMostrando los graficos de...")
                        print("\n===== Itinerario de tiempo =====")
                        graficar_distancia_vs_tiempo(itinerario_tiempo)
                        graficar_costo_vs_distancia(itinerario_tiempo)

                elif itinerario_costo:
                    print("\nMostrando los graficos de...")
                    print("\n===== Itinerario de costo =====")
                    graficar_distancia_vs_tiempo(itinerario_costo)
                    graficar_costo_vs_distancia(itinerario_costo)

                elif itinerario_tiempo:
                    print("\nMostrando los graficos de...")
                    print("\n===== Itinerario de tiempo =====")
                    graficar_distancia_vs_tiempo(itinerario_tiempo)
                    graficar_costo_vs_distancia(itinerario_tiempo)

                itinerarios_validos = planificador.get_itinerarios_validos()
                if itinerarios_validos:
                    print("\nMostrando graficos de itinerarios validos...")
                    graficar_costo_total_vs_modo(itinerarios_validos)
                    graficar_tiempo_total_vs_modo(itinerarios_validos)
                else:
                    print("\nNo hay itinerarios válidos para graficar.")
            else:
                print("Primero ejecuta la opción 4.")

        if opcion == "6":
            seguir = False


if __name__ == "__main__":
    main()