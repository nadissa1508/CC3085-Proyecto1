"""
Representación de nodo de búsqueda para algoritmos de búsqueda en grafo
"""


class Node:
    """Representa un nodo en el árbol de búsqueda"""
    
    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic=0):
        """
        Inicializar un nodo de búsqueda
        
        Args:
            state: El estado representado por este nodo (ej. posición (fila, col))
            parent: Nodo padre en el árbol de búsqueda
            action: Acción tomada para alcanzar este nodo desde el padre
            path_cost: Costo desde el inicio hasta este nodo (g(n))
            heuristic: Valor heurístico (h(n))
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost  # g(n)
        self.heuristic = heuristic  # h(n)
        self.f_cost = path_cost + heuristic  # f(n) = g(n) + h(n)
        
        # Profundidad en el árbol de búsqueda
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
    
    def get_path(self):
        """
        Reconstruir camino desde el inicio hasta este nodo
        
        Returns:
            Lista de nodos desde el inicio hasta este nodo
        """
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        path.reverse()
        return path
    
    def get_state_path(self):
        """
        Obtener lista de estados desde el inicio hasta este nodo
        
        Returns:
            Lista de estados
        """
        return [node.state for node in self.get_path()]
    
    def __lt__(self, other):
        """Comparación para priority queue (usado en A*)"""
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        """Verificar si dos nodos representan el mismo estado"""
        if not isinstance(other, Node):
            return False
        return self.state == other.state
    
    def __hash__(self):
        """Hash basado en estado para uso en sets/dicts"""
        return hash(self.state)
    
    def __repr__(self):
        return f"Node(state={self.state}, g={self.path_cost}, h={self.heuristic}, f={self.f_cost})"
