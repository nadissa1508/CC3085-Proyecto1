"""
Representación de tile para la matriz discretizada.
Cada tile representa un grupo de píxeles en la imagen original.
"""

class TileType:
    """Clase tipo enum para representar diferentes tipos de tile"""
    FREE = 0      # Blanco - Camino libre
    WALL = 1      # Negro - Obstáculo
    START = 2     # Rojo - Punto de inicio
    GOAL = 3      # Verde - Estado meta
    
    @staticmethod
    def to_string(tile_type):
        """Convertir tipo de tile a representación string"""
        if tile_type == TileType.FREE:
            return "FREE"
        elif tile_type == TileType.WALL:
            return "WALL"
        elif tile_type == TileType.START:
            return "START"
        elif tile_type == TileType.GOAL:
            return "GOAL"
        return "UNKNOWN"


class Tile:
    """Representa un tile (lote de píxeles) en la matriz discretizada"""
    
    def __init__(self, row, col, tile_type, avg_color):
        """
        Inicializar un tile
        
        Args:
            row: Posición de fila en la matriz
            col: Posición de columna en la matriz
            tile_type: Tipo de tile (TileType)
            avg_color: Color RGB promedio del tile (tupla)
        """
        self.row = row
        self.col = col
        self.tile_type = tile_type
        self.avg_color = avg_color  # (R, G, B)
    
    def is_walkable(self):
        """Verificar si este tile puede ser atravesado"""
        return self.tile_type != TileType.WALL
    
    def is_goal(self):
        """Verificar si este tile es una meta"""
        return self.tile_type == TileType.GOAL
    
    def is_start(self):
        """Verificar si este tile es el inicio"""
        return self.tile_type == TileType.START
    
    def __repr__(self):
        return f"Tile({self.row}, {self.col}, {TileType.to_string(self.tile_type)})"
    
    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))
