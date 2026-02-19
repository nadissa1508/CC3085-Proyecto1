# CC3085-Proyecto1: Robot Navigation System

## Descripción del Proyecto

Este proyecto implementa el sistema de navegación inteligente para un robot de entrega autónomo. El robot debe encontrar la ruta más eficiente desde un punto de inicio hasta una meta dentro de un mapa representado como imagen.

### Task 1: Search Engine 

Implementa un motor de búsqueda que:
1. **Percibe**: Discretiza una imagen en una matriz de nodos (tiles)
2. **Decide**: Calcula rutas usando algoritmos de búsqueda (BFS, DFS, A*)
3. **Visualiza**: Muestra la solución encontrada sobre la imagen original

## Estructura del Proyecto

```
/project
│
├── main.py                      # Programa principal
├── create_test_maze.py          # Script para crear laberintos de prueba
├── requirements.txt             # Dependencias del proyecto
│
├── img/                         # Carpeta con imágenes de prueba
│   ├── Prueba Lab1.bmp
│   ├── Test.bmp
│   ├── Test2.bmp
│   └── turing.bmp
│
├── enviroment/                  # Módulo de procesamiento de imágenes
│   ├── __init__.py
│   ├── image_loader.py         # Carga de imágenes PNG/BMP
│   ├── discretizer.py          # Discretización de imagen a grid
│   └── tile.py                 # Representación de tiles/celdas
│
├── search/                      # Módulo de búsqueda
│   ├── __init__.py
│   ├── problem.py              # Clase abstracta Problem
│   ├── maze_problem.py         # Implementación concreta para laberintos
│   ├── node.py                 # Nodo de búsqueda
│   ├── graph_search.py         # Algoritmo genérico de graph search
│   └── strategies.py           # BFS, DFS, A* y fronteras
│
├── neural_network/              # Módulo de redes neuronales (Task 2)
│   ├── mlp.py
│   ├── train.py
│   └── utils.py
│
└── utils/                       # Utilidades
    ├── __init__.py
    └── visualizer.py           # Visualización de resultados
```

## Instalación

### 1. Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `numpy`: Procesamiento de arrays y matrices
- `Pillow`: Manipulación de imágenes
- `matplotlib`: Visualización de resultados

## Uso del Programa

### Imágenes de Prueba Disponibles

El proyecto incluye imágenes de prueba en la carpeta `img/`:
- `img/turing.bmp`: Laberinto pequeño (~64x64 tiles)
- `img/Test.bmp`: Laberinto mediano con obstáculos
- `img/Test2.bmp`: Laberinto mediano alternativo
- `img/Prueba Lab1.bmp`: Laberinto complejo y grande

### Crear Tus Propios Laberintos (Opcional)

Puedes generar laberintos adicionales con:

```bash
python create_test_maze.py
```

Esto creará laberintos de prueba personalizados en el directorio actual.

### Ejecutar el Programa Principal

```bash
python main.py <ruta_imagen> [tamaño_tile] [algoritmo]
```

**Parámetros:**
- `ruta_imagen`: Ruta al archivo PNG o BMP del laberinto (requerido)
- `tamaño_tile`: Tamaño de los tiles en píxeles (opcional, default: 10)
- `algoritmo`: Algoritmo a usar (opcional, default: astar)
  - `bfs`: Breadth-First Search
  - `dfs`: Depth-First Search
  - `astar`: A* Search
  - `all`: Ejecutar todos y comparar

**Ejemplos:**

```bash
# Usar A* con tiles de 10x10 en laberinto pequeño
python main.py img\turing.bmp

# Usar BFS en laberinto mediano
python main.py img\Test.bmp 10 bfs

# Comparar todos los algoritmos en laberinto complejo
python main.py "img\Prueba Lab1.bmp" 10 all

# Usar DFS en otro laberinto
python main.py img\Test2.bmp 10 dfs
```

### Formato de la Imagen de Entrada

Las imágenes deben seguir esta convención de colores:

- Blanco, (255, 255, 255), Camino libre 
- Negro, (0, 0, 0), Pared/obstáculo 
- Rojo, (255, 0, 0), Punto de inicio 
- Verde, (0, 255, 0), Punto meta 

**Notas importantes:**
- Puede haber múltiples puntos meta (verde)
- Solo puede haber un punto de inicio (rojo)
- Las paredes deben ser negro absoluto [0, 0, 0]
- Se aceptan archivos PNG y BMP
- Si el nombre tiene espacios, usa comillas: `"img\archivo con espacios.bmp"`

## Implementación Técnica

### Task 1.1: Discretización del Mundo

**Archivo**: `enviroment/discretizer.py`

