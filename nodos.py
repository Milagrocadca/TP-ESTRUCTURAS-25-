from conexion import Conexion

class Nodo:
    def __init__(self, nombre, modos):

        #nombre= Nombre de la ciudad
        #modos= modos de transporte habilitados (list o set)
        
        self.nombre = nombre
        self.modos = set(modos)
        self.conexiones = [] 

    
    def agregar_conexion(self, conexion): #agregar conexion:Conexion
        self.conexiones.append(conexion)

    def tiene_modo(self, modo):
        return modo in self.modos

    def __repr__(self):
        return f"Nodo({self.nombre}, modos={self.modos})"


#red de transporte> metodo de clase para una funcion de clase que agrega una conexion y reuna a los metodos de instancia de cada una clase (en este caso nodo)
#inicia;iza y agrega en nodo