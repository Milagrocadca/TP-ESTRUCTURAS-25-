from collections import deque

import numpy as np
from solicitud import Solicitud
from red import cargar_nodos, cargar_conexiones
from mapa_vehiculos import CLASES_VEHICULO

def main():
    #resultado = Itinerario()

    archivo_solicitudes = "solicitudes.csv"
    archivo_nodos = "nodos.csv"
    archivo_conexiones = "conexiones.csv"

    seguir=True
    while seguir:
        print("\n===== MENÚ PLANIFICADOR =====")
        print("1. Agregar tarea")
        print("2. Mostrar tareas")
        print("3. Completar tarea")
        print("4. Ver historial")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id = int(input("ID de la tarea: "))
                descripcion = input("Descripción: ")
                prioridad = input("Prioridad (alta/media/baja): ").lower()
                resultado.agregar(id, descripcion, prioridad)
            except ValueError:
                print("ID debe ser un número entero.")

        elif opcion == "2":
            resultado.mostrar()

        elif opcion == "3":
            try:
                id = int(input("ID de la tarea a completar: "))
                resultado.completar(id)
            except ValueError:
                print("ID inválido.")
        
        elif opcion == "4":
            resultado.historial()

        elif opcion == "5":
            print("Saliendo del planificador.")
            seguir=False

        else:
            print("Opción inválida. Intente de nuevo.")

        #abrir archivos y cargar datos
        try:
            for archivo in [archivo_solicitudes, archivo_nodos, archivo_conexiones]:
                if not os.path.exists(archivo):
                    print(f"Archivo no encontrado: {archivo}")
                    return
            # Cargar nodos y conexiones
            print("Cargando nodos y conexiones")
            nodos = cargar_nodos(archivo_nodos)
            cargar_conexiones(archivo_conexiones, nodos)

            # Mostrar nodos y conexiones
            print("\nRed de transporte:")
            for nombre, nodo in nodos.items():
                print(f"{nombre} ({', '.join(nodo.get_modos())})")
                for conexion in nodo.get_conexiones():
                    print(f"   → {conexion.get_destino()} | {conexion}")

            # Cargar solicitudes
            print("\nCargando solicitudes...")
            solicitudes = Solicitud.cargar_solicitudes(archivo_solicitudes)
            for s in solicitudes:
                print(f"{s}")

            # Crear vehículos disponibles
            print("\n Vehículos disponibles:")
            vehiculos = [
                CLASES_VEHICULO["camion"](),
                CLASES_VEHICULO["tren"](),
                CLASES_VEHICULO["avion"](mal_tiempo=True),
                CLASES_VEHICULO["barcaza"](tipo_agua="mar")
            ]
            for v in vehiculos:
                print(f" {v}")
            print("\n Sistema inicializado correctamente.")

        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            
            


# -------------------- EJECUCIÓN --------------------

if __name__ == "__main__":
    main()
    

#crear e importar nodos y conexiones
# Crear los nodos
nodos = {}
for nombre in nodos_df["nombre"]:
    nodos[nombre] = Nodo(nombre)

# Crear y agregar las conexiones
for _, row in conexiones_df.iterrows():
    origen = nodos[row["origen"]]
    destino = nodos[row["destino"]]
    tipo = row["tipo"]
    distancia = row["distancia_km"]
    restriccion = row["restriccion"] if pd.notna(row["restriccion"]) else None
    valor = row["valor_restriccion"] if pd.notna(row["valor_restriccion"]) else None

    conexion = Conexion(origen, destino, tipo, distancia, restriccion, valor)
    origen.agregar_conexion(conexion)

    # Si la conexión es bidireccional (por defecto), agregar la inversa
    conexion_inversa = Conexion(destino, origen, tipo, distancia, restriccion, valor)
    destino.agregar_conexion(conexion_inversa)

# Ejemplo: imprimir conexiones desde "Zarate"
for conexion in nodos["Zarate"].conexiones:
    print(conexion)