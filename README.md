# CC3085-Proyecto1: Robot de Navegación con Algoritmos de Búsqueda

## Universidad del Valle de Guatemala
### Facultad de Ingeniería
### CC3045 – Inteligencia Artificial

**Autores:**
- Cristian Tunchez
- Angie Vela

---

## Descripción del Proyecto

Este proyecto implementa el sistema de navegación inteligente para un robot de entrega autónomo. El robot recibe imágenes satelitales (mapas) donde debe encontrar la ruta más eficiente desde un punto de inicio (rojo) hasta una meta (verde).

### Task 1: Search Engine

Implementa un motor de búsqueda completo que:
1. **Percibe**: Discretiza una imagen en una matriz de tiles (nodos)
2. **Decide**: Calcula rutas usando algoritmos de búsqueda informada y no informada
3. **Visualiza**: Muestra la solución encontrada sobre representaciones discretas

## Estructura del Proyecto

```
CC3085-Proyecto1/
│
├── Proyecto1.ipynb              # Notebook principal con toda la implementación
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
│
├── img/                            # Imágenes de prueba
│   ├── Prueba Lab1.bmp            # 582x582 píxeles
│   ├── Test.bmp                   # 582x582 píxeles  
│   ├── Test2.bmp                  # 582x582 píxeles
│   └── turing.bmp                 # 640x640 píxeles (patrones orgánicos)
│
└── myenv/                          # Entorno virtual de Python
```

## Instalación

### 1. Requisitos Previos
- Python 3.8 o superior
- Jupyter Notebook o VS Code con extensión de Python
- pip (gestor de paquetes de Python)

### 2. Crear Entorno Virtual (Recomendado)

```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `numpy`: Procesamiento de arrays y matrices
- `Pillow (PIL)`: Manipulación y carga de imágenes
- `matplotlib`: Visualización de resultados y gráficas
- `ipykernel`: Kernel de Jupyter para notebooks

## Uso del Programa

### Ejecutar el Notebook

1. **Con Jupyter Notebook:**
   ```bash
   jupyter notebook Proyecto1.ipynb
   ```

2. **Con VS Code:**
   - Abrir el archivo `Proyecto1.ipynb`
   - Seleccionar el kernel del entorno virtual `myenv`
   - Ejecutar las celdas secuencialmente

### Estructura del Notebook

El notebook está organizado en las siguientes secciones:

1. **Importación de Librerías**: NumPy, PIL, matplotlib
2. **Task 1.1 - Discretización**: Clase `WorldDiscretizer`
3. **Task 1.2 - Búsqueda**: BFS y DFS con `GraphSearch`
4. **Task 1.3 - A* Search**: Implementación con heurística Manhattan
5. **Pruebas Automáticas**: Función `test_all_images()` para todas las imágenes
6. **Visualización y Resultados**: Comparaciones y conclusiones

### Imágenes de Prueba Disponibles

El proyecto incluye imágenes de prueba en la carpeta `img/`:
- `Prueba Lab1.bmp`: Laberinto complejo (582x582 píxeles)
- `Test.bmp`: Laberinto mediano con obstáculos (582x582 píxeles)
- `Test2.bmp`: Laberinto mediano alternativo (582x582 píxeles)
- `turing.bmp`: Patrones orgánicos (640x640 píxeles) - **Requiere tile_size=5**

### Formato de la Imagen de Entrada

Las imágenes deben seguir esta convención de colores:

| Color | RGB | Significado |
|-------|-----|-------------|
| Blanco | (255, 255, 255) | Camino libre |
| Negro | (0, 0, 0) | Pared/Obstáculo |
| Rojo | (255, 0, 0) | Punto de inicio |
| Verde | (0, 255, 0) | Punto meta |

**Notas importantes:**
- Puede haber múltiples puntos meta (verde)
- Solo un punto de inicio (rojo)
- Las paredes deben ser negro puro [0, 0, 0]
- Se aceptan archivos PNG y BMP
- Considerar el tamaño del tile según la complejidad de la imagen

## Implementación Técnica

### Task 1.1: Discretización del Mundo

**Clase**: `WorldDiscretizer`

Convierte una imagen continua en una representación discreta mediante tiles:

```python
discretizer = WorldDiscretizer(tile_size=10)  # Tiles de 10x10 píxeles
grid = discretizer.discretize(img_array)
```

**Proceso de discretización:**
1. Divide la imagen en tiles de NxN píxeles
2. Calcula el color RGB promedio de cada tile
3. Clasifica cada tile como: `OBSTACLE`, `PATH`, `START`, o `GOAL`
4. Identifica posiciones de inicio y metas

**Estrategia de clasificación:**
- Si hay píxeles rojos → tile de START
- Si hay píxeles verdes → tile de GOAL
- Si >50% son negros → tile de OBSTACLE
- De lo contrario → tile de PATH

**Consideraciones especiales:**
- `turing.bmp` requiere `tile_size=5` debido a sus patrones orgánicos
- Imágenes más pequeñas benefician de tiles más pequeños
- Tiles más grandes aceleran la búsqueda pero reducen precisión

### Task 1.2: Framework de Búsqueda

**Clases principales:**

1. **`SearchProblem` (Clase abstracta)**
   ```python
   class SearchProblem(ABC):
       @abstractmethod
       def actions(self, state): pass
       
       @abstractmethod
       def result(self, state, action): pass
       
       @abstractmethod
       def is_goal(self, state): pass
       
       @abstractmethod
       def step_cost(self, state, action, next_state): pass
       
       @abstractmethod
       def heuristic(self, state): pass
   ```

2. **`MazeProblem` (Implementación concreta)**
   - Hereda de `SearchProblem`
   - Define estado inicial y estados meta
   - Implementa acciones: 4 direcciones (↑ ↓ ← →)
   - Costo uniforme: 1.0 por movimiento
   - Evita movimientos fuera de límites y a obstáculos

3. **`Node` (Nodo de búsqueda)**
   - Encapsula estado, padre, acción, costo g(n)
   - Permite reconstruir path desde inicio hasta meta

4. **`GraphSearch` (Algoritmo genérico)**
   ```python
   def search(self, problem, frontier_type='queue'):
       """
       - Recibe cualquier tipo de frontera (Queue/Stack)
       - Mantiene conjunto 'reached' para evitar ciclos
       - Retorna nodo solución con path completo
       """
   ```

**Algoritmos implementados con `GraphSearch`:**

1. **BFS (Breadth-First Search)**
   - Frontera: FIFO Queue (`deque`)
   - Explora por niveles
   - **Completo**: Siempre encuentra solución si existe
   - **Óptimo**: Para costo uniforme
   - **Uso**: Cuando se necesita camino con menor número de pasos

2. **DFS (Depth-First Search)**
   - Frontera: LIFO Stack (lista con `pop()`)
   - Explora profundamente antes de retroceder
   - **Completo**: En espacios finitos con detección de ciclos
   - **No óptimo**: No garantiza mejor solución
   - **Uso**: Cuando memoria es limitada o se busca cualquier solución rápido

### Task 1.3: A* Search

**Clase**: `AStarSearch`

Implementación de búsqueda heurística óptima:

```python
class AStarSearch:
    def search(self, problem):
        # f(n) = g(n) + h(n)
        # g(n) = costo del camino desde inicio
        # h(n) = heurística (Manhattan)
