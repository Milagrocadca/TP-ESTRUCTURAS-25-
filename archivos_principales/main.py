from red import Red
from vehiculos import Vehiculos
from solicitud import Solicitud
from graficos import graficar_distancia_vs_tiempo, graficar_costo_vs_distancia, graficar_comparacion_itinerarios, graficar_mapa_utilizacion
from planificador import Planificador
import matplotlib.pyplot as plt

def pedir_archivos_red():
    while True:
        archivo_nodos = input("Ingrese el nombre del archivo de nodos: ").strip()
        archivo_conexiones = input("Ingrese el nombre del archivo de conexiones: ").strip()
        try:
            red_nodos = Red(archivo_nodos, archivo_conexiones)
            tiene_conexiones = any(
                len(nodo.conexiones) > 0 for nodo in red_nodos.get_red().values()
            )
            if not tiene_conexiones:
                print("No se cargaron conexiones válidas. Verifique el archivo de conexiones.")
            else:
                return red_nodos
        except FileNotFoundError as e:
            print(f"Archivo no encontrado: {e}. Intente nuevamente.")
        except ValueError as e:
            print(f"Error en los datos del archivo: {e}. Intente nuevamente.")
        except Exception as e:
            print(f"Error al cargar la red: {e}. Intente nuevamente.")

def menu_vehiculos(tipos_vehiculos):
    finalizado = False
    while not finalizado:
        print("\n===== MENÚ DE VEHÍCULOS =====")
        print("1. Agregar vehículo")
        print("2. Remover vehículo")
        print("3. Ver lista de vehículos")
        print("4. Finalizar carga de vehículos")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("\nSeleccione una opción para agregar:")
            print("a) Camión")
            print("b) Tren de Carga")
            print("c) Avión")
            print("d) Barco (fluvial)")
            print("e) Barco (maritimo)")
            op = input("Opción (a/b/c/d/e): ").strip().lower()
            try:
                tipos_vehiculos.addVehiculo(op)
                print("Vehículo agregado correctamente.")
            except ValueError as e:
                print(e)
        elif opcion == "2":
            print("\nSeleccione una opción para eliminar:")
            print("a) Camión")
            print("b) Tren de Carga")
            print("c) Avión")
            print("d) Barco (fluvial)")
            print("e) Barco (maritimo)")
            op = input("Opción (a/b/c/d/e): ").strip().lower()
            if tipos_vehiculos.removeVehiculo(op):
                print("Vehículo eliminado correctamente.")
            else:
                print("El tipo de vehículo a eliminar no existe o la opción no es válida.")
        elif opcion == "3":
            tipos_vehiculos.printVehiculos()
        elif opcion == "4":
            if not any(tipos_vehiculos.getListVehiculos()):
                print("Debe cargar al menos un vehículo antes de continuar.")
            else:
                finalizado = True
        else:
            print("Opción no válida.")

