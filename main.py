from red import Red
from vehiculos import Vehiculos
from solicitud import Solicitud


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
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
            tipos_vehiculos.addVehiculo()

        if opcion == "2":
            # tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
            print(tipos_vehiculos.removeVehiculo())

        if opcion == "3":
            # tipo, modo, velocidad, capacidad, costo_fijo, costo_km, costo_kg
            print(tipos_vehiculos.getListVehiculos())
            
        if opcion=="4":
            archivo = input('Ingrese el archivo: ')
            solicitudes = Solicitud.cargar_solicitudes(archivo)
            from planificador import Planificador  # Importa aquí para evitar ciclos si es necesario
            planificador = Planificador(red_nodos.get_red(), tipos_vehiculos.getListVehiculos())
            for solicitud in solicitudes:
                itinerario = planificador.planificar(solicitud)
                if itinerario:
                    print(itinerario)
                else:
                    print(f"No se encontró itinerario para la solicitud {solicitud.get_id()}")
            
        if opcion == "5":
            flag = False


if __name__ == "__main__":
    main()
    