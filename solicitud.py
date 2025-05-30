import csv
from validaciones import *

class Solicitud:
    ids_usados=set()
    
    def __init__(self, id_carga:str, peso:float, origen:str, destino:str):
        if id_carga in Solicitud.ids_cargas:
            raise ValueError('Ya una solicitud con ese ID')
        
        elif not validarPositivo(peso):
            raise ValueError ("El peso del vehiculo ingresado no se encentra dentro de las opciones disponibles")

        self.id_carga = str(id_carga)
        self.peso = float(peso)
        self.origen = origen
        self.destino = destino

        Solicitud.ids_usados.add(id_carga)

    def __repr__(self):
        return (f"Solicitud(ID={self.id_carga}, "
                f"Peso={self.peso} kg, "
                f"{self.origen} → {self.destino})")

    def dic_solicitud(self): #STR??
       
        return {
            "id": self.id_carga,
            "peso": self.peso,
            "origen": self.origen,
            "destino": self.destino
        }


    
    def cargar_solicitudes(path):
        solicitudes = []
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                solicitudes.append(Solicitud(
                    row['id'], row['peso'], row['origen'], row['destino']
                ))
        return solicitudes
