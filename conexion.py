class Conexion:
    
    def __init__(self, tipo:int, distancia:int , destino: int, modo:int, vel_max=None, peso_max=None, calado_max=None):
        
        self.tipo=tipo
        self.distancia=float(distancia)
        self.destino=destino
        self.modo=modo.lower()
        self.vel_max = float(vel_max) if vel_max else None
        self.peso_max = float(peso_max)  if peso_max else None
        self.calado_max = float(calado_max) if calado_max else None
        
       
    def __eq__(self, other): #depende de id si o no
        if not isinstance(other, Conexion):
            return False
        return self.origen == other.origen and self.destino==other.destino

    def __str__(self): #no tiene id
        return (f"Conexion(tipo={self.tipo}, distancia={self.distancia}km, destino={self.destino}, modo={self.modo}, vel_max={self.vel_max}, peso_max={self.peso_max}, calado_max={self.calado_max}, tasa={self.tasa})")
    
class ConexionFluvial(Conexion):
    def __init__(self, tipo, distancia, destino, vel_max=None, peso_max=None, calado_max=None):
        super().__init__(tipo, distancia, destino, modo="maritimo", vel_max=vel_max,
                         peso_max=peso_max, calado_max=calado_max)
        self.tipo_agua = "fluvial"

    def __str__(self):
        return super().__str__()[:-1] + f", tipo_agua={self.tipo_agua})"

class ConexionMaritima(Conexion):
    def __init__(self, tipo, distancia, destino, vel_max=None, peso_max=None, calado_max=None):
        super().__init__(tipo, distancia, destino, modo="maritimo", vel_max=vel_max,
                         peso_max=peso_max, calado_max=calado_max)
        self.tipo_agua = "maritimo"

    def __str__(self):
        return super().__str__()[:-1] + f", tipo_agua={self.tipo_agua})"


#prueba = Conexion(1, 100, 2, "terrestre", vel_max=80, peso_max=1000)
# print(prueba)