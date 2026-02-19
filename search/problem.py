"""
Clase abstracta de problema - Framework para definir problemas de búsqueda
"""
from abc import ABC, abstractmethod


class Problem(ABC):
    """
    Clase abstracta que representa un problema de búsqueda formal.
    Las subclases deben implementar todos los métodos abstractos.
    """
    
    def __init__(self, initial_state, goal_states):
        """
        Inicializar el problema
        
        Args:
            initial_state: El estado inicial
            goal_states: Lista de estados meta (o un solo estado meta)
        """
        self.initial_state = initial_state
        # Asegurar que goal_states es una lista
        if not isinstance(goal_states, list):
            self.goal_states = [goal_states]
        else:
            self.goal_states = goal_states
    
    @abstractmethod
    def actions(self, state):
        """
        Retornar lista de acciones válidas desde el estado dado
        
        Args:
            state: Estado actual
            
        Returns:
            Lista de acciones válidas
        """
        pass
    
    @abstractmethod
    def result(self, state, action):
        """
        Retornar el estado resultante de tomar una acción en un estado
        
        Args:
            state: Estado actual
            action: Acción a tomar
            
        Returns:
            Estado resultante
        """
        pass
    
    @abstractmethod
    def step_cost(self, state, action, next_state):
        """
        Retornar el costo de tomar una acción desde state hasta next_state
        
        Args:
            state: Estado actual
            action: Acción tomada
            next_state: Estado resultante
            
        Returns:
            Costo (numérico)
        """
        pass
    
    def goal_test(self, state):
        """
        Verificar si un estado es un estado meta
        
        Args:
            state: Estado a verificar
            
        Returns:
            Booleano indicando si el estado es meta
        """
        return state in self.goal_states
    
    @abstractmethod
    def heuristic(self, state):
        """
        Función heurística para búsqueda informada (ej. A*)
        
        Args:
            state: Estado a evaluar
            
        Returns:
            Valor heurístico (numérico)
        """
        pass
