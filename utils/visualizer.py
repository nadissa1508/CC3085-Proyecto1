"""
Utilidades de visualización para mostrar soluciones del laberinto
"""
import numpy as np
from PIL import Image, ImageDraw

# Hacer matplotlib opcional
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Advertencia: matplotlib no disponible. Algunas características de visualización estarán deshabilitadas.")


class Visualizer:
    """Maneja la visualización del laberinto y caminos de solución"""
    
    @staticmethod
    def draw_solution_on_image(img_array, solution_path, tile_size, output_path=None):
        """
        Dibujar camino de solución en la imagen original
        
        Args:
            img_array: Imagen original como array numpy
            solution_path: Lista de estados (fila, col) representando el camino
            tile_size: Tamaño de tiles usado en la discretización
            output_path: Ruta opcional para guardar el resultado
            
        Returns:
            Array de imagen modificado con la solución dibujada
        """
        # Crear una copia para evitar modificar el original
        result_img = img_array.copy()
        
        # Convertir a PIL Image para dibujar
        pil_img = Image.fromarray(result_img.astype('uint8'))
        draw = ImageDraw.Draw(pil_img)
        
        # Dibujar camino
        if len(solution_path) > 1:
            # Convertir coordenadas de matriz a coordenadas de píxeles (centro de tiles)
            pixel_path = []
            for row, col in solution_path:
                pixel_x = col * tile_size + tile_size // 2
                pixel_y = row * tile_size + tile_size // 2
                pixel_path.append((pixel_x, pixel_y))
            
            # Dibujar líneas conectando puntos del camino
            for i in range(len(pixel_path) - 1):
                draw.line([pixel_path[i], pixel_path[i + 1]], 
                         fill=(255, 255, 0), width=3)  # Línea amarilla
            
            # Dibujar círculos en puntos del camino
            for point in pixel_path:
                x, y = point
                r = 2  # radio
                draw.ellipse([x-r, y-r, x+r, y+r], fill=(255, 0, 255))  # Puntos magenta
        
        # Convertir de vuelta a array numpy
        result_array = np.array(pil_img)
        
        # Guardar si se proporciona ruta de salida
        if output_path:
            pil_img.save(output_path)
            print(f"Imagen de solución guardada en: {output_path}")
        
        return result_array
    
    @staticmethod
    def draw_grid_solution(grid, solution_path, output_path=None):
        """
        Dibujar solución en la representación de matriz discretizada
        
        Args:
            grid: Lista 2D de objetos Tile
            solution_path: Lista de estados (fila, col)
            output_path: Ruta opcional para guardar el resultado
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Advertencia: matplotlib no disponible. Omitiendo visualización de matriz.")
            return
        
        rows = len(grid)
        cols = len(grid[0]) if grid else 0
        
        # Crear array de imagen para visualización de matriz
        # Cada tile será representado como un solo píxel por simplicidad
        grid_img = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        # Colorear cada tile
        for i in range(rows):
            for j in range(cols):
                tile = grid[i][j]
                if tile.tile_type == 0:  # FREE
                    grid_img[i, j] = [255, 255, 255]  # White
                elif tile.tile_type == 1:  # WALL
                    grid_img[i, j] = [0, 0, 0]  # Black
                elif tile.tile_type == 2:  # START
                    grid_img[i, j] = [255, 0, 0]  # Red
                elif tile.tile_type == 3:  # GOAL
                    grid_img[i, j] = [0, 255, 0]  # Green
        
        # Dibujar camino de solución (excluyendo inicio y meta)
        for row, col in solution_path[1:-1]:
            grid_img[row, col] = [255, 255, 0]  # Yellow
        
        # Mostrar usando matplotlib
        plt.figure(figsize=(10, 10))
        plt.imshow(grid_img)
        plt.title(f"Solución en Matriz (Longitud del camino: {len(solution_path)})")
        plt.axis('off')
        
        if output_path:
            plt.savefig(output_path, bbox_inches='tight', dpi=150)
            print(f"Solución de matriz guardada en: {output_path}")
        
        plt.show()
    
    @staticmethod
    def display_image(img_array, title="Imagen"):
        """
        Mostrar una imagen usando matplotlib
        
        Args:
            img_array: Imagen como array numpy
            title: Título para el gráfico
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Advertencia: matplotlib no disponible. Omitiendo visualización de imagen.")
            return
        
        plt.figure(figsize=(10, 10))
        plt.imshow(img_array)
        plt.title(title)
        plt.axis('off')
        plt.show()
    
    @staticmethod
    def compare_solutions(img_array, solutions_dict, tile_size):
        """
        Comparar múltiples soluciones de algoritmos de búsqueda lado a lado
        
        Args:
            img_array: Imagen original
            solutions_dict: Diccionario mapeando nombres de algoritmos a caminos de solución
            tile_size: Tamaño de tile usado en la discretización
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Advertencia: matplotlib no disponible. Omitiendo visualización de comparación.")
            return
        
        num_solutions = len(solutions_dict)
        fig, axes = plt.subplots(1, num_solutions, figsize=(6*num_solutions, 6))
        
        if num_solutions == 1:
            axes = [axes]
        
        for idx, (name, path) in enumerate(solutions_dict.items()):
            # Dibujar solución en la imagen
            result_img = Visualizer.draw_solution_on_image(
                img_array.copy(), path, tile_size
            )
            
            axes[idx].imshow(result_img)
            axes[idx].set_title(f"{name}\nLongitud del camino: {len(path)}")
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.show()
