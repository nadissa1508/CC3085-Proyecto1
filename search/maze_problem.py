"""
Implementación del problema del laberinto - Problema concreto para navegación en laberinto
"""
from search.problem import Problem


class MazeProblem(Problem):
    """
    Implementación concreta de Problem para navegación en laberinto.
    Representación de estado: tupla (fila, columna)
    """
    
    def __init__(self, grid, start_position, goal_positions):
        """
        Inicializar el problema del laberinto
        
        Args:
            grid: Lista 2D de objetos Tile de la discretización
            start_position: tupla (fila, col) para el inicio
            goal_positions: Lista de tuplas (fila, col) para las metas
        """
        super().__init__(start_position, goal_positions)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        
        # Movimientos posibles: arriba, abajo, izquierda, derecha y diagonales
        self.movements = [
            (-1, 0),   # arriba
            (1, 0),    # abajo
            (0, -1),   # izquierda
            (0, 1),    # derecha
            (-1, -1),  # arriba-izquierda
            (-1, 1),   # arriba-derecha
            (1, -1),   # abajo-izquierda
            (1, 1)     # abajo-derecha
        ]
    
    def actions(self, state):
        """
        Retornar lista de acciones de movimiento válidas desde la posición actual
        
        Args:
            state: tupla (fila, col)
            
        Returns:
            Lista de tuplas de movimiento válidas
        """
        row, col = state
        valid_actions = []
        
        for move in self.movements:
            new_row = row + move[0]
            new_col = col + move[1]
            
            # Verificar si está dentro de los límites
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                tile = self.grid[new_row][new_col]
                # Verificar si el tile es caminable (no es una pared)
                if tile.is_walkable():
                    valid_actions.append(move)
        
        return valid_actions
    
    def result(self, state, action):
        """
        Retornar el estado resultante de tomar una acción
        
        Args:
            state: tupla (fila, col)
            action: tupla (delta_fila, delta_col)
            
        Returns:
            Nueva tupla (fila, col)
        """
        row, col = state
        delta_row, delta_col = action
        return (row + delta_row, col + delta_col)
    
    def step_cost(self, state, action, next_state):
        """
        Costo de moverse desde state hasta next_state
        Para Task 1, asumir costo uniforme de 1 para todos los tiles no pared
        Los movimientos diagonales cuestan un poco más (sqrt(2) ≈ 1.414)
        
        Args:
            state: (fila, col) actual
            action: Movimiento tomado
            next_state: (fila, col) resultante
            
        Returns:
            Valor de costo
        """
        # Movimientos diagonales
        if abs(action[0]) + abs(action[1]) == 2:
            return 1.414  # sqrt(2)
        # Movimientos rectos
        return 1.0
    
    def heuristic(self, state):
        """
        Función heurística: distancia Manhattan a la meta más cercana
        Para búsqueda A*
        
        Args:
            state: tupla (fila, col)
            
        Returns:
            Valor heurístico (distancia a la meta más cercana)
        """
        row, col = state
        
        # Calcular distancia a todas las metas y retornar el mínimo
        min_distance = float('inf')
        for goal_row, goal_col in self.goal_states:
            # Distancia Euclidiana (mejor para matriz con diagonales)
            distance = ((row - goal_row) ** 2 + (col - goal_col) ** 2) ** 0.5
            min_distance = min(min_distance, distance)
        
        return min_distance
    
    def get_tile(self, state):
        """
        Obtener el tile en un estado dado
        
        Args:
            state: tupla (fila, col)
            
        Returns:
            Objeto Tile
        """
        row, col = state
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
