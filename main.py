import red
import vehiculos


def main():
    red_nodos = red.Red()
    tipos_vehiculos = vehiculos.Vehiculos()
    print(red_nodos.get_red())

    flag = True
    while flag:
        print("\n===== MENÚ PLANIFICADOR =====")
        print("1. Agregar vehiculo")
        print("2. Remover vehiculo")
        print("3. Ver lista vehiculos")
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

        if opcion == "5":
            flag = False


if __name__ == "__main__":
    main()
