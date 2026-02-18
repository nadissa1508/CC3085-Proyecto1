# CC3085-Proyecto1
Este proyecto implementa el sistema de navegación inteligente para un robot de entrega autónomo. El robot debe encontrar la ruta más eficiente desde un punto de inicio hasta una meta dentro de un mapa representado como imagen.

/project
│
├── main.py
│
├── environment/
│   ├── image_loader.py
│   ├── discretizer.py
│   ├── color_classifier.py
│
├── search/
│   ├── problem.py
│   ├── maze_problem.py
│   ├── node.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── astar.py
│
├── neural_network/
│   ├── mlp.py
│   ├── train.py
│
└── utils/
    ├── visualization.py

