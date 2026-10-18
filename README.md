# Cuando el camino más corto no es el mejor

Práctica en equipo de **Fundamentos de Inteligencia Artificial**, grupo LITIID71.

Prototipo que simula una zona inundada como una cuadrícula. Un agente debe llegar desde una zona afectada hasta un refugio, sin pasar por zonas bloqueadas y considerando el riesgo de cada zona según su nivel de inundación. Se implementan y comparan cinco estrategias de búsqueda para mostrar la diferencia entre **encontrar una ruta** y **encontrar una ruta conveniente**.

**Archivo principal:** [`practica_rutas.ipynb`](practica_rutas.ipynb). Contiene las explicaciones, la visualización, la comparación de algoritmos con ejecuciones reales y las pruebas.

## Integrantes

| Integrante | Usuario de GitHub | Rol |
|---|---|---|
| Hector Partido Flores | @HectorPartido | Coordinación e integración |
| Ismael Alexander Hidalgo Aguilando | @Ismael-78 | Terreno y visualización |
| Hector Martínez Sánchez | @HectorMartinez17 | Búsqueda no informada |
| Gildardo Emmanuel González García | @Thenoob20-0 | Búsqueda informada y comparación |
| Anthony Oziel Ramos López | @ThonyOziel | Validación y pruebas |

## Resultados principales

En el escenario principal con λ = 1:

| Algoritmo | Pasos | Costo | Nodos expandidos |
|---|---|---|---|
| BFS | 11 | 25 | 81 |
| DFS | 83 | 151 | 93 |
| UCS | 19 | **19** | 89 |
| Greedy | 11 | 25 | 11 |
| A\* | 19 | **19** | **48** |

- La ruta más corta (11 pasos) cruza la zona inundada. La ruta conveniente (19 pasos) la rodea y cuesta menos.
- A\* obtiene el mismo costo óptimo que UCS con aproximadamente la mitad del trabajo, y lo confirma en 900 ejecuciones sobre mapas aleatorios.
- Al variar el peso del riesgo λ, la ruta elegida cambia en λ = 0.5 y λ = 0.67, exactamente donde lo predice el modelo de costo.

## Modelo del problema

| Nivel | Significado | Transitable | Riesgo |
|---|---|---|---|
| 0 | Seco | Sí | 0 |
| 1 | Inundación leve | Sí | 1 |
| 2 | Inundación media | Sí | 3 |
| 3 | Inundación severa | No | — |

- Movimiento en 4 direcciones, sin diagonales.
- Costo de entrar a una celda: `1 + λ · riesgo`.
- El sistema elige la ruta con menor costo total: `pasos + λ · riesgo acumulado`.

## Estructura del repositorio

```
├── practica_rutas.ipynb            Notebook principal
├── src/
│   ├── modelo.py                   Contrato común: niveles, riesgo y Resultado
│   ├── terreno.py                  Cuadrícula, vecinos, riesgo y costo de paso
│   ├── escenarios.py               Escenarios de prueba reutilizables
│   ├── busqueda_comun.py           Reconstrucción de rutas y armado de Resultado
│   ├── busqueda_no_informada.py    BFS, DFS y UCS
│   ├── busqueda_informada.py       Heurística Manhattan, Greedy y A*
│   ├── validacion.py               Validador independiente de rutas
│   └── visualizacion.py            Dibujo del terreno y comparación de rutas
├── requirements.txt
└── README.md
```

## Cómo reproducir los resultados

Requisitos: Python 3.10 o superior y Git.

```bash
git clone https://github.com/HectorPartido/litiid71-rutas-inundacion-ia.git
cd litiid71-rutas-inundacion-ia
```

Crear y activar el entorno virtual:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

Instalar dependencias y abrir el notebook:

```bash
pip install -r requirements.txt
jupyter notebook practica_rutas.ipynb
```

Ejecutar todas las celdas en orden (**Run All**). Los escenarios y los mapas aleatorios usan semillas fijas, así que los costos, pasos y nodos son siempre los mismos. Solo los tiempos varían según el equipo.

Para ejecutarlo completo desde la terminal, sin abrir Jupyter:

```bash
jupyter nbconvert --to notebook --execute practica_rutas.ipynb --output ejecucion_verificacion.ipynb
```

## Forma de trabajo

- Una rama por tarea y Pull Request a `main`, revisado por otro integrante.
- Commits con prefijo por tipo: `feat`, `fix`, `test`, `docs`, `chore`.
- Las salidas del notebook se limpiaron con `nbstripout` durante el desarrollo para evitar conflictos. En la versión de entrega (`v1.0`) se conservan para poder revisarlas en GitHub.

## Uso de herramientas de IA

Se describe en la sección 8 del notebook, incluido cómo se verificó el código generado.