```

**Heurística utilizada: Distancia Manhattan**

```python
def heuristic(self, state):
    """
    Calcula distancia Manhattan al goal más cercano.
    h(n) = |x1 - x2| + |y1 - y2|
    """
    row, col = state
    min_distance = float('inf')
    for goal_row, goal_col in self.goal_states:
        manhattan = abs(row - goal_row) + abs(col - goal_col)
        min_distance = min(min_distance, manhattan)
    return min_distance
```

**Propiedades de la heurística:**
- **Admisible**: Nunca sobreestima el costo real
- **Consistente**: h(n) ≤ costo(n,a,n') + h(n')
- **Apropiada**: Para movimiento en 4 direcciones sin diagonales

**Frontera:**
- Priority Queue (heap) ordenada por f(n) = g(n) + h(n)
- Elemento con menor f(n) se expande primero

**Ventajas de A*:**
- **Óptimo**: Con heurística admisible, garantiza mejor solución
- **Eficiente**: Expande menos nodos que BFS/DFS
- **Informado**: Usa conocimiento del problema (distancia a meta)

### Visualización

**Funciones implementadas:**

1. **`visualize_path_discrete(grid, path)`**
   - Muestra representación del grid discretizado
   - Camino marcado con cuadrados rojos (inicio) y verdes (meta)
   - Usa colormap personalizado:
     - Negro: Obstáculos
     - Blanco: Caminos
     - Amarillo: Path de la solución

2. **`compare_all_algorithms(problem, search_results)`**
   - Compara BFS, DFS y A* lado a lado
   - Muestra nodos expandidos, longitud y costo del path
   - Visualización gráfica de las tres soluciones

### Pruebas Automáticas

**Función**: `test_all_images(img_folder="img")`

Ejecuta automáticamente los tres algoritmos en todas las imágenes de la carpeta:

```python
for img_name in ['Prueba Lab1.bmp', 'Test.bmp', 'Test2.bmp', 'turing.bmp']:
    # Ajusta tile_size según imagen
    if 'turing' in img_name:
        tile_size = 5  # Patrones orgánicos
    else:
        tile_size = 10  # Laberintos estándar
    
    # Ejecuta BFS, DFS, A*
    # Recopila métricas
    # Visualiza resultados
