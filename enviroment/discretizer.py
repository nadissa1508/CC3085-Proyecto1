"""
Módulo discretizador - Convierte imagen continua en matriz discreta de tiles
"""
import numpy as np
from enviroment.tile import Tile, TileType


class Discretizer:
    """Convierte una imagen en una representación de matriz discreta"""
    
    def __init__(self, tile_size=10):
        """
        Inicializar el discretizador
        
        Args:
            tile_size: Tamaño de cada tile (tile_size x tile_size píxeles)
        """
        self.tile_size = tile_size
        self.grid = None
        self.start_position = None
        self.goal_positions = []
    
    def discretize(self, img_array):
        """
        Convertir array de imagen en matriz discreta de tiles
        
        Args:
            img_array: array numpy de forma (altura, ancho, 3) con valores RGB
            
        Returns:
            Lista 2D de objetos Tile
        """
        height, width = img_array.shape[0], img_array.shape[1]
        
        # Calcular dimensiones de la matriz
        grid_rows = height // self.tile_size
        grid_cols = width // self.tile_size
        
        # Inicializar matriz
        self.grid = [[None for _ in range(grid_cols)] for _ in range(grid_rows)]
        self.goal_positions = []
        
        # Procesar cada tile
        for row in range(grid_rows):
            for col in range(grid_cols):
                # Extraer región del tile
                start_y = row * self.tile_size
                end_y = start_y + self.tile_size
                start_x = col * self.tile_size
                end_x = start_x + self.tile_size
                
                tile_region = img_array[start_y:end_y, start_x:end_x]
                
                # Calcular color promedio
                avg_color = np.mean(tile_region, axis=(0, 1))
                avg_color = tuple(avg_color.astype(int))
                
                # Determinar tipo de tile
                tile_type = self._classify_tile(avg_color)
                
                # Crear tile
                tile = Tile(row, col, tile_type, avg_color)
                self.grid[row][col] = tile
                
                # Rastrear posiciones de inicio y meta
                if tile_type == TileType.START:
                    self.start_position = (row, col)
                elif tile_type == TileType.GOAL:
                    self.goal_positions.append((row, col))
        
        return self.grid
    
    def _classify_tile(self, avg_color):
        """
        Clasificar tipo de tile basado en color RGB promedio
        
        Args:
            avg_color: tupla (R, G, B)
            
        Returns:
            Constante TileType
        """
        r, g, b = avg_color
        
        # Negro (Pared) - [0, 0, 0] con tolerancia
        if r < 30 and g < 30 and b < 30:
            return TileType.WALL
        
        # Rojo (Inicio) - Rojo alto, verde y azul bajos (umbral relajado)
        if r > 120 and g < 100 and b < 100 and r > g and r > b:
            return TileType.START
        
        # Verde (Meta) - Verde alto, rojo y azul bajos (umbral relajado)
        if g > 120 and r < 100 and b < 100 and g > r and g > b:
            return TileType.GOAL
        
        # Blanco u otros colores (Camino libre)
        return TileType.FREE
    
    def get_start_position(self):
        """Obtener la posición de inicio (fila, columna)"""
        return self.start_position
    
    def get_goal_positions(self):
        """Obtener lista de posiciones meta [(fila, columna), ...]"""
        return self.goal_positions
    
    def get_grid_dimensions(self):
        """Obtener dimensiones de la matriz (filas, columnas)"""
        if self.grid is None:
            return 0, 0
        return len(self.grid), len(self.grid[0]) if self.grid else 0
    
    def get_tile(self, row, col):
        """Obtener tile en posición específica"""
        if self.grid is None or row < 0 or col < 0:
            return None
        if row >= len(self.grid) or col >= len(self.grid[0]):
            return None
        return self.grid[row][col]
