class Conexion:
    def __init__(self, origen, destino, tipo, distancia_km, restriccion=None, valor_restriccion=None):
        self.origen = origen
        self.destino = destino
        self.tipo = tipo  # Ej: "Ferroviaria", "Automotor", "Fluvial", "Aerea"
        self.distancia = float(distancia_km)
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion

        # Inicializa restricciones específicas
        self.vel_max = float(valor_restriccion) if restriccion == "velocidad_max" else None
        self.peso_max = float(valor_restriccion) if restriccion == "peso_max" else None
        self.tipo_agua = valor_restriccion if restriccion == "tipo" else None
        self.prob_mal_tiempo = float(valor_restriccion) if restriccion == "prob_mal_tiempo" else None

    def __eq__(self, other):
        if not isinstance(other, Conexion):
            return False
        return self.origen == other.origen and self.destino == other.destino and self.tipo == other.tipo

    def __str__(self):
        return (f"Conexion({self.origen} → {self.destino}, tipo={self.tipo}, distancia={self.distancia}km, "
                f"restriccion={self.restriccion}, valor={self.valor_restriccion})")