```

**Métricas recopiladas:**
- Nodos expandidos
- Longitud del path (número de pasos)
- Costo total del path
- Tiempo de ejecución (implícito en nodos expandidos)

## Resultados y Análisis

### Comparación de Algoritmos

Los tres algoritmos fueron probados en 4 imágenes diferentes:

**Características observadas:**

| Algoritmo | Optimalidad | Nodos Expandidos | Velocidad |
|-----------|-------------|------------------|-----------|
| **BFS** | ✓ Óptimo | Alto (exhaustivo) | Moderada |
| **DFS** | ✗ No óptimo | Variable | Rápida |
| **A*** | ✓ Óptimo | Bajo (heurística) | Más eficiente |

**Conclusiones:**

1. **BFS**: Garantiza encontrar el camino más corto, pero explora muchos nodos innecesarios. Ideal cuando se necesita certeza de optimalidad y el espacio de búsqueda es pequeño.

2. **DFS**: Encuentra soluciones rápidamente pero no garantiza el mejor camino. Útil para espacios grandes donde cualquier solución es aceptable.

3. **A***: Combina optimalidad con eficiencia. Gracias a la heurística Manhattan, expande significativamente menos nodos que BFS mientras mantiene garantía de optimalidad. **Recomendado para navegación de robots**.

4. **Heurística Manhattan**: Es admisible y consistente para movimiento en 4 direcciones. Proporciona una guía efectiva hacia la meta sin sobreestimar costos.

5. **Discretización**: El tamaño del tile es crítico. Tiles muy grandes pierden detalles importantes (turing.bmp necesita tile_size=5). Tiles muy pequeños aumentan el espacio de búsqueda.

### Manejo de Casos Especiales

- **turing.bmp**: Patrones orgánicos y formas curvas requieren discretización más fina (5x5 píxeles)
- **Múltiples metas**: El sistema soporta múltiples puntos verdes, encontrando el camino al más cercano
- **Laberintos complejos**: A* demuestra su superioridad en laberintos grandes donde BFS se vuelve ineficiente

## Características Técnicas

### Paradigma de Programación Orientada a Objetos

El proyecto utiliza POO de forma extensiva:

- **Abstracción**: Clase abstracta `SearchProblem` define interfaz común
- **Herencia**: `MazeProblem` hereda de `SearchProblem`
- **Encapsulación**: Componentes modulares con responsabilidades claras
  - `WorldDiscretizer`: Maneja discretización de imágenes
  - `MazeProblem`: Define lógica del problema de búsqueda
  - `GraphSearch` / `AStarSearch`: Algoritmos de búsqueda
- **Polimorfismo**: Los algoritmos trabajan con cualquier `SearchProblem`

### Implementación Desde Cero

- **Solo usa**: `numpy`, `Pillow`, `matplotlib`
- **No usa**: `sklearn`, `tensorflow`, `pytorch`, o librerías de IA
- **Todo implementado manualmente**:
  - Estructuras de datos (Queue, Stack, PriorityQueue con heapq)
  - Algoritmos de búsqueda completos
  - Heurísticas y funciones de evaluación
  - Sistema de discretización de imágenes

### Estructuras de Datos Utilizadas

| Estructura | Uso | Implementación |
|------------|-----|----------------|
| `deque` | Frontera BFS | `collections.deque` |
| `list` | Frontera DFS | Lista de Python con `pop()` |
| `heapq` | Frontera A* | `heapq` para priority queue |
| `set` | Conjunto 'reached' | Set de Python para O(1) lookup |
| `numpy.ndarray` | Grid discretizado | NumPy array 2D |

## Complejidad de Algoritmos

| Algoritmo | Tiempo | Espacio | Optimalidad | Completitud |
|-----------|--------|---------|-------------|-------------|
| **BFS** | O(b^d) | O(b^d) | Óptimo* | Completo |
| **DFS** | O(b^m) | O(bm) | No óptimo | Completo** |
| **A*** | O(b^d) | O(b^d) | Óptimo*** | Completo |

**Donde:**
- **b** = factor de ramificación (4 direcciones)
- **d** = profundidad de la solución
- **m** = profundidad máxima del árbol de búsqueda

**Notas:**
- \* BFS es óptimo para costo uniforme (todos los pasos cuestan 1)
- \*\* DFS es completo con detección de ciclos (conjunto 'reached')
- \*\*\* A* es óptimo con heurística admisible y consistente (Manhattan)

### Optimalidad de la Heurística Manhattan

La heurística h(n) = |x₁ - x₂| + |y₁ - y₂| es:

1. **Admisible**: Nunca sobreestima el costo real
   - En el mejor caso, el camino real es una línea recta
   - Distancia Manhattan ≤ Distancia real del camino

2. **Consistente (Monotónica)**: h(n) ≤ cost(n, a, n') + h(n')
   - Moverse un paso reduce la heurística en exactamente 1 o aumenta en 1
   - Cumple desigualdad triangular

3. **Apropiada**: Para movimiento en 4 direcciones (sin diagonales)
   - Refleja exactamente los movimientos permitidos
   - Si se permitieran diagonales, sería mejor usar distancia Euclidiana

## Ejecución y Resultados

### Salidas Generadas por el Notebook

Al ejecutar el notebook completo, se genera:

1. **Visualizaciones de discretización**
   - Grid coloreado mostrando obstáculos, caminos, inicio y meta
   - Información de dimensiones y estadísticas del grid

2. **Resultados de búsqueda por imagen**
   - Estadísticas: nodos expandidos, longitud del path, costo
   - Visualización del path encontrado sobre el grid
   - Marcadores: cuadrado rojo (inicio), cuadrado verde (meta)

3. **Comparación de algoritmos**
   - Gráficas comparativas de BFS vs DFS vs A*
   - Tres subplots mostrando el path de cada algoritmo
   - Tabla resumen con métricas de rendimiento

4. **Tabla resumen final**
   - Resultados consolidados de todas las imágenes
   - Comparación de eficiencia entre algoritmos
   - Conclusiones basadas en datos

### Ejemplo de Salida (Consola)

```
[OK] Imagen cargada: img/Test.bmp
Dimensiones: 582x582 píxeles
Discretización con tile_size=10
Grid resultante: 58x58 tiles

