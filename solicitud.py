import csv

from validaciones import *

class Solicitud:
    ids_usados = set()
    
    def __init__(self, id_carga: str, peso: float, origen: str, destino: str):
        if id_carga in Solicitud.ids_usados:
            raise ValueError('Ya existe una solicitud con ese ID')
        elif not validarPositivo(peso):
            raise ValueError("El peso del vehículo ingresado no se encuentra dentro de las opciones disponibles")

        self.id_carga = str(id_carga)
        self.peso = float(peso)
        self.origen = origen
        self.destino = destino

        Solicitud.ids_usados.add(id_carga)

    #GETTER
    def get_id(self): 
        return self.id_carga
    
    def get_peso(self): 
        return self.peso
    
    def get_origen(self): 
        return self.origen
    
    def get_destino(self): 
        return self.destino

    #SETTER
    def set_id(self, id_carga):
        if id_carga in Solicitud.ids_usados:
            raise ValueError('Ya existe una solicitud con ese ID')
        Solicitud.ids_usados.add(id_carga)
        self.id_carga = str(id_carga)

    def __repr__(self):
        return (f"Solicitud(ID={self.id_carga}, "
                f"Peso={self.peso} kg, "
                f"{self.origen} → {self.destino})")

    def dic_solicitud(self):
        return {
            "id": self.id_carga,
            "peso": self.peso,
            "origen": self.origen,
            "destino": self.destino
        }

 
@staticmethod
def cargar_solicitudes(path):
    solicitudes = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    id_carga = row['id']
                    peso = float(row['peso'])
                    origen = row['origen']
                    destino = row['destino']
                    solicitudes.append(Solicitud(id_carga, peso, origen, destino))
                except Exception as e:
                    raise ValueError(f"Error al procesar fila: {row} → {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    
    return solicitudes
