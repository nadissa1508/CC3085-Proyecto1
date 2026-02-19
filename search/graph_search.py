"""
Implementación del algoritmo genérico de búsqueda en grafo
"""
from search.node import Node


def graph_search(problem, frontier):
    """
    Algoritmo genérico de búsqueda en grafo
    
    Args:
        problem: Una instancia de Problem (o subclase)
        frontier: Una estructura de datos frontier (cola, pila, o priority queue)
        
    Returns:
        Nodo solución si se encuentra, None en caso contrario
    """
    # Inicializar frontier con el estado inicial
    initial_node = Node(
        state=problem.initial_state,
        parent=None,
        action=None,
        path_cost=0,
        heuristic=problem.heuristic(problem.initial_state)
    )
    frontier.add(initial_node)
    
    # Mantener registro de estados explorados
    explored = set()
    
    # Estadísticas
    nodes_expanded = 0
    
    while not frontier.is_empty():
        # Elegir un nodo de la frontier
        node = frontier.remove()
        
        # Prueba de meta
        if problem.goal_test(node.state):
            print(f"¡Solución encontrada! Nodos expandidos: {nodes_expanded}")
            print(f"Longitud del camino: {len(node.get_path())}")
            print(f"Costo del camino: {node.path_cost}")
            return node
        
        # Agregar a explorados
        explored.add(node.state)
        nodes_expanded += 1
        
        # Expandir nodo
        for action in problem.actions(node.state):
            # Obtener estado resultante
            next_state = problem.result(node.state, action)
            
            # Saltar si ya fue explorado
            if next_state in explored:
                continue
            
            # Calcular costo del camino
            step_cost = problem.step_cost(node.state, action, next_state)
            path_cost = node.path_cost + step_cost
            
            # Calcular heurística
            heuristic = problem.heuristic(next_state)
            
            # Crear nodo hijo
            child = Node(
                state=next_state,
                parent=node,
                action=action,
                path_cost=path_cost,
                heuristic=heuristic
            )
            
            # Agregar a frontier si no está allí o si encontramos un mejor camino
            if not frontier.contains_state(child.state):
                frontier.add(child)
            elif frontier.can_replace(child):
                frontier.replace(child)
    
    print(f"No se encontró solución. Nodos expandidos: {nodes_expanded}")
    return None
