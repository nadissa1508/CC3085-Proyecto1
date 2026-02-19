"""
Estrategias de búsqueda e implementaciones de frontier
"""
from collections import deque
import heapq


class Frontier:
    """Clase base para estructuras de datos frontier"""
    
    def add(self, node):
        """Agregar un nodo a la frontier"""
        raise NotImplementedError
    
    def remove(self):
        """Remover y retornar un nodo de la frontier"""
        raise NotImplementedError
    
    def is_empty(self):
        """Verificar si la frontier está vacía"""
        raise NotImplementedError
    
    def contains_state(self, state):
        """Verificar si un estado está en la frontier"""
        raise NotImplementedError
    
    def can_replace(self, node):
        """Verificar si podemos reemplazar un nodo con mejor costo de camino"""
        return False
    
    def replace(self, node):
        """Reemplazar nodo con mejor costo de camino"""
        pass


class QueueFrontier(Frontier):
    """Cola FIFO para Búsqueda en Amplitud"""
    
    def __init__(self):
        self.queue = deque()
        self.states = set()
    
    def add(self, node):
        self.queue.append(node)
        self.states.add(node.state)
    
    def remove(self):
        node = self.queue.popleft()
        self.states.remove(node.state)
        return node
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def contains_state(self, state):
        return state in self.states


class StackFrontier(Frontier):
    """Pila LIFO para Búsqueda en Profundidad"""
    
    def __init__(self):
        self.stack = []
        self.states = set()
    
    def add(self, node):
        self.stack.append(node)
        self.states.add(node.state)
    
    def remove(self):
        node = self.stack.pop()
        self.states.remove(node.state)
        return node
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def contains_state(self, state):
        return state in self.states


class PriorityQueueFrontier(Frontier):
    """Priority Queue para A* y otras búsquedas informadas"""
    
    def __init__(self):
        self.heap = []
        self.state_to_node = {}  # Mapear estado al mejor nodo
        self.counter = 0  # Para desempate
    
    def add(self, node):
        # Usar contador para desempate y asegurar comportamiento FIFO para prioridades iguales
        heapq.heappush(self.heap, (node.f_cost, self.counter, node))
        self.counter += 1
        self.state_to_node[node.state] = node
    
    def remove(self):
        # Seguir sacando hasta encontrar un nodo válido (no reemplazado)
        while self.heap:
            _, _, node = heapq.heappop(self.heap)
            # Verificar si este nodo es aún válido (no reemplazado)
            if node.state in self.state_to_node and self.state_to_node[node.state] == node:
                del self.state_to_node[node.state]
                return node
            # De lo contrario, es un nodo obsoleto que fue reemplazado, saltarlo
        raise Exception("Frontera vacía")
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def contains_state(self, state):
        return state in self.state_to_node
    
    def can_replace(self, node):
        """Verificar si el nuevo nodo tiene mejor f-cost que el existente"""
        if node.state in self.state_to_node:
            existing = self.state_to_node[node.state]
            return node.f_cost < existing.f_cost
        return False
    
    def replace(self, node):
        """Reemplazar nodo con mejor f-cost"""
        # Remover entrada antigua (marcar como inválida eliminando del mapa)
        if node.state in self.state_to_node:
            del self.state_to_node[node.state]
        # Agregar nuevo nodo
        self.add(node)


# Funciones auxiliares para diferentes estrategias de búsqueda

def breadth_first_search(problem):
    """
    Búsqueda en Amplitud
    Encuentra camino con mínimo número de pasos
    
    Args:
        problem: Instancia de Problem
        
    Returns:
        Nodo solución o None
    """
    from search.graph_search import graph_search
    print("Ejecutando BFS (Búsqueda en Amplitud)...")
    frontier = QueueFrontier()
    return graph_search(problem, frontier)


def depth_first_search(problem):
    """
    Búsqueda en Profundidad
    Explora profundamente antes de retroceder
    
    Args:
        problem: Instancia de Problem
        
    Returns:
        Nodo solución o None
    """
    from search.graph_search import graph_search
    print("Ejecutando DFS (Búsqueda en Profundidad)...")
    frontier = StackFrontier()
    return graph_search(problem, frontier)


def a_star_search(problem):
    """
    Búsqueda A*
    Usa f(n) = g(n) + h(n) para encontrar camino óptimo
    
    Args:
        problem: Instancia de Problem
        
    Returns:
        Nodo solución o None
    """
    from search.graph_search import graph_search
    print("Ejecutando Búsqueda A*...")
    frontier = PriorityQueueFrontier()
    return graph_search(problem, frontier)