La clase `Discretizer` convierte una imagen continua en una representación discreta:

```python
discretizer = Discretizer(tile_size=10)  # Tiles de 10x10 píxeles
grid = discretizer.discretize(img_array)
```

**Proceso:**
1. Divide la imagen en tiles de NxN píxeles
2. Calcula el color RGB promedio de cada tile
3. Clasifica cada tile como: FREE, WALL, START, o GOAL
4. Identifica posiciones de inicio y meta

### Task 1.2: Framework de Búsqueda

**Archivos**: `search/problem.py`, `search/maze_problem.py`

Implementación del framework formal de problemas usando POO:

```python
class Problem(ABC):
    @abstractmethod
    def actions(self, state): pass
    
    @abstractmethod
    def result(self, state, action): pass
    
    @abstractmethod
    def step_cost(self, state, action, next_state): pass
    
    @abstractmethod
    def heuristic(self, state): pass
```

**Algoritmo Genérico**: `search/graph_search.py`

```python
def graph_search(problem, frontier):
    """
    Algoritmo genérico de búsqueda en grafos
    - Funciona con cualquier frontera (Queue, Stack, PriorityQueue)
    - Evita ciclos usando conjunto de explorados
    - Retorna nodo solución con el camino completo
    """
```

**Algoritmos Implementados:**

1. **BFS (Breadth-First Search)**
   - Frontera: FIFO Queue
   - Garantiza camino con menor número de pasos
   - Completo y óptimo para costo uniforme

2. **DFS (Depth-First Search)**
   - Frontera: LIFO Stack
   - Explora profundamente antes de retroceder
   - No garantiza solución óptima

3. **A\* Search**
   - Frontera: Priority Queue con f(n) = g(n) + h(n)
   - g(n): costo del camino desde inicio
   - h(n): heurística (distancia Euclidiana a la meta)
   - Óptimo con heurística admisible

### Task 1.3: A* con Heurística

**Heurística utilizada**: Distancia Euclidiana

```python
def heuristic(self, state):
    row, col = state
    min_distance = float('inf')
    for goal_row, goal_col in self.goal_states:
        distance = ((row - goal_row)**2 + (col - goal_col)**2)**0.5
        min_distance = min(min_distance, distance)
    return min_distance
```

**Costos de movimiento:**
- Movimiento recto (↑ ↓ ← →): costo 1.0
- Movimiento diagonal (↖ ↗ ↙ ↘): costo 1.414 (√2)

### Visualización

**Archivo**: `utils/visualizer.py`

Dos tipos de visualización:

1. **Solución sobre imagen original**: Dibuja el camino como línea amarilla
2. **Representación del grid**: Muestra la matriz discreta con el camino

## Salida del Programa

El programa genera:

1. **Consola**: Estadísticas de búsqueda
   ```
   Running A* Search...
   Solution found! Nodes expanded: 234
   Path length: 45
   Path cost: 52.3
   ```

2. **Archivos de salida** (carpeta `output/`):
   - `solution_<algoritmo>.png`: Camino dibujado sobre imagen original
   - `grid_<algoritmo>.png`: Representación del grid discreto

3. **Visualización interactiva**: Gráficas con matplotlib

## Características Técnicas

### Paradigma de Programación Orientada a Objetos

- **Abstracción**: Clase abstracta `Problem` define interfaz común

- **Herencia**: `MazeProblem` hereda de `Problem`

- **Encapsulación**: Componentes modulares e independientes

- **Polimorfismo**: `graph_search` funciona con cualquier subclase de `Problem`

### Sin Dependencias de Librerías de IA

- Solo usa: `numpy`, `Pillow`, `matplotlib`

- No usa: `sklearn`, `tensorflow`, `pytorch`, etc.

-  Todo implementado desde cero usando estructuras de datos básicas

## Algoritmos y Complejidad

| Algoritmo | Complejidad Temporal | Complejidad Espacial | Optimidad |
|-----------|---------------------|---------------------|-----------|
| BFS | O(b^d) | O(b^d) | Óptimo (costo uniforme) |
| DFS | O(b^m) | O(bm) | No óptimo |
| A* | O(b^d) | O(b^d) | Óptimo (h admisible) |

Donde:
- b = factor de ramificación (máx 8 direcciones)
- d = profundidad de la solución
- m = profundidad máxima del árbol

## Próximos Pasos (Task 2)

- Implementar MLP desde cero con numpy
- Entrenar clasificador de colores RGB
- Integrar costos variables según tipo de terreno
- Modificar A* para usar predicciones de la red neuronal

## Autores

- Angie Vela
- Cristian Tunchez