def main():
    red_nodos = pedir_archivos_red()
    tipos_vehiculos = Vehiculos()

    # Paso 1: Cargar vehículos
    menu_vehiculos(tipos_vehiculos)

    # Paso 2: Cargar solicitudes
    solicitudes = []
    while not solicitudes:
        path = input("\nIngrese la ruta del archivo de solicitudes: ")
        try:
            solicitudes = Solicitud.cargar_solicitudes(path)
        except FileNotFoundError as e:
            print(f"Archivo no encontrado: {e}")
        except ValueError as e:
            print(f"Error en los datos del archivo: {e}")
    print(f"Se cargaron {len(solicitudes)} solicitudes correctamente.")

    # Paso 3: Planificar y mostrar resultados
    planificador = Planificador(red_nodos.get_red(), tipos_vehiculos.getInfoVehiculos())
    itinerarios = []
    for solicitud in solicitudes:
        itinerario_costo = planificador.planificar(solicitud, kpi="costo")
        itinerario_tiempo = planificador.planificar(solicitud, kpi="tiempo")
        itinerario_aleatorio = planificador.planificar(solicitud, kpi="aleatorio")
        itinerarios.append((solicitud, itinerario_costo, itinerario_tiempo, itinerario_aleatorio))

        if not itinerario_costo and not itinerario_tiempo and not itinerario_aleatorio:
            print(f"No se encontró itinerario para la solicitud {solicitud.get_id()}")
        else:
            if (
                itinerario_costo
                and itinerario_tiempo
                and itinerario_costo.get_tramos() == itinerario_tiempo.get_tramos()
            ):
                print(f"\nRuta única óptima para solicitud {solicitud.get_id()} (minimiza tiempo y costo):\n")
                print(itinerario_costo)
            else:
                if itinerario_costo:
                    print(f"\nRuta más barata para solicitud {solicitud.get_id()}:\n")
                    print(itinerario_costo)
                if itinerario_tiempo:
                    print(f"\nRuta más rápida para solicitud {solicitud.get_id()}:\n")
                    print(itinerario_tiempo)
            if itinerario_aleatorio:
                print(f"\nRuta aleatoria (máx 3 tramos) para solicitud {solicitud.get_id()}:\n")
                print(itinerario_aleatorio)

    # Paso 4: Mostrar gráficos
    mostrar_graficos = False
    while not mostrar_graficos:
        print("1. Mostrar los gráficos de los itinerarios creados")
        print("2. Mostrar mapa de utilización de la red")
        print("3. Salir")
        op = input("Seleccione una opción: ")
        if op == "1":
            for solicitud, itinerario_costo, itinerario_tiempo, itinerario_aleatorio in itinerarios:
                solicitud_id = solicitud.get_id()
                if not itinerario_costo and not itinerario_tiempo:
                    print(f"No se encontró itinerario para la solicitud {solicitud.get_id()}")
                else:
                    if (
                        itinerario_costo
                        and itinerario_tiempo
                        and itinerario_costo.get_tramos() == itinerario_tiempo.get_tramos()
                    ):
                        print(f"\nMostrando los gráficos para la solicitud {solicitud.get_id()} (óptima en costo y tiempo):")
                        graficar_distancia_vs_tiempo(itinerario_costo, solicitud_id)
                        graficar_costo_vs_distancia(itinerario_costo, solicitud_id)
                    else:
                        if itinerario_costo:
                            print(f"\nMostrando los gráficos para la solicitud {solicitud.get_id()} (óptima en costo):")
                            graficar_distancia_vs_tiempo(itinerario_costo, solicitud_id)
                            graficar_costo_vs_distancia(itinerario_costo, solicitud_id)
                        if itinerario_tiempo:
                            print(f"\nMostrando los gráficos para la solicitud {solicitud.get_id()} (óptima en tiempo):")
                            graficar_distancia_vs_tiempo(itinerario_tiempo, solicitud_id)
                            graficar_costo_vs_distancia(itinerario_tiempo, solicitud_id)
                        if (
                            itinerario_costo
                            and itinerario_tiempo
                            and itinerario_costo.get_tramos() != itinerario_tiempo.get_tramos()
                        ):
                            print(f"\nMostrando gráfico comparativo para la solicitud {solicitud.get_id()}:")
                            graficar_comparacion_itinerarios(itinerario_costo, itinerario_tiempo, solicitud_id)
            plt.show()
        elif op == "2":
            itinerarios_planos = []
            for _, it_costo, it_tiempo, it_aleatorio in itinerarios:
                for it in [it_costo, it_tiempo, it_aleatorio]:
                    if it and it not in itinerarios_planos:
                        itinerarios_planos.append(it)
            if itinerarios_planos:
                graficar_mapa_utilizacion(itinerarios_planos, titulo="Mapa de utilización de la red")
                plt.show()
            else:
                print("No hay itinerarios para graficar el mapa de utilización.")
        elif op == "3":
            print("Saliendo del programa.")
            mostrar_graficos = True
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
