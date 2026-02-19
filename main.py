"""
CC3085 - Inteligencia Artificial - Proyecto 1

Programa principal para la Tarea 1: Sistema de Navegación de Laberintos
Este programa implementa un sistema de navegación para robots que puede:
1. Cargar y discretizar imágenes de laberintos
2. Encontrar caminos usando los algoritmos de búsqueda BFS, DFS y A*
3. Visualizar las soluciones en la imagen original
"""

import sys
import os
from enviroment.image_loader import ImageLoader
from enviroment.discretizer import Discretizer
from search.maze_problem import MazeProblem
from search.strategies import breadth_first_search, depth_first_search, a_star_search
from utils.visualizer import Visualizer


def main():
    """Función principal para ejecutar el solucionador de laberintos""" 
    print("CC3085 - Proyecto 1: Sistema de Navegación de Robot")
    print("Tarea 1: Implementación del Motor de Búsqueda")
    
    # Configuración
    # Puedes modificar estos parámetros
    IMAGE_PATH = "maze.png"  # Ruta a tu imagen del laberinto
    TILE_SIZE = 10  # Tamaño de tiles (10x10 píxeles por tile)
    ALGORITHM = "astar"  # Opciones: "bfs", "dfs", "astar", "all"
    
    # Verificar si la ruta de imagen se proporciona como argumento de línea de comandos
    if len(sys.argv) > 1:
        IMAGE_PATH = sys.argv[1]
    if len(sys.argv) > 2:
        TILE_SIZE = int(sys.argv[2])
    if len(sys.argv) > 3:
        ALGORITHM = sys.argv[3].lower()
    
    # Verificar si la imagen existe
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: ¡Archivo de imagen '{IMAGE_PATH}' no encontrado!")
        print(f"Por favor proporcione una ruta de imagen válida.")
        print(f"Uso: python main.py <ruta_imagen> [tamaño_tile] [algoritmo]")
        print(f"  opciones de algoritmo: bfs, dfs, astar, all")
        return
    
    print(f"\nConfiguración:")
    print(f"  Imagen: {IMAGE_PATH}")
    print(f"  Tamaño de tile: {TILE_SIZE}x{TILE_SIZE} píxeles")
    print(f"  Algoritmo: {ALGORITHM.upper()}")
    print()
    
    # Paso 1: Cargar imagen
    print("Paso 1: Cargando imagen...")
    try:
        img_array = ImageLoader.load_image(IMAGE_PATH)
        height, width = ImageLoader.get_dimensions(img_array)
        print(f"  Imagen cargada: {width}x{height} píxeles")
    except Exception as e:
        print(f"  Error al cargar imagen: {e}")
        return
    
    # Paso 2: Discretizar imagen en matriz
    print("\nPaso 2: Discretizando imagen en matriz...")
    discretizer = Discretizer(tile_size=TILE_SIZE)
    grid = discretizer.discretize(img_array)
    grid_rows, grid_cols = discretizer.get_grid_dimensions()
    print(f"  Matriz creada: {grid_rows}x{grid_cols} tiles")
    
    # Obtener posiciones de inicio y meta
    start_pos = discretizer.get_start_position()
    goal_positions = discretizer.get_goal_positions()
    
    if start_pos is None:
        print("  Error: ¡No se encontró posición de inicio (rojo) en la imagen!")
        return
    if not goal_positions:
        print("  Error: ¡No se encontró posición de meta (verde) en la imagen!")
        return
    
    print(f"  Posición de inicio: {start_pos}")
    print(f"  Posiciones de meta: {goal_positions}")
    
    # Paso 3: Crear problema del laberinto
    print("\nPaso 3: Creando problema del laberinto...")
    problem = MazeProblem(grid, start_pos, goal_positions)
    print(f"  Problema creado con {len(goal_positions)} meta(s)")
    
    # Paso 4: Resolver usando algoritmo(s) seleccionado(s)
    print("\nPaso 4: Resolviendo laberinto...")
    print("-" * 60)
    
    solutions = {}
    
    if ALGORITHM == "all":
        # Ejecutar todos los algoritmos
        algorithms = {
            "BFS": breadth_first_search,
            "DFS": depth_first_search,
            "A*": a_star_search
        }
        
        for name, algo_func in algorithms.items():
            print(f"\n{name}:")
            solution_node = algo_func(problem)
            if solution_node:
                path = solution_node.get_state_path()
                solutions[name] = path
            else:
                print(f"  No se encontró solución con {name}")
            print()
    else:
        # Ejecutar un solo algoritmo
        if ALGORITHM == "bfs":
            solution_node = breadth_first_search(problem)
        elif ALGORITHM == "dfs":
            solution_node = depth_first_search(problem)
        elif ALGORITHM == "astar":
            solution_node = a_star_search(problem)
        else:
            print(f"Algoritmo desconocido: {ALGORITHM}")
            print("Opciones válidas: bfs, dfs, astar, all")
            return
        
        if solution_node:
            path = solution_node.get_state_path()
            solutions[ALGORITHM.upper()] = path
        else:
            print("¡No se encontró solución!")
            return
    
    print("-" * 60)
    
    # Paso 5: Visualizar resultados
    if solutions:
        print("\nPaso 5: Visualizando resultados...")
        
        # Crear directorio de salida si no existe
        os.makedirs("output", exist_ok=True)
        
        if len(solutions) == 1:
            # Solución única
            name, path = list(solutions.items())[0]
            
            # Dibujar en imagen original
            output_path = f"output/solution_{name.lower()}.png"
            result_img = Visualizer.draw_solution_on_image(
                img_array, path, TILE_SIZE, output_path
            )
            
            # Dibujar representación de matriz
            grid_output = f"output/grid_{name.lower()}.png"
            Visualizer.draw_grid_solution(grid, path, grid_output)
            
            print(f"\n  Longitud del camino de solución: {len(path)} pasos")
            print(f"  Imágenes guardadas en el directorio output/")
        else:
            # Múltiples soluciones - comparar
            Visualizer.compare_solutions(img_array, solutions, TILE_SIZE)
            
            # Guardar soluciones individuales
            for name, path in solutions.items():
                output_path = f"output/solution_{name.lower()}.png"
                Visualizer.draw_solution_on_image(
                    img_array, path, TILE_SIZE, output_path
                )
            
            print(f"\n  Soluciones guardadas en el directorio output/")
            print("\n  Comparación:")
            for name, path in solutions.items():
                print(f"    {name}: {len(path)} pasos")
    


if __name__ == "__main__":
    main()
