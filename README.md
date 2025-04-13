# Proyecto 2 - Algoritmos de Búsqueda en Laberintos

Este proyecto consiste en la generación aleatoria de laberintos y la comparación de distintos algoritmos de búsqueda para encontrar rutas óptimas desde un punto de inicio hasta un punto de salida. Forma parte del curso de **Inteligencia Artificial 2025**.

## 📚 Objetivos

- Implementar algoritmos de generación de laberintos.
- Resolver laberintos con algoritmos de búsqueda.
- Comparar el desempeño de distintos algoritmos de búsqueda en términos de:
  - Nodos explorados.
  - Tiempo de ejecución.
  - Longitud del camino encontrado.

---

## 🧩 Estructura del Proyecto

```
proyecto2-busqueda/
│
├── maze/
│   ├── generator_maze.py    # Algoritmos de generación (Kruskal, Prim, etc.)
│   ├── solver.py            # Solvers de laberinto (BFS, DFS, UCS, A*)
│   ├── visualizer.py        # Funciones de visualización (construcción y resolución)
│   └── utils.py             # Funciones comunes: grid, coordenadas válidas, etc.
│
├── experiments/
│   ├── batch_runner.py      # Genera K laberintos y corre todos los algoritmos
│   └── analysis.py          # Calcula métricas: nodos explorados, tiempo, longitud
│
├── results/
│   ├── report.csv           # Datos de nodos explorados, tiempos y distancias
│   └── *.png                # Capturas de visualizaciones (opcional)
│
├── tests/                   # Pruebas unitarias
│   ├── test_generator.py
│   ├── test_solver.py
│   └── test_utils.py
│
└── 📁 data/
|    └── sample_mazes/        # Guardar laberintos generados (JSON, TXT, etc.)
│
├── main.py                  # Script principal de ejecución
├── requirements.txt         # Dependencias del proyecto
└── README.md
```

---

## 🧠 Algoritmos Implementados

### 🔨 Generación de laberintos

- Kruskal
- Prim

### 🚀 Solución de laberintos

- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- UCS (Uniform Cost Search / Dijkstra)
- A* (A estrella)

---

## 🔬 Comparación de algoritmos

Se ejecutan **25 simulaciones** con laberintos aleatorios de tamaño 45x55, comparando el rendimiento de los algoritmos. Se mide:

- 🧱 Nodos explorados
- ⏱ Tiempo de ejecución
- 📏 Longitud de la ruta

Los resultados se resumen en un archivo CSV y una tabla de ranking promedio.

---

## ▶️ Ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar ejemplo simple
python main.py

# Ejecutar experimentos masivos
python experiments/batch_runner.py
```

## 🎓 Curso

**Inteligencia Artificial - Primer Semestre 2025**  
Universidad de San Carlos de Guatemala