=== BFS ===
[OK] Solución encontrada!
Nodos expandidos: 1523
Longitud del path: 87
Costo del path: 87.0

=== DFS ===
[OK] Solución encontrada!
Nodos expandidos: 245
Longitud del path: 156
Costo del path: 156.0

=== A* ===
[OK] Solución encontrada!
Nodos expandidos: 432
Longitud del path: 87
Costo del path: 87.0
```

## Modificar el Código

### Cambiar Imagen de Prueba

Modificar la celda con `IMAGE_FILE`:
```python
IMAGE_FILE = "img/turing.bmp"  # Cambiar según imagen deseada
```

### Ajustar Tamaño de Tile

Modificar el parámetro en la discretización:
```python
discretizer = WorldDiscretizer(tile_size=5)  # 5, 10, 15, 20...
```

**Recomendaciones:**
- Imágenes pequeñas o patrones complejos: `tile_size=5`
- Laberintos estándar: `tile_size=10`  
- Imágenes muy grandes: `tile_size=15-20`

### Agregar Nuevas Imágenes

1. Colocar imagen `.bmp` o `.png` en carpeta `img/`
2. Asegurar formato de colores correcto (rojo=inicio, verde=meta, negro=obstáculo, blanco=camino)
3. La función `test_all_images()` automáticamente detectará nuevas imágenes

### Extender los Algoritmos

Para agregar un nuevo algoritmo:

1. Si es búsqueda no informada (ej: UCS):
   - Usar `GraphSearch` con frontera `PriorityQueue` ordenada por g(n)

2. Si es búsqueda informada (ej: Greedy):
   - Crear nueva clase similar a `AStarSearch`
   - Modificar función de evaluación (ej: solo h(n) para Greedy)

3. Agregar visualización:
   - Incluir en función `compare_all_algorithms()`

## Limitaciones Conocidas

1. **Solo movimientos ortogonales**: No se permiten movimientos diagonales
   - Simplifica el problema y hace Manhattan más apropiada
   - Extensión futura: agregar 8 direcciones

2. **Discretización con pérdida**: Tiles pueden perder detalles
   - Solución: ajustar `tile_size` según complejidad de imagen
   - Trade-off entre precisión y eficiencia

3. **Un solo punto de inicio**: Solo acepta un área roja
   - Extensión: permitir múltiples inicios y encontrar el mejor

4. **Costo uniforme**: Todos los movimientos cuestan 1.0
   - Task 2 integrará costos variables según terreno

## Trabajo Futuro (Task 2)

- Implementar MLP (Multi-Layer Perceptron) desde cero
- Entrenar clasificador de tipos de terreno (más allá de 4 colores)
- Integrar costos variables según predicciones de la red neuronal
- Modificar A* para considerar diferentes costos de terreno
- Explorar terrenos continuos (arena, pasto, agua, etc)

## Dependencias del Proyecto

**requirements.txt:**
```
numpy>=1.26.0
Pillow>=10.0.0
matplotlib>=3.8.0
ipykernel>=6.25.0
jupyter>=1.0.0
```

## Referencias

- Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.)
- Clase CC3045 - Inteligencia Artificial, Universidad del Valle de Guatemala
- Documentación de NumPy: https://numpy.org/doc/
- Documentación de Pillow: https://pillow.readthedocs.